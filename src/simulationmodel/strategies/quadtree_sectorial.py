from dto.course import Course

from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.maps.quadtreemap import QuadtreeMap


class Quadtree_sectorial(NavigationStrategy):

	def __init__(self):
		pass
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def nextPos(self, vehicle, area)
		return self.target
		
	def test(self):
		print('QuadtreeStrat')