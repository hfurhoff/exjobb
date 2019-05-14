from dto.celldto import CellDTO
from dto.point import Point

from simulationmodel.maps.quadtreemap import QuadtreeMap
from simulationmodel.searcharea import Searcharea
from simulationmodel.cell import Cell

import numpy as np

class Tree():
	
	center = None
	base = None
	minGridsize = None
	area = None
	parent = None
	root = None
	prob = 0
	maxProb = 0
	children = {'topLeft'	: None,
				'topRight'	: None,
				'botLeft'	: None,
				'botRight'	: None}
	
	
	def __init__(self, center, base, minGridsize, area, parent):
		self.center = center
		self.base = base
		self.minGridsize = minGridsize
		self.area = area
		self.parent = parent
		self.root = area.getTree()
		if self.inEllipse(center, base, area):
			if base > minGridsize:
				diff = base * 0.25
				for key in self.children:
					tempCenter = None
					x = center.getX()
					y = center.getY()
					if key == 'topLeft':
						x = x - diff
						y = y + diff
					elif key == 'topRight':
						x = x + diff
						y = y + diff
					elif key == 'botLeft':
						x = x - diff
						y = y - diff
					elif key == 'botRight':
						x = x + diff
						y = y - diff
					tempCenter = Point(x, y)
					self.children[key] = Tree(tempCenter, base * 0.5, minGridsize, area, self)
					prob = self.children[key].getProb()
					if prob > self.maxProb:
						self.maxProb = prob
					self.prob += prob
			else:
				self.children.clear()
				dist = self.radiusFromRootCenter(center, area)
				prob = area.getDataForDist(dist)
				self.prob = prob
				self.maxProb = prob
				t = area.getTarget()
				correctx = t.getX() >= center.getX() - (base * 0.5) and t.getX() <= center.getX() + (base * 0.5)
				correcty = t.getY() >= center.getY() - (base * 0.5) and t.getY() <= center.getY() + (base * 0.5)
				hasTarget = correctx and correcty
				self.children.update({'leaf': Leaf(self, Cell(prob, center.getX(), center.getY(), hasTarget))})
		else:
			self.children.clear()

	def getSmallestBase(self):
		if self.parent == None:
			return self.children['topLeft'].getSmallestBase()
		elif len(self.children) == 4:
			return self.children['botRight'].getSmallestBase()
		else:
			return self.base
			
	def getMaxPos(self):
		maxProb = 0
		max = None
		for c in self.children;
			prob = self.children[c].getMaxProb()
			if prob > maxProb:
				max = self.children[c]
		if isinstance(max, Leaf):
			return max.getPosition()
		elif isinstance(max, Tree):
			return max.getMaxPos()
		else:
			print('in getMaxProb, something went wrong')
			return None

	def getMaxProb(self):
		return self.maxProb

	def inEllipse(self, center, base, area):
		inEllipse = False
		x, y = center.getX(), center.getY()
		diff = 0.5 * base
		corners = [	Point(x + diff, y + diff), 
					Point(x - diff, y + diff), 
					Point(x + diff, y - diff), 
					Point(x - diff, y - diff)]
		for corner in corners:
			inEllipse = inEllipse or self.radiusFromRootCenter(corner, area) <= 1
		return inEllipse

	def radiusFromRootCenter(self, pos, area):
		x = pos.getX()
		y = pos.getY()
		return (np.power(x, 2) / np.power((area.getWidth() / 2), 2)) + (np.power(y, 2) / np.power((area.getHeight() / 2), 2))

class Leaf():

	parent = None
	cell = None
	
	def __init__(self, parent, cell):
		self.parent = parent
		self.cell = cell
		
	def getCell(self):
		return self.cell
		
	def getParent(self):
		return self.parent
		
	def getProb(self):
		return self.cell.getProb()
		
	def getPosition(self):
		return self.cell.getPosition()
		
	def getMaxProb(self):
		return self.getProb()