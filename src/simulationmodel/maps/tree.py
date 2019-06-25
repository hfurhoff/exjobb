from dto.celldto import CellDTO
from dto.point import Point

#from simulationmodel.maps.quadtreemap import QuadtreeMap
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
	totProb = 0
	maxProb = 0
	children = None
	keys = None
	key = None
	maxKey = None
	
	
	def __init__(self, center, base, minGridsize, area, inputKey):
		self.center = center
		self.base = base
		self.minGridsize = minGridsize
		self.area = area
		self.key = inputKey
		self.root = area.getTree()
		self.children = dict()
		self.keys = [	"topLeft",
						"topRight",
						"botLeft",
						"botRight"]
		if self.inEllipse(center, base, area):
			if base * 0.5 > minGridsize and base * 0.5 > 1:
				diff = base * 0.25
				for key in self.keys:
					tempCenter = None
					x = center.getX()
					y = center.getY()
					if key == "topLeft":
						x = x - diff
						y = y + diff
					elif key == "topRight":
						x = x + diff
						y = y + diff
					elif key == "botLeft":
						x = x - diff
						y = y - diff
					elif key == "botRight":
						x = x + diff
						y = y - diff
					tempCenter = Point(x, y)
					tree = Tree(tempCenter, base * 0.5, minGridsize, area, key)
					self.children[key] = tree
					self.children[key].setParent(self)
					prob = self.children[key].getMaxProb()
					if prob > self.maxProb:
						self.maxProb = prob
						self.maxKey = key
					self.totProb += prob
			else:
				self.keys = ["leaf"]
				dist = self.radiusFromRootCenter(center, area)
				prob = area.getDataForDist(dist)
				self.totProb = prob
				self.maxProb = prob
				self.maxKey = "leaf"
				t = area.getTarget()
				hasTarget = self.posInCell(t)
				#hasTarget = hasTarget or pos.getX() <= self.center.getY() + (self.base * 0.5)
				#hasTarget = hasTarget or pos.getY() <= self.center.getY() + (self.base * 0.5)
				self.children["leaf"] = Leaf(Cell(prob, center.getX(), center.getY(), hasTarget), "leaf")
				self.children["leaf"].setParent(self)
				'''print('leaf created')
				print('keys: ' + repr(self.keys))
				print('children: ' + repr(self.children))
				print('----------------------------------------------')'''
		else:
			self.keys = []

	def setParent(self, parent):
		self.parent = parent

	def getLeafForPos(self, pos):
		if "leaf" in self.keys:
			return self.children["leaf"]
		else:
			leaf = Leaf(Cell(0, self.area.getHalfSideLength(), self.area.getHalfSideLength(), False), "outside ellipse")
			if self.posInCell(pos):
				for key in self.keys:
					if self.children[key].posInCell(pos):
						leaf = self.children[key].getLeafForPos(pos)
			return leaf

	def posInCell(self, pos):
		correctx = pos.getX() >= self.center.getX() - (self.base * 0.5) 
		correctx = correctx and pos.getX() < self.center.getX() + (self.base * 0.5)
		
		correcty = pos.getY() >= self.center.getY() - (self.base * 0.5) 
		correcty = correcty and pos.getY() < self.center.getY() + (self.base * 0.5)
		
		hasPos = correctx and correcty
		return hasPos

	def getSmallestBase(self):
		if self.key == 'root':
			return self.children["topLeft"].getSmallestBase()
		elif len(self.children) == 4:
			return self.children["botRight"].getSmallestBase()
		else:
			return self.base
			
	def getMaxPos(self):
		if "leaf" in self.keys:
			return self.children["leaf"].getPosition()
		else:
			return self.children[self.maxKey].getMaxPos()

	def getMaxProb(self):
		return self.maxProb
		
	def getTotProb(self):
		return self.totProb
		
	def updateProb(self, oldProb, newProb, childKey):
		diff = oldProb - newProb
		self.totProb = self.totProb - diff
		self.maxKey = childKey
		self.maxProb = newProb
		for key in self.keys:
			prob = self.children[key].getMaxProb()
			if prob > self.maxProb:
				self.maxProb = prob
				self.maxKey = key
		if self.parent != None:
			self.parent.updateProb(oldProb, newProb, self.key)
			
	def inEllipse(self, center, base, area):
		inEllipse = False
		x, y = center.getX(), center.getY()
		diff = 0.5 * base
		corners = [	center,
					Point(x + diff, y + diff), 
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
	key = "leaf"
	
	def __init__(self, cell, key):
		self.cell = cell
		self.key = key
		
	def setParent(self, parent):
		self.parent = parent
		
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
		
	def hasTarget(self):
		return self.cell.hasTarget()
		
	def updateProb(self, newProb):
		oldProb = self.getProb()
		self.cell.setProb(newProb)
		if self.parent != None:
			self.parent.updateProb(oldProb, newProb, self.key)