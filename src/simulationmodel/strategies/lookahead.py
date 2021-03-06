from dto.course import Course
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.maps.matrixmap import MatrixMap
from simulationmodel.cell import Cell
from dto.point import Point
from dto.sensor import Sensor
import numpy as np



class Lookahead(NavigationStrategy):

	depth = None
	sensor = None

	def __init__(self):
		pass
		
	def makeArea(self, area, sensor, depth):
		self.setDepth(depth)
		self.sensor = sensor
		return MatrixMap(area)
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def nextPos(self, vehicle, area):
		pos = vehicle.getPosition()
		if self.atPositionWithExtraMargin(vehicle, area, self.target): 
			sensor = vehicle.getSensor()
			d = int(round(self.depth * sensor.getRadius() / area.getGridsize()) + 1)
			currentHeading = vehicle.getHeading()
			currentCell = area.getCellForPos(pos)
			targetCell = currentCell
			i = 1
			cutoff = 0.1
			while float(targetCell.getProb()) < cutoff and d + i < area.getCells():
				cells = area.getAdjacentCells(pos, d + i)
				targetCell = cells[0]
				maxValue = self.calculateValue(vehicle, targetCell)
				for cell in cells:
					value = self.calculateValue(vehicle, cell)
					if value > maxValue and area.inSearchArea(cell.getPosition()):
						targetCell = cell
						maxValue = value
					self.target = targetCell.getPosition()
				i = i * 2
				if d + i >= area.getCells() - 1:
					i = 1
					cutoff = cutoff / 2.0
		return self.target
		
	def atPositionWithExtraMargin(self, vehicle, area, target):
		margin = max([area.getGridsize(), self.sensor.getRadius() * 0.9])
		tarx = target.getX()
		tary = target.getY()
		pos = vehicle.getPosition()
		posx = pos.getX()
		posy = pos.getY()
		correctx = posx > tarx - margin and posx < tarx + margin
		correcty = posy > tary - margin and posy < tary + margin
		return correctx and correcty
		
	def calculateValue(self, vehicle, cell):
		pos = vehicle.getPosition()
		currentHeading = vehicle.getHeading()
		cpos = cell.getPosition()
		tr = vehicle.getTurningRadius()
		course = self.getCourseFromTo(pos, cpos)
		diff = currentHeading - course
		sign = 1
		if int(diff) != 0:
			sign = diff / abs(diff)
		if abs(diff) > 180:
			if sign < 0:
				diff = diff + 360
			else:
				diff = diff - 360
		diff = abs(diff)
		reward = cell.getProb()
		steps = int(diff / tr) + 1
		cost = steps * 0.5
		value = reward
		return value
		
	def setDepth(self, depth):
		self.depth = depth
		
	def test(self):
		print('LookaheadStrat')