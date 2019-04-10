from dto.course import Course
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.matrixmap import MatrixMap
from simulationmodel.cell import Cell
from dto.point import Point
import numpy as np


class Greedy(NavigationStrategy):

	def __init__(self):
		pass
		
	def nextCourse(self, vehicle, area):
		pos = vehicle.getPosition()
		cells = area.getAdjacentCells(pos)
		'''max = cells[0]
		print('from getAdjacentCells')
		for cell in cells:
			print(repr(cell[0]) + ' ' + repr(cell[1]) + ' ' + repr(cell[2]))
			if cell[0] > max[0]:
				max = cell
		print('max ' + repr(max[0]) + ' ' + repr(max[1]) + ' ' + repr(max[2]))
		
		#print(cell.getPosition().toString())
		dx = max[1] - pos.getX()
		dy = max[2] - pos.getY()'''
		max = cells[0]
		#print('from getAdjacentCells ' + pos.toString())
		for cell in cells:
			#print(repr(cell.getProb()) + ' ' + cell.getPosition().toString())
			if cell.getProb() > max.getProb():
				max = cell
		#print('max ' + repr(max.getProb()) + ' ' + max.getPosition().toString())
		
		#print(max.getPosition().toString() + '  ' + pos.toString())
		dx = max.getX() - pos.getX()
		dy = max.getY() - pos.getY()
		deg = np.degrees(np.arctan2(dy, dx))
		course = (-(deg - 90) % 360) 
		#print(repr(course))
		return course
		
	def test(self):
		print('GreedyStrat')