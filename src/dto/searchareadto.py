from dto.pose import Pose
from dto.pdf import PDF
from dto.target import Target
from dto.logentry import LogEntry
from dto.point import Point

class SearchareaDTO():

	height = None
	width = None
	target = None
	gridsize = None
	halfSideLength = None
	cells = None
	data = None
	
	def __init__(self, args):
		if len(args) == 1:
			self.height = int(args[0].getHeight())
			self.width = int(args[0].getWidth())
			self.gridsize = args[0].getGridsize()
			self.data = args[0].getData()
			self.cells = len(self.data[0])
			self.halfSideLength = args[0].getHalfSideLength()
			self.target = args[0].getTarget()
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
		
	def getTarget(self):
		return self.target