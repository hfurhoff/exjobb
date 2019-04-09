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

	height = None
	width = None
	target = None
	sampledSpace = None
	gridsize = None
	halfSideLength = None
	cells = None
	data = None
	mean = 0
	stddev = 0.5
				
	def __init__(self, a):
		self.height = int(a.getHeight())
		self.width = int(a.getWidth())
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
			while self.radiusFromCenter(targetx, targety) > 1:
				targetx, targety = self.randTarget()
		print('Target is at ' + Point(targetx, targety).toString())
		targetx = targetx + self.halfSideLength
		targety = self.halfSideLength - targety
		self.target = Point(targetx, targety)

		self.cells = int((self.halfSideLength * 2) / self.gridsize) + 1
		self.data = [0] * self.cells
		for i in range(self.cells):
			self.data[i] = [0] * self.cells
			
		'''		for i in range(self.cells):
			for j in range(self.cells):
				self.data[i][j] = Cell(j - self.halfSideLength, i - self.halfSideLength, self.target)
'''
		for yindex in range(self.cells):
			for xindex in range(self.cells):
				y = yindex - self.halfSideLength
				x = xindex - self.halfSideLength
				if self.radiusFromCenter(x, y) <= 1:
					self.data[yindex][xindex] = norm.pdf(self.radiusFromCenter(x, y), self.mean, self.stddev)
#					self.data[yindex][xindex].setActive()
	
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
		
	def updateSearchBasedOnLog(self, log):
		returnData = []
		#print(log.toString())
		#print(repr(log.length()))
		
		dt = log.getTimestepLength()
		
		for i in range(log.length() - 1):
			'''			for ii in range(self.cells):
				for jj in range(self.cells):
					self.data[ii][jj].unvisit()
'''
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
			
			steps = 10
			
			for s in range(steps + 1):
				xPos = int(fX + (dX * s / steps)) + int(self.halfSideLength)
				yPos = int(fY + (dY * s / steps)) + int(self.halfSideLength)
#				if not self.data[yPos][xPos].hasBeenVisited():
				self.data[yPos][xPos] *= 0.2
				if yPos == int(self.target.getY()) and xPos == int(self.target.getX()):
					for yindex in range(self.cells):
						for xindex in range(self.cells):
							self.data[yindex][xindex] = 0
					self.data[yPos][xPos] = 1
						
			returnData.append(SearchareaDTO([self]))
			
		return returnData
		
	def getHeight(self):
		return self.height
		
	def getWidth(self):
		return self.width
		
	def getGridsize(self):
		return self.gridsize
		
	def getData(self):
		'''		data = [0] * self.cells
		for i in range(self.cells):
			data[i] = [0] * self.cells
			
		for i in range(self.cells):
			for j in range(self.cells):
				data[i][j] = self.data[i][j].getProb()
'''
		return copy.deepcopy(self.data)
		
	def getHalfSideLength(self):
		return self.halfSideLength
		
	def getTarget(self):
		return Point(self.target.getX() - self.halfSideLength, self.target.getY() - self.halfSideLength)
		
	def getAdjacentCells(self, pos):
		x = int(pos.getX()) + int(self.cells / 2)
		y = int(pos.getY()) + int(self.cells / 2)
		cells = []
		ystart = -1
		xstart = -1
		if y == 0:
			ystart = 0
		if x == 0:
			xstart = 0
		ystop = 2
		xstop = 2
		if y + ystop >= self.cells:
			ystop = 1
		if x + xstop >= self.cells:
			xstop = 1
		print('in getAdjacentCells ' + repr(x) + ' ' + repr(y) + ' datalen ' + repr(len(self.data)) + ' ' + repr(self.cells))
		for i in range(ystart, ystop):
			for j in range(xstart, xstop):
				if i == 0 and j == 0:
					pass
				else:
					print(repr(x + j) + ' ' + repr(y + i))
					cells.append((self.data[y + i][x + j], x + j, y + i))
		return cells
