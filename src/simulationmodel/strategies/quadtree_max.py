from dto.course import Course

from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.maps.quadtreemap import QuadtreeMap


class Quadtree_max(NavigationStrategy):

	def __init__(self):
		pass
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def nextPos(self, vehicle, area):
		if self.atPosition(vehicle, area, self.target):
			#print('--------------------------------------------------')
			#print('Previous target: ' + self.target.toString())
			self.target = area.getMaxPos()
			#print('New target: ' + self.target.toString())
		return self.target
		
	def test(self):
		print('QuadtreeStrat')