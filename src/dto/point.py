
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