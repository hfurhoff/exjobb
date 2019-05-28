from dto.course import Course
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.maps.coveragemap import CoverageMap
from simulationmodel.cell import Cell
from dto.point import Point
from dto.sensor import Sensor
from util.util import Util
import numpy as np


class Spiral(NavigationStrategy):

	a1 = None
	turnsMade = -1
	aPrevious = 361
	wps = None

	def __init__(self):
		pass
		
	def makeArea(self, area, sensor, depth):
		return CoverageMap(area)
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def nextPos(self, vehicle, area):
		pos = vehicle.getPosition()
		if self.wps == None:
			dia = vehicle.getSensor().getDiameter() * 0.9
			self.makeSpiral(dia)
		if self.atPosition(vehicle, area, self.target): 
			self.wps.append(self.target)
			self.target = self.wps.pop(0)
			
		desiredSpeed = pos.distTo(self.target) / float(vehicle.getTimestepLength())
		tr = vehicle.getTurningRadius()
		course = vehicle.getHeading()
		nextCourse = self.getCourseFromTo(pos, self.target)
		diff = abs(Util.unwrap(course - nextCourse))
		steps = int(diff / tr) + 1
		desiredSpeed = desiredSpeed / steps
		vehicle.setDesiredSpeed(desiredSpeed)
		
		return self.target
		
	def makeSpiral(self, dia):
		pos = self.vehicle.getPosition()
		self.wps = []
		r = 0
		a = 0.0
		turns = 0
		newWp = Point(0, 0)
		while self.area.inArea(newWp):
			turns = int(a / 360)
			a += 360 / (8 + 8 * turns)
			r = dia * (a / 360.0)
			x = r * np.cos(np.deg2rad(a))
			y = r * np.sin(np.deg2rad(a))
			newWp = Point(x, y).translate(pos.getX(), pos.getY())
			self.wps.append(newWp)
		self.target = self.wps.pop(0)
		
	def currAngle(self, pos):
		return np.degrees(np.arccos(pos.getX() / pos.distTo(Point(0, 0)))) % 360

	def localSearch(self, localSearch):
		dia = self.vehicle.getSensor().getDiameter() * 0.9
		self.makeSpiral(dia)
		super(Spiral, self).localSearch(localSearch)
		
	def test(self):
		print('SpiralStrat')