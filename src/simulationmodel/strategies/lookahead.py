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

	def __init__(self):
		pass
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def nextPos(self, vehicle, area):
		pos = vehicle.getPosition()
		if self.atPositionWithExtraMargin(vehicle, area, self.target): 
			#get new target
			sensor = vehicle.getSensor()
			d = int(self.depth * sensor.getRadius() + 1)
			print('-------------------------------------------------------------------')
			currentHeading = vehicle.getHeading()
			currentCell = area.getCellForPos(pos)
			targetCell = currentCell
			while not targetCell.getProb() > 0.0 and d < area.getCells():
				print('depth: ' + repr(d))
				cells = area.getAdjacentCells(pos, d)
				targetCell = cells[0]
				maxValue = self.calculateValue(vehicle, targetCell)
				for cell in cells:
					value = self.calculateValue(vehicle, cell)
					if value > maxValue and area.inSearchArea(cell.getPosition()):
						targetCell = cell
						maxValue = value
					self.target = targetCell.getPosition()
				d += int(sensor.getRadius() + 1)
			print('Target: ' + self.target.toString() + ', diff: ' + repr(currentHeading - self.getCourseFromTo(pos, targetCell.getPosition())))
			print('-------------------------------------------------------------------')
		return self.target
		
	def atPositionWithExtraMargin(self, vehicle, area, target):
		sensorRad = vehicle.getSensor().getRadius() * 0.6
		margin = sensorRad
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
		reward = cell.getProb()#np.power(cell.getProb() * 10, 3)
		steps = int(diff / tr) + 1
		cost = steps * 0.5
		'''reward = int(reward * 1000)
		cost = int(cost * 1000)'''
		value = reward# / cost) + reward
		#print('value: ' + repr(value) + '\treward: ' + repr(reward) + '\tcost: ' + repr(cost) + '\tpos: ' + cpos.toString())
		#print('diff: ' + repr(diff) + ', steps: ' + repr(steps) + ', tr: ' + repr(tr))
		#print('diff: ' + repr(diff) + ', prob: ' + repr(cell.getProb()) + ', value: ' + repr(value))
		return value
		
	def setDepth(self, depth):
		self.depth = depth
		
	def test(self):
		print('LookaheadStrat')