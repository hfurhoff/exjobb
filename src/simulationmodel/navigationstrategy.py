from abc import ABCMeta, abstractmethod
from dto.course import Course
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea


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
		vp = self.vehicle.getPosition()
		tp = self.area.getTarget()
		return vp.equals(tp)
		
	def setVehicleAndArea(self, vehicle, area):
		self.vehicle = vehicle
		self.area = area