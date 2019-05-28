from dto.course import Course

from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea
from simulationmodel.maps.quadtreemap import QuadtreeMap


class Quadtree_max(NavigationStrategy):

	def __init__(self):
		pass
		
	def makeArea(self, area, sensor, depth):
		return QuadtreeMap(area)
		
	def nextCourse(self, vehicle, area):
		nextPos = self.nextPos(vehicle, area)
		course = self.getCourseTowards(nextPos)
		return course
		
	def updateTarget(self):
		self.target = self.area.getMaxPos()
		self.targetCell = self.area.getCellForPos(self.target)
		
	def nextPos(self, vehicle, area):
		if self.atPosition(vehicle, area, self.target) or self.targetCell.getProb() * 2 < self.area.getMaxProb():
			self.updateTarget()
		return self.target
		
	def test(self):
		print('QuadtreeStrat')