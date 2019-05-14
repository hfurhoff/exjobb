from dto.searchareadto import SearchareaDTO
from dto.celldto import CellDTO
from dto.point import Point
from dto.pose import Pose

from util.log import Log

from simulationmodel.searcharea import Searcharea
from simulationmodel.tree import Tree, Leaf
from simulationmodel.cell import Cell

import numpy as np
from scipy.stats import norm
import copy

class QuadtreeMap(Searcharea):
	
	tree = None
	
	def __init__(self, a):
		self.height = int(round(a.getHeight()))
		self.width = int(round(a.getWidth()))
		self.gridsize = a.getGridsize()
		t = a.getTarget()
		
		self.halfSideLength = 0.6 * self.bigDia()

		targetx = None
		targety = None
		try:
			targetx = float(t.getX())
			targety = float(t.getY())
		except:	
			targetx, targety = self.randTarget()
		while self.radiusFromCenter(targetx, targety) >= 1:
			targetx, targety = self.randTarget()
		print('Target is at ' + Point(targetx, targety).toString())
		self.setTarget(targetx, targety)

		center = Point(0, 0)
		base = self.halfSideLength * 2.0
		minGridsize = self.gridsize
		area = self		
		self.tree = Tree(center, base, minGridsize, area, None)
		self.gridsize = self.tree.getSmallestBase()
		
		self.cells = int(round((self.halfSideLength * 2) / self.gridsize)) + 1
		self.middle = int(round(self.halfSideLength / self.gridsize))
		
	def isCoverage(self):
		return False
		
	def updateSearchBasedOnLog(self, log, showProb, maxPos):
		pass
		
	def setTarget(self, x, y):
		self.target = Point(x, y)
		
	def getTarget(self):
		return self.target
	
	def getTree(self):
		return self.tree
		
	def getMaxPos(self):
		return self.tree.getMaxPos()
		
	def getData(self):
		self.data = [0] * self.cells
		for i in range(self.cells):
			self.data[i] = [0] * self.cells
		return self.data