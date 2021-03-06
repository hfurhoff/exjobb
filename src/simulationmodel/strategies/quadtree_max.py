from dto.course import Course

from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.maps.quadtreemap import QuadtreeMap


class Quadtree_max(NavigationStrategy):

	def __init__(self):
		pass
		
	def makeArea(self, area, sensor, depth):
		return QuadtreeMap(area, sensor)
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def updateTarget(self, area):
		self.target = area.getMaxPos()
		self.targetCell = area.getCellForPos(self.target)
		
	def nextPos(self, vehicle, area):
		if self.atPosition(vehicle, area, self.target):
			self.updateTarget(area)
		return self.target
		
	def test(self):
		print('QuadtreeStrat')