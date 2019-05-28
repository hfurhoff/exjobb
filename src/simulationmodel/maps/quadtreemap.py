from dto.searchareadto import SearchareaDTO
from dto.celldto import CellDTO
from dto.point import Point
from dto.pose import Pose

from util.log import Log

from simulationmodel.searcharea import Searcharea
from simulationmodel.maps.tree import Tree 
from simulationmodel.maps.tree import Leaf
from simulationmodel.cell import Cell

import numpy as np
from scipy.stats import norm
import copy

class QuadtreeMap(Searcharea):
	
	tree = None
	changesInStore = []
	
	def __init__(self, a):
		self.height = int(round(a.getHeight()))
		self.width = int(round(a.getWidth()))
		self.gridsize = a.getGridsize()
		t = a.getTarget()
		
		self.halfSideLength = 0.6 * self.bigDia()

		targetx = None
		targety = None
		try:
			targetx = float(t.getX())
			targety = float(t.getY())
		except:	
			targetx, targety = self.randTarget()
		while self.radiusFromCenter(targetx, targety) >= 1:
			targetx, targety = self.randTarget()
		print('Target is at ' + Point(targetx, targety).toString())
		self.setTarget(targetx, -targety)

		center = Point(0, 0)
		base = self.halfSideLength * 2.0
		minGridsize = self.gridsize
		area = self		
		self.tree = Tree(center, base, minGridsize, area, 'root')
		#print('tree is made')
		self.gridsize = self.tree.getSmallestBase()
		
		self.cells = int(round((self.halfSideLength * 2) / self.gridsize)) + 1
		self.middle = int(round(self.halfSideLength / self.gridsize))
		self.data = [None] * self.cells
		for i in range(self.cells):
			self.data[i] = [None] * self.cells
		
		for yindex in range(self.cells):
			for xindex in range(self.cells):
				pos = self.cellIndexToPos(xindex, yindex)
				leaf = self.tree.getLeafForPos(pos)
				self.data[yindex][xindex] = copy.copy(leaf)
		
	def isCoverage(self):
		return False
		
	def updateSearchBasedOnLog(self, log, showProb, maxPos):
		returnData = []
		dt = log.getTimestepLength()
		for i in range(log.length() - 1):
			changes = []
			if len(self.changesInStore) > 0:
				for c in self.changesInStore:
					changes.append(c)
				self.changesInStore = []
			logFrom = log.get(i)
			sensor = logFrom.getSensor()
			posFrom = logFrom.getPose().getPosition()
			fX = posFrom.getX()
			fY = posFrom.getY()
			leaf = self.tree.getLeafForPos(posFrom)
			leafPos = leaf.getPosition()
			xPos, yPos = self.posToCellIndex(leafPos)
			
			logTo = log.get(i + 1)
			posTo = logTo.getPose().getPosition()
			found = self.getCellForPos(posTo).hasTarget()
			found = found or self.getCellForPos(posTo).hasTarget()
			if found:
				maxPos = self.target
			else:
				sensorRange = sensor.getMaxRange()
				depth = int(round(sensorRange / self.getGridsize()) + 1)
				adjCells = self.getAdjacentCells(leafPos, depth)
				priorProb = leaf.getProb()
				leaf.updateProb(0)
				if showProb  and not priorProb == leaf.getProb():
					changes.append(self.getCellDTO(leaf.getProb(), xPos, yPos))
				for cell in adjCells:
					cpos = cell.getPosition()
					dist = posFrom.distTo(cpos)
					if dist <= sensorRange:
						x, y = self.posToCellIndex(cpos)
						probOfDetection = sensor.probabilityOfDetection(dist)
						priorProb = self.data[y][x].getProb()
						self.data[y][x].updateProb(self.data[y][x].getProb() * (1.0 - probOfDetection))
						if showProb and not priorProb == self.data[y][x].getProb():
							if self.firstTimeZeroProb:
								changes.append(self.getCellDTO(self.data[y][x].getProb(), x, y))
				if not self.firstTimeZeroProb and showProb:
					for yy in range(self.cells):
						for xx in range(self.cells):
							changes.append(self.getCellDTO(self.data[yy][xx].getProb(), xx, yy))
					self.firstTimeZeroProb = True
			
			if not showProb:
				x, y = self.posToCellIndex(maxPos)
				zeroProbs = [0] * self.cells
				for i in range(self.cells):
					zeroProbs[i] = [0] * self.cells
				zeroProbs[y][x] = 1
				if self.firstTimeZeroProb:
					for i in range(self.cells):
						for j in range(self.cells):
							changes.append(self.getCellDTO(zeroProbs[i][j], j, i))
				self.firstTimeZeroProb = False
			returnData.append(changes)
		return returnData

	def getCellForPos(self, pos):
		x, y = self.posToCellIndex(pos)
		return self.data[y][x]
		
	def setTarget(self, x, y):
		self.target = Point(x, y)
		
	def getTarget(self):
		return self.target
	
	def getTree(self):
		return self.tree
		
	def getMaxPos(self):
		return self.tree.getMaxPos()
		
	def getMaxProb(self):
		return self.tree.getMaxProb()
		
	def getData(self):
		data = [0] * self.cells
		for i in range(self.cells):
			data[i] = [0] * self.cells
			
		for y in range(self.cells):
			for x in range(self.cells):
				data[y][x] = self.data[y][x].getProb()
		return data
		
	def getAdjacentCells(self, pos, depth):
		x, y = self.posToCellIndex(pos)
		cells = []
		ystart = -depth
		xstart = -depth
		while y + ystart < 0:
			ystart = ystart + 1
		while x + xstart < 0:
			xstart = xstart + 1
		ystop = depth + 1
		xstop = depth + 1
		while y + ystop > self.cells:
			ystop = ystop - 1
		while x + xstop > self.cells:
			xstop = xstop - 1

		for i in range(ystart, ystop):
			for j in range(xstart, xstop):
				if i == 0 and j == 0:
					pass
				else:
					p = self.cellIndexToPos(x + j, y + i)
					c = self.data[y + i][x + j]
					cells.append(c)
		return cells
		
	def getMargin(self):
		return self.gridsize * 0.5

	def raiseNearby(self, sensor, pos):
		leaf = self.tree.getLeafForPos(pos)
		leafPos = leaf.getPosition()
		sensorRange = sensor.getMaxRange()
		d = int(round(sensorRange / self.getGridsize()) + 1)
		adjCells = self.getAdjacentCells(leafPos, d)
		leaf.updateProb(0)
		xPos, yPos = self.posToCellIndex(leafPos)
		self.changesInStore.append(self.getCellDTO(leaf.getProb(), xPos, yPos))
		for cell in adjCells:
			cpos = cell.getPosition()
			dist = pos.distTo(cpos)
			if dist <= sensorRange:
				x, y = self.posToCellIndex(cpos)
				probOfDetection = sensor.probabilityOfDetection(dist)
				if probOfDetection == 1:
					self.data[y][x].updateProb(0)
				else:
					cProb = self.data[y][x].getProb()
					if not cProb == 0:
						self.data[y][x].updateProb(cProb + (sensor.getRadiusProb() - probOfDetection) + 0.5)
				self.changesInStore.append(self.getCellDTO(self.data[y][x].getProb(), x, y))
