from abc import ABCMeta, abstractmethod
from dto.course import Course
from simulationmodel.searcharea import Searcharea
from dto.point import Point
from simulationmodel.vehicle import Vehicle
from simulationmodel.cell import Cell
from dto.point import Point
import numpy as np


class NavigationStrategy:
	__metaclass__ = ABCMeta

	vehicle = None
	area = None
		
	@abstractmethod
	def nextCourse(self, vehicle, area):
		pass
		
	@abstractmethod
	def nextPos(self, vehicle, area):
		pass
		
	def foundTarget(self):
		print('checking')
		vp = self.vehicle.getPosition()
		tp = self.area.getTarget()
		found = int(round(vp.getX())) == int(round(tp.getX())) and int(round(vp.getY())) == int(round(tp.getY()))
		if(found):
			print('found target')
		return found
		
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