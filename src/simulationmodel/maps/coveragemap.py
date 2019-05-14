from dto.pose import Pose
from dto.point import Point
from dto.pdf import PDF
from dto.target import Target
from util.log import Log
from simulationmodel.searcharea import Searcharea
import numpy as np
from scipy.stats import norm
from dto.searchareadto import SearchareaDTO
import copy
from simulationmodel.cell import Cell
from dto.celldto import CellDTO


class CoverageMap(Searcharea):

	found = False
			
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
					self.data[yindex][xindex] = 1
		self.firstTimeZeroProb = False
					
	def isCoverage(self):
		return True

	def updateSearchBasedOnLog(self, log, showProb, maxPos):
		returnData = []
		dt = log.getTimestepLength()
		for i in range(log.length() - 1):
			changes = []
			logFrom = log.get(i)
			sensor = logFrom.getSensor()
			posFrom = logFrom.getPose().getPosition()
			fX = posFrom.getX()
			fY = posFrom.getY()
			xPos = int(round((fX + self.halfSideLength) / self.gridsize))
			yPos = int(round((fY + self.halfSideLength) / self.gridsize))

			logTo = log.get(i + 1)
			posTo = logTo.getPose().getPosition()
			found = self.getCellForPos(posTo).hasTarget()
			found = found or self.getCellForPos(posTo).hasTarget()
			if found:
				maxPos = self.realTarget
			else:
				sensorRange = sensor.getRadius()
				depth = int(round(sensorRange)) + 1
				adjCells = self.getAdjacentCells(posFrom, depth)
				self.data[yPos][xPos] = 0.5
				changes.append(self.getCellDTO(self.data[yPos][xPos], xPos, yPos))
				for cell in adjCells:
					cpos = cell.getPosition()
					dist = posFrom.distTo(cpos)
					if dist <= sensorRange:
						x, y = self.posToCellIndex(cpos)
						probOfDetection = sensor.probabilityOfDetection(dist)
						if probOfDetection == 1:
							self.data[y][x] = 0.5
						if self.firstTimeZeroProb:
							changes.append(self.getCellDTO(self.data[y][x], x, y))
						else:
							for yy in range(self.cells):
								for xx in range(self.cells):
									changes.append(self.getCellDTO(self.data[yy][xx], xx, yy))
						self.firstTimeZeroProb = True
			returnData.append(changes)
		return returnData
		
	def foundTarget(self):
		return self.found
		
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
					hasTarget = False
					tpx, tpy = self.posToCellIndex(self.realTarget)
					hasTarget = p.getX() == tpx
					hasTarget = hasTarget and p.getY() == tpy
					c = Cell(self.data[y + i][x + j], p.getX(), p.getY(), hasTarget)
					cells.append(c)
		return cells
		
	def getMargin(self):
		return self.gridsize * 0.4
