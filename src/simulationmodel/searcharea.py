from abc import ABCMeta, abstractmethod
from dto.pose import Pose
from dto.point import Point
from dto.pdf import PDF
from dto.target import Target
from util.log import Log
import numpy as np
from scipy.stats import norm
from dto.searchareadto import SearchareaDTO
import copy
from simulationmodel.cell import Cell
from dto.celldto import CellDTO


class Searcharea:
	__metaclass__ = ABCMeta

	height = None
	width = None
	target = None
	realTarget = None
	sampledSpace = None
	gridsize = None
	halfSideLength = None
	cells = None
	data = None
	mean = 0
	stddev = 0.4
	middle = None
	firstTimeZeroProb = True
		
	@abstractmethod
	def updateSearchBasedOnLog(self, log):
		pass

	@abstractmethod
	def isCoverage(self):
		pass
		
	def randTarget(self):
		ex = (self.width / 2)
		ey = (self.height / 2)
		x = norm.rvs(self.mean, self.stddev)*ex
		y = norm.rvs(self.mean, self.stddev)*ey
		return x, y
	
	def radiusFromCenter(self, x, y):
		return (np.power(x, 2) / np.power((self.width / 2), 2)) + (np.power(y, 2) / np.power((self.height / 2), 2))
		
	def bigDia(self):
		return max([self.height, self.width])
		
	def inArea(self, pos):
		x, y = self.posToCellIndex(pos)
		return x >= 0 and x < self.cells and y >= 0 and y < self.cells
		
	def inSearchArea(self, pos):
		x = pos.getX()
		y = pos.getY()
		return self.radiusFromCenter(x, y) <= 1
		
	def inMiddleOfCell(self, pos):
		x, y = self.posToCellIndex(pos)
		margin = self.getMargin()
		posx = pos.getX()
		posy = pos.getY()
		correctx = posx > x - margin and posx < x + margin
		correcty = posy > y - margin and posy < y + margin
		return correctx and correcty
		
	def inMiddleOfSpecificCell(self, pos, cell):
		margin = self.getMargin()
		tarx = cell.getX()
		tary = cell.getY()
		posx = pos.getX()
		posy = pos.getY()
		correctx = posx > tarx - margin and posx < tarx + margin
		correcty = posy > tary - margin and posy < tary + margin
		return correctx and correcty
		
	def cellIndexToPos(self, xindex, yindex):
		dy = yindex * self.gridsize
		dx = xindex * self.gridsize
		y = dy - self.halfSideLength
		x = dx - self.halfSideLength
		return Point(x, y)

	def posToCellIndex(self, pos):
		x = int(round(pos.getX() + self.halfSideLength) / self.gridsize)
		y = int(round(pos.getY() + self.halfSideLength) / self.gridsize)
		return x, y
		
	def cellToCellIndex(self, cell):
		x = int(round(cell.getX() + self.halfSideLength) / self.gridsize)
		y = int(round(cell.getY() + self.halfSideLength) / self.gridsize)
		return x, y
		
	def getCellForPos(self, pos):
		x, y = self.posToCellIndex(pos)
		tx, ty = self.posToCellIndex(self.getTarget())
		hasTarget = tx == x and ty == y
		return Cell(self.data[y][x], x, y, hasTarget)
		
	def getHeight(self):
		return self.height
		
	def getWidth(self):
		return self.width
		
	def getGridsize(self):
		return self.gridsize
		
	def getData(self):
		return copy.deepcopy(self.data)
		
	def getHalfSideLength(self):
		return self.halfSideLength
		
	def getTarget(self):
		return self.realTarget
		
	def getDataForDist(self, dist):
		if dist > 1:
			return 0
		else:
			return norm.pdf(dist, self.mean, self.stddev) / 2.0
		
	def setTarget(self, targetx, targety):
		self.realTarget = Point(targetx, -targety)
		targetx = targetx + self.halfSideLength
		targety = self.halfSideLength - targety
		self.target = Point(targetx, targety)
		
	def getCells(self):
		return self.cells
		
	def getCellDTO(self, prob, xindex, yindex):
		pos = self.cellIndexToPos(xindex, yindex)
		return CellDTO(prob, xindex, yindex, pos)