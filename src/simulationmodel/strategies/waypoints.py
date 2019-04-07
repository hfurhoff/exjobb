from dto.course import Course
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from dto.point import Point


class Waypoints(NavigationStrategy):

	area = None
	path = None

	def __init__(self, path):
		pass
		
	def nextCourse(self, vehicle, area):
		pass
		
	def test(self):
		print('WaypointStrat')