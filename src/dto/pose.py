from dto.point import Point
from dto.course import Course

class Pose():

	orientation = None
	position = None

	def __init__(self, orientation, position):
		self.orientation = orientation
		self.position = position
		
	def getOrientation(self):
		return self.orientation
		
	def getPosition(self):
		return self.position
		
	def setPosition(self, p):
		self.position = p
		
	def toString(self):
		#return 'Course ' + repr(self.orientation) + ' at: ' + self.position.toString()
		return self.position.toString()