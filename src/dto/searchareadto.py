from dto.pose import Pose
from dto.pdf import PDF
from dto.target import Target
from dto.logentry import LogEntry
from dto.point import Point

import copy

class SearchareaDTO():

	height = None
	width = None
	target = None
	gridsize = None
	halfSideLength = None
	cells = None
	data = None
	coverage = False
	
	def __init__(self, args):
		if len(args) == 1:
			area = copy.deepcopy(args[0])
			self.height = int(round(area.getHeight()))
			self.width = int(round(area.getWidth()))
			self.gridsize = area.getGridsize()
			self.data = area.getData()
			self.cells = len(self.data[0])
			self.halfSideLength = area.getHalfSideLength()
			self.target = area.getTarget()
			self.coverage = area.isCoverage()
		else:
			self.height = args[0]
			self.width = args[1]
			self.gridsize = args[2]
			self.target = Point(args[3], args[4])
		
	def getHeight(self):
		return self.height
		
	def getWidth(self):
		return self.width
		
	def getGridsize(self):
		return self.gridsize
		
	def getData(self):
		return self.data
		
	def getHalfSideLength(self):
		return self.halfSideLength
		
	def bigDia(self):
		return max([self.height, self.width])
		
	def getTarget(self):
		return self.target
		
	def setData(self, data):
		self.data = data
		
	def setZeroData(self):
		self.data = [0] * self.cells
		for i in range(self.cells):
			self.data[i] = [0] * self.cells
		self.data[int(self.cells / 2)][int(self.cells / 2)] = 1
		
	def setGridsize(self, gridsize):
		self.gridsize = gridsize
		
	def isCoverage(self):
		return self.coverage