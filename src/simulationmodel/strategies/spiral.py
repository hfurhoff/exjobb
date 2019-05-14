from dto.course import Course
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.matrixmap import MatrixMap
from simulationmodel.cell import Cell
from dto.point import Point
from dto.sensor import Sensor
import numpy as np


class Spiral(NavigationStrategy):

	a1 = None
	turnsMade = -1
	aPrevious = 361
	wps = None

	def __init__(self):
		pass
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def nextPos(self, vehicle, area):
		#x(a) = rcos(a)
		#y(a) = rsin(a)
		#a = angle
		#increase spiral-radius by a constant * sensor-radius every lap
		pos = vehicle.getPosition()
		if self.wps == None:
			self.wps = []
			r = 0
			a = 0.0
			#a1 = (self.currAngle(pos) - 180) % 360
			turns = 0
			radiusIncreasePerTurn = vehicle.getSensor().getDiameter() * 0.9
			newWp = Point(0, 0)
			while area.inArea(newWp):
				turns = int(a / 360)
				a += 360 / (8 + 8 * turns)
				r = radiusIncreasePerTurn * (a / 360.0)
				x = r * np.cos(np.deg2rad(a))
				y = r * np.sin(np.deg2rad(a))
				newWp = Point(x, y).translate(pos.getX(), pos.getY())
				#if newWp.distTo(Point(0, 0).translate(pos.getX(), pos.getY())) > radiusIncreasePerTurn / 2.0:
				self.wps.append(newWp)
			self.target = self.wps.pop(0)
			
		if self.atPosition(vehicle, area, self.target): 
			#get new target
			self.wps.append(self.target)
			self.target = self.wps.pop(0)
			
		pos = vehicle.getPosition()
		desiredSpeed = pos.distTo(self.target) / float(vehicle.getTimestepLength())
		tr = vehicle.getTurningRadius()
		course = vehicle.getHeading()
		nextCourse = self.getCourseFromTo(self.target, self.wps[0])
		diff = (course - nextCourse) % 360
		steps = int(diff / tr) + 1
		desiredSpeed = desiredSpeed / steps
		vehicle.setDesiredSpeed(desiredSpeed)
		
		return self.target
		
	def currAngle(self, pos):
		return np.degrees(np.arccos(pos.getX() / pos.distTo(Point(0, 0)))) % 360
		
	def foundTarget(self):
		return self.area.foundTarget() or super(Spiral, self).foundTarget()
		
	def test(self):
		print('SpiralStrat')