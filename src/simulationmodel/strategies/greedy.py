from dto.course import Course
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.sensormap import SensorMap
from simulationmodel.cell import Cell
from dto.point import Point
import numpy as np


class Greedy(NavigationStrategy):

	found = False

	def __init__(self):
		pass
		
	def nextCourse(self, vehicle, area):
		'''pos = vehicle.getPosition()
		margin = area.getMargin()
		tarx = self.target.getX()
		tary = self.target.getY()
		posx = pos.getX()
		posy = pos.getY()
		correctx = posx > tarx - margin and posx < tarx + margin
		correcty = posy > tary - margin and posy < tary + margin
		if correctx and correcty: 
			#get new target
			cells = area.getAdjacentCells(pos)
			tarpos = cells[0]
			for cell in cells:
				if cell.getProb() > tarpos.getProb():
					tarpos = cell
				self.target = tarpos.getPosition()
		course = self.getCourseTowards(self.target)'''
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def foundTarget(self):
		if self.found:
			return True
		print('checking, in greedy')
		vp = self.vehicle.getPosition()
		if self.area.inArea(vp):
			found = self.area.getCellForPos(vp).hasTarget()
		else:
			found = False
			
		self.found = found
		if(found):
			print('found target')
		return found
		
	def nextPos(self, vehicle, area):
		pos = vehicle.getPosition()
		if self.atPosition(vehicle, area, self.target): 
			#get new target
			print('get new target')
			cells = area.getAdjacentCells(pos)
			tarpos = cells[0]
			for cell in cells:
				#print(cell.toString())
				if cell.getProb() > tarpos.getProb():
					tarpos = cell
				self.target = tarpos.getPosition()
		print('Target ' + self.target.toString())
		return self.target
		
	def test(self):
		print('GreedyStrat')