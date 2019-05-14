from dto.point import Point
import copy

class CellDTO():

	prob = 0
	x = None
	y = None
	pos = None

	def __init__(self, prob, x, y, pos):
		self.x = x
		self.y = y
		self.prob = copy.deepcopy(prob)
		self.pos = pos

	def getProb(self):
		return self.prob
		
	def setProb(self, prob):
		self.prob = prob
				
	def getX(self):
		return self.x
		
	def getY(self):
		return self.y
		
	def getPosition(self):
		return self.pos

	def toString(self):
		return 'Cell: ' + self.getPosition().toString() + ', ' + repr(self.getProb())