from dto.point import Point

class Cell():

	prob = 0
	visited = False
	active = False
	x = None
	y = None
	t = False

	def __init__(self, prob, x, y, target):
		self.x = x
		self.y = y
		self.prob = prob
		tx, ty = int(target.getX()), int(target.getY())
		self.t = int(x) == tx and int(y) == ty

	def getProb(self):
		return self.prob
		
	def setProb(self, prob):
		self.prob = prob
		
	def setActive(self):
		self.active = True
	
	def visit(self):
		self.prob *= 0.2
		self.visited = True
		
	def unvisit(self):
		self.visited = False
	
	def hasBeenVisited(self):
		return self.visited
		
	def hasTarget(self):
		return self.t
		
	def getX(self):
		return self.x
		
	def getY(self):
		return self.y
		
	def getPosition(self):
		return Point(self.x, self.y)
