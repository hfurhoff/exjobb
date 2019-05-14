from simulationmodel.searcharea import Searcharea
from dto.pose import Pose
from dto.point import Point
from dto.target import Target
from util.log import Log
import numpy as np
from scipy.stats import norm
from dto.searchareadto import SearchareaDTO
import copy
from simulationmodel.cell import Cell
from dto.celldto import CellDTO

class SensorMap(Searcharea):
			
	def __init__(self, a, sensor):
		self.height = int(round(a.getHeight()))
		self.width = int(round(a.getWidth()))
		gs = sensor.getDiameter()
		self.gridsize = int(gs / np.sqrt(2)) + 1
		if self.gridsize == 0:
			self.gridsize = 1
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
		self.setTarget(targetx, targety)
		
		self.cells = int(round((self.halfSideLength * 2) / self.gridsize)) + 1
		self.middle = int(round(self.halfSideLength / self.gridsize))
		self.data = [0] * self.cells
		for i in range(self.cells):
			self.data[i] = [0] * self.cells
			
		for yindex in range(self.cells):
			dy = yindex * self.gridsize
			for xindex in range(self.cells):
				dx = xindex * self.gridsize
				y = dy - self.halfSideLength - (np.sign(dy - self.halfSideLength) * float(self.gridsize) * 0.5)
				x = dx - self.halfSideLength - (np.sign(dx - self.halfSideLength) * float(self.gridsize) * 0.5)
				if self.radiusFromCenter(x, y) <= 1:
					self.data[yindex][xindex] = self.getDataForDist(self.radiusFromCenter(x, y))
	
	def isCoverage(self):
		return False
	
	def updateSearchBasedOnLog(self, log, showProb, maxPos):
		returnData = []
		dt = log.getTimestepLength()
		for i in range(log.length() - 1):
			changes = []
			logFrom = log.get(i)
			logTo = log.get(i + 1)
			posFrom = logFrom.getPose().getPosition()
			fX = posFrom.getX()
			fY = posFrom.getY()
			posTo = logTo.getPose().getPosition()
			tX = posTo.getX()
			tY = posTo.getY()
			dX = tX - fX
			dY = tY - fY
			averageSpeed = (logFrom.getSpeed() + logTo.getSpeed()) / 2
			steps = averageSpeed / dt
			xPos = int(round((fX + dX) + self.halfSideLength) / self.gridsize)
			yPos = int(round((fY + dY) + self.halfSideLength) / self.gridsize)
			
			if i == log.length() - 2:
				self.data[yPos][xPos] = 0

			if showProb:
				if self.firstTimeZeroProb:
					changes.append(self.getCellDTO(self.data[yPos][xPos], xPos, yPos))
				else:
					for yy in range(self.cells):
						for xx in range(self.cells):
							changes.append(self.getCellDTO(self.data[yy][xx], xx, yy))
				self.firstTimeZeroProb = True
			else:
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
		
	def getAdjacentCells(self, pos):
		x, y = self.posToCellIndex(pos)
		#print('in getAdjacentCells: ' + pos.toString() + ' ' + Point(x, y).toString())
		cells = []
		goodResult = False
		depth = 1
		while(not goodResult):
			#print(repr(depth))
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
						if self.data[y + i][x + j] > 0:
							goodResult = True
						p = self.cellIndexToPos(x + j, y + i)
						hasTarget = False
						tpx, tpy = self.posToCellIndex(self.realTarget)
						hasTarget = x + j == tpx
						hasTarget = hasTarget and y + i == tpy
						c = Cell(self.data[y + i][x + j], p.getX(), p.getY(), hasTarget)
						cells.append(c)
			depth = depth + 1
			if depth == self.cells:
				break
		return cells
		
	def getMargin(self):
		return self.gridsize * 0.2
