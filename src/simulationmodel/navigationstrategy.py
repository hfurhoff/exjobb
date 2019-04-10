from abc import ABCMeta, abstractmethod
from dto.course import Course
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from dto.point import Point


class NavigationStrategy:
	__metaclass__ = ABCMeta

	vehicle = None
	area = None

	def __init__(self):
		pass
		
	@abstractmethod
	def nextCourse(self, vehicle, area):
		pass
		
	def foundTarget(self):
		print('checking')
		vp = self.vehicle.getPosition()
		tp = self.area.getTarget()
		#print(vp.toString() + ' ' + tp.toString())
		found = int(round(vp.getX())) == int(round(tp.getX())) and int(round(vp.getY())) == int(round(tp.getY()))
		if(found):
			print('found target')
		return found
		
	def setVehicleAndArea(self, vehicle, area):
		self.vehicle = vehicle
		self.area = area