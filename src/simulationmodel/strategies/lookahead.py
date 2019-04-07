from dto.course import Course
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.vehicle import Vehicle
from simulationmodel.searcharea import Searcharea


class Lookahead(NavigationStrategy):

	area = None
	depth = None

	def __init__(self):
		pass
		
	def nextCourse(self, vehicle, area):
		pass
		
	def test(self):
		print('LookaheadStrat')