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
	
	class Cell():
	
		prob = 0
		visited = False
		active = False
		x = None
		y = None
		t = False
	
		def __init__(self, x, y, target):
			self.x = x
			self.y = y
			self.target = target
			tx, ty = int(target.getX()), int(target.getY())
			self.t = x == tx and y == ty
	
		def getProb(self):
			return self.prob
			
		def setProb(self, prob):
			self.prob = prob
			
		def setActive(self):
			self.active = True
		
		def visit(self):
			self.prob *= 0.2
			self.visited = True
			
		def hasBeenVisited(self):
			return self.visited
			
		def hasTarget(self):
			return self.t
			
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
		self.data = [None] * self.cells
		for i in range(self.cells):
			self.data[i] = [None] * self.cells
			
		for i in range(self.cells):
			for j in range(self.cells):
				self.data[i][j] = self.Cell(j, i, self.target)
				
		print('datalen ' + repr(len(self.data)))
		print('cells ' + repr(self.cells))
				
		for yindex in range(self.cells):
			for xindex in range(self.cells):
				y = yindex - self.halfSideLength
				x = xindex - self.halfSideLength
				if self.radiusFromCenter(x, y) <= 1:
					self.data[yindex][xindex].setProb(norm.pdf(self.radiusFromCenter(x, y), self.mean, self.stddev))
					self.data[yindex][xindex].setActive()
	
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
				if not self.data[yPos][xPos].hasBeenVisited():
					self.data[yPos][xPos].visit()
					if self.data[yPos][xPos].hasTarget():
						for yindex in range(self.cells):
							for xindex in range(self.cells):
								self.data[yindex][xindex].setProb(0)
						self.data[yPos][xPos].setProb(1)
						
			returnData.append(SearchareaDTO([self]))
			
		return returnData
		
	def getHeight(self):
		return self.height
		
	def getWidth(self):
		return self.width
		
	def getGridsize(self):
		return self.gridsize
		
	def getData(self):
		data = [0] * self.cells
		for i in range(self.cells):
			data[i] = [0] * self.cells
			
		for i in range(self.cells):
			for j in range(self.cells):
				data[i][j] = self.data[i][j].getProb()
		return data
		
	def getHalfSideLength(self):
		return self.halfSideLength
		
	def getTarget(self):
		return Point(self.target.getX() - self.halfSideLength, self.target.getY() - self.halfSideLength)
		