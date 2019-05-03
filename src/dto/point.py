import numpy as np

class Point():

	x = None
	y = None
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def getX(self):
		return self.x
		
	def getY(self):
		return self.y
		
	def toString(self):
		return '(' + repr(self.x) + ', ' + repr(self.y) + ')' 
		
	def equals(self, that):
		return self.x == that.getX() and self.y == that.getY()
		
	def distTo(self, that):
		return np.sqrt(np.power(self.x - that.getX(), 2) + np.power(self.y - that.getY(), 2))