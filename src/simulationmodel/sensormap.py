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

class SensorMap(Searcharea):

	height = None
	width = None
	target = None
	sampledSpace = None
	gridsize = None
	halfSideLength = None
	cells = None
	data = None
	mean = 0
	stddev = 0.4
	middle = None
				
	def __init__(self, a):
		self.height = int(round(a.getHeight()))
		self.width = int(round(a.getWidth()))
		gs = a.getGridsize()
		self.gridsize = int(gs / np.sqrt(2))
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
					self.data[yindex][xindex] = norm.pdf(self.radiusFromCenter(x, y), self.mean, self.stddev)
	
	def randTarget(self):
		ex = (self.width / 2)
		ey = (self.height / 2)
		x = norm.rvs(self.mean, self.stddev)*ex
		y = norm.rvs(self.mean, self.stddev)*ey
		return x, y
	
	def radiusFromCenter(self, x, y):
		return (np.power(x, 2) / np.power((self.width / 2), 2)) + (np.power(y, 2) / np.power((self.height / 2), 2))
	
	def bigDia(self):
		return max([self.height, self.width])
		
	def updateSearchBasedOnLog(self, log, showProb):
		returnData = []
		
		dt = log.getTimestepLength()
		
		for i in range(log.length() - 1):
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
			
			if i == log.length() - 2:
				xPos = int(round((fX + dX) + self.halfSideLength) / self.gridsize)
				yPos = int(round((fY + dY) + self.halfSideLength) / self.gridsize)
				self.data[yPos][xPos] = 0
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
		
	def getHeight(self):
		return self.height
		
	def getWidth(self):
		return self.width
		
	def getGridsize(self):
		return self.gridsize
		
	def getData(self):
		return copy.deepcopy(self.data)
		
	def getHalfSideLength(self):
		return self.halfSideLength
		
	def getTarget(self):
		return Point(self.target.getX() - self.halfSideLength, self.target.getY() - self.halfSideLength)
		
	def getAdjacentCells(self, pos):
		x, y = self.posToCellIndex(pos)
		print('in getAdjacentCells: ' + pos.toString() + ' ' + Point(x, y).toString())
		cells = []
		goodResult = False
		depth = 1
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
		
	def cellIndexToPos(self, xindex, yindex):
		dy = yindex * self.gridsize
		dx = xindex * self.gridsize
		y = dy - self.halfSideLength
		x = dx - self.halfSideLength
		return Point(x, y)

	def posToCellIndex(self, pos):
		x = int(round(pos.getX() + self.halfSideLength) / self.gridsize)
		y = int(round(pos.getY() + self.halfSideLength) / self.gridsize)
		return x, y

	def getCellForPos(self, pos):
		x, y = self.posToCellIndex(pos)
		tx, ty = self.posToCellIndex(self.getTarget())
		hasTarget = tx == x and ty == y
		return Cell(self.data[y][x], x, y, hasTarget)
		
	def getMargin(self):
		return self.gridsize * 0.2
		
	def inArea(self, pos):
		x, y = self.posToCellIndex(pos)
		return x >= 0 and x < self.cells and y >= 0 and y < self.cells
		
	def inMiddleOfCell(self, pos):
		x, y = self.posToCellIndex(pos)
		margin = self.getMargin()
		posx = pos.getX()
		posy = pos.getY()
		correctx = posx > x - margin and posx < x + margin
		correcty = posy > y - margin and posy < y + margin
		return correctx and correcty
		
	def inMiddleOfSpecificCell(self, pos, cell):
		margin = self.getMargin()
		tarx = cell.getX()
		tary = cell.getY()
		posx = pos.getX()
		posy = pos.getY()
		correctx = posx > tarx - margin and posx < tarx + margin
		correcty = posy > tary - margin and posy < tary + margin
		return correctx and correcty
