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
		return '(' + repr(round(self.x, 2)) + ', ' + repr(round(self.y, 2)) + ')' 
		
	def equals(self, that):
		return self.x == that.getX() and self.y == that.getY()
		
	def distTo(self, that):
		return np.sqrt(np.power(self.x - that.getX(), 2) + np.power(self.y - that.getY(), 2))
		
	def rotate(self, a):
		rad = np.deg2rad(a)
		x1 = self.x
		y1 = self.y
		x = x1 * np.cos(rad) - y1 * np.sin(rad)
		y = x1 * np.sin(rad) + y1 * np.cos(rad)
		return Point(x, y)
		
	def translate(self, x, y):
		return Point(self.x + x, self.y + y)