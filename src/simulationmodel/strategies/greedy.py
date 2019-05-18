from dto.course import Course
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.maps.sensormap import SensorMap
from simulationmodel.cell import Cell
from dto.point import Point
import numpy as np


class Greedy(NavigationStrategy):

	found = False

	def __init__(self):
		pass
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def foundTarget(self):
		if self.found:
			return True
		#print('checking, in greedy')
		vp = self.vehicle.getPosition()
		if self.area.inArea(vp):
			found = self.area.getCellForPos(vp).hasTarget()
		else:
			found = False
			
		self.found = found
		#if(found):
			#print('found target')
		return found
		
	def nextPos(self, vehicle, area):
		pos = vehicle.getPosition()
		if self.atPosition(vehicle, area, self.target): 
			#get new target
			#print('get new target')
			cells = area.getAdjacentCells(pos)
			tarpos = cells[0]
			for cell in cells:
				#print(cell.toString())
				if cell.getProb() > tarpos.getProb():
					tarpos = cell
				self.target = tarpos.getPosition()
		#print('Target ' + self.target.toString())
		return self.target
		
	def test(self):
		print('GreedyStrat')