from dto.course import Course
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.maps.sensormap import SensorMap
from simulationmodel.cell import Cell
from dto.point import Point
import numpy as np


class Greedy(NavigationStrategy):

	def __init__(self):
		pass
		
	def makeArea(self, area, sensor, depth):
		return SensorMap(area, sensor)
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
				
	def nextPos(self, vehicle, area):
		pos = vehicle.getPosition()
		if self.atPosition(vehicle, area, self.target): 
			cells = area.getAdjacentCells(pos)
			tarpos = cells[0]
			for cell in cells:
				if cell.getProb() > tarpos.getProb():
					tarpos = cell
				self.target = tarpos.getPosition()
		return self.target
		
	def test(self):
		print('GreedyStrat')