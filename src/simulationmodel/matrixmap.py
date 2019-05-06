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

class MatrixMap(Searcharea):
			
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
		targetx = targetx + self.halfSideLength
		targety = self.halfSideLength - targety
		self.target = Point(targetx, targety)

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
					

	def updateSearchBasedOnLog(self, log, showProb):
		returnData = []
		dt = log.getTimestepLength()
		for i in range(log.length() - 1):
			logFrom = log.get(i)
			sensor = logFrom.getSensor()
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
			steps = int(round(averageSpeed / dt))

			for s in range(1, steps + 1):
				xPos = int(round((fX + (dX * s / steps)) + self.halfSideLength) / self.gridsize)
				yPos = int(round((fY + (dY * s / steps)) + self.halfSideLength) / self.gridsize)
				if xPos >= self.cells - 1 or yPos >= self.cells - 1:
					pass
				else:
					self.data[yPos][xPos] = (1 - sensor.probabilityOfDetection(0)) * self.data[yPos][xPos]
					
					found = self.getCellForPos(posTo).hasTarget()
					if found:
						for yindex in range(self.cells):
							for xindex in range(self.cells):
								self.data[yindex][xindex] = 0
						self.data[yPos][xPos] = 1
						
			dto = SearchareaDTO([self])
			if not showProb:
				zeroProbs = [0] * self.cells
				for i in range(self.cells):
					zeroProbs[i] = [0] * self.cells
				zeroProbs[self.middle][self.middle] = 1
				dto.setData(zeroProbs)
			returnData.append(dto)
			
		return returnData
		
	def getAdjacentCells(self, pos, depth):
		x, y = self.posToCellIndex(pos)
		cells = []
		goodResult = False
		while(not goodResult):
			print(repr(depth))
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
						c = Cell(self.data[y + i][x + j], p.getX(), p.getY(), self.target)
						cells.append(c)
			depth = depth + 1
			if depth == self.cells:
				break
		return cells
		
	def getMargin(self):
		return self.gridsize * 0.2
