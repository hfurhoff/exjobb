from abc import ABCMeta, abstractmethod
from dto.course import Course
from simulationmodel.searcharea import Searcharea
from dto.point import Point
from simulationmodel.vehicle import Vehicle
from simulationmodel.cell import Cell
from dto.point import Point
import numpy as np
from numpy import random


class NavigationStrategy:
	__metaclass__ = ABCMeta

	vehicle = None
	area = None
	target = Point(0, 0)
	localSearch = False
		
	@abstractmethod
	def nextCourse(self, vehicle, area):
		pass
		
	@abstractmethod
	def nextPos(self, vehicle, area):
		pass

	@abstractmethod
	def makeArea(self, area, sensor, depth):
		pass
		
	def setVehicleAndArea(self, vehicle, area):
		self.vehicle = vehicle
		self.area = area
		
	def getCourseTowards(self, that):
		this = self.vehicle.getPosition()
		return self.getCourseFromTo(this, that)
		
	def getCourseFromTo(self, this, that):
		dx = that.getX() - this.getX()
		dy = that.getY() - this.getY()
		deg = np.degrees(np.arctan2(dy, dx))
		course = self.degToNav(deg) 
		return course
		
	def degToNav(self, deg):
		return (-(deg - 90)) % 360
		
	def navToDeg(self, nav):
		return ((-nav) + 90) % 360
		
	def atPosition(self, vehicle, area, target):
		margin = area.getMargin()
		tarx = target.getX()
		tary = target.getY()
		pos = vehicle.getPosition()
		posx = pos.getX()
		posy = pos.getY()
		correctx = posx > tarx - margin and posx < tarx + margin
		correcty = posy > tary - margin and posy < tary + margin
		return correctx and correcty
		
	def updateSpeed(self, target):
		vehicle = self.vehicle
		desiredCourse = self.getCourseTowards(target)
		tr = vehicle.getTurningRadius()
		pos = vehicle.getPosition()
		desiredSpeed = pos.distTo(target) / float(vehicle.getTimestepLength())
		course = vehicle.getHeading()
		diff = (course - desiredCourse) % 360
		steps = int(diff / tr) + 1
		desiredSpeed = desiredSpeed / steps
		vehicle.setDesiredSpeed(desiredSpeed)
		
	def getTarget(self):
		return self.target
		
	def localSearch(self, localSearch):
		self.localSearch = localSearch
		self.target = self.vehicle.getPosition()