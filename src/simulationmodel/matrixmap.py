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
	
	class Cell():
	
		prob = 0
		visited = False
	
		def __init__(self):
			pass
	
		def getProb(self):
			return self.prob
			
		def setProb(self, prob):
			self.prob = prob
		
		def visit(self):
			self.prob *= 0.5
			self.visited = True
			
		def hasBeenVisited(self):
			return self.visited
	
	def __init__(self, a):
		self.height = int(a.getHeight())
		self.width = int(a.getWidth())
		self.gridsize = a.getGridsize()
		t = a.getTarget()
		
		self.halfSideLength = 0.6 * self.bigDia()

		self.cells = int((self.halfSideLength * 2) / self.gridsize) + 1
		self.data = [None] * self.cells
		for i in range(self.cells):
			self.data[i] = [None] * self.cells
			
		for i in range(self.cells):
			for j in range(self.cells):
				self.data[i][j] = self.Cell()
				
		for yindex in range(self.cells):
			for xindex in range(self.cells):
				y = yindex - self.halfSideLength
				x = xindex - self.halfSideLength
				if self.radFromCenter(x, y) <= 1:
					self.data[yindex][xindex].setProb(norm.pdf(self.radFromCenter(x, y), 0, 0.5))

		x = None
		y = None
		try:
			x = int(t.getX())
			y = int(t.getY())
		except:	
			x, y = self.randTarget()
			while self.radFromCenter(x, y) > 1:
				x, y = self.randTarget()
		print('Target is at ' + Point(x, y).toString())
		x = int(x + self.halfSideLength)
		y = int(self.halfSideLength - y)
		self.target = Point(x, y)
		#self.data[y][x] = 1
	
	def randTarget(self):
		ex = (self.width / 2)
		ey = (self.height / 2)
		x = int(norm.rvs(0, 0.5)*ex)
		y = int(norm.rvs(0, 0.5)*ey)
		return x, y
	
	def radFromCenter(self, x, y):
		return (np.power(x, 2) / np.power((self.width / 2), 2)) + (np.power(y, 2) / np.power((self.height / 2), 2))
	
	def bigDia(self):
		return max([self.height, self.width])
		
	def updateSearchBasedOnLog(self, log):
		returnData = []
		print(log.toString())
		print(repr(log.length()))
		for i in range(log.length() - 1):
			print(repr(i) + ' ' + log.get(i).toString() + ' ' + repr(i + 1) + ' ' + log.get(i + 1).toString())
			logFrom = log.get(i)
			logTo = log.get(i + 1)
			
			posFrom = logFrom.getPose().getPosition()
			fX = posFrom.getX()
			fY = posFrom.getY()
			
			posTo = logTo.getPose().getPosition()
			tX = posTo.getX()
			tY = posTo.getY()
			
			hypo = int((np.sqrt([np.power(fX - tX, 2) + np.power(fY - tY, 2)])[0]) / self.gridsize) + 1
			for j in range(hypo + 1):
				xPos = int(fX * (1.0 - (float(j) / float(hypo))) + int(self.halfSideLength))
				yPos = int(fY * (1.0 - (float(j) / float(hypo))) + int(self.halfSideLength))
				if not self.data[yPos][xPos].hasBeenVisited():
					self.data[yPos][xPos].visit()
					returnData.append(SearchareaDTO([copy.deepcopy(self)]))
			
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
		return self.target
		