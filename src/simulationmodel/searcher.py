from util.observer import Observer
from dto.settings import Settings
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.searcharea import Searcharea 
from simulationmodel.vehicle import Vehicle
from dto.event import Event
from dto.searchareadto import SearchareaDTO
from simulationmodel.matrixmap import MatrixMap
from dto.point import Point

from pydoc import locate

class Searcher():

	strategy = None
	area = None
	vehicle = None
	observers = None
	firstEntry = None
	lastEntry = None
	ackumulatedSearch = None

	def __init__(self, strategy, area, vehicle):
		str = strategy
		classname = str[:-(len(str) - 1)].upper() + str[1:]
		mod = __import__('simulationmodel.strategies.' + str, fromlist=[classname])
		klass = getattr(mod, classname)
		self.strategy = klass()
		self.area = MatrixMap(area)
		self.vehicle = Vehicle(vehicle)
		self.lastEntry = self.vehicle.latestLogEntry()
		self.firstEntry = self.lastEntry
		self.strategy.test()
		self.ackumulatedSearch = []
		
	def getSearcharea(self):
		sa = SearchareaDTO([self.area])
		return sa
		
	def startSearch(self):
		le = self.vehicle.latestLogEntry()
		self.strategy.setVehicleAndArea(self.vehicle, self.area)
		foundTarget = False
		self.vehicle.setCourseTowards(Point(0, 0))
		print(self.vehicle.getPosition().toString())
		while (not self.vehicle.atOrigo()) and (not foundTarget):
			self.vehicle.updatePose(1)
			foundTarget = self.strategy.foundTarget()

		sublog = self.vehicle.logFrom(le)
		data = self.area.updateSearchBasedOnLog(sublog)
		#self.ackumulatedSearch.append(data[-1])
		for sa in data:
			self.ackumulatedSearch.append(sa)
		if(foundTarget):
			return 1
		
	def getAckumulatedSearch(self):
		return self.ackumulatedSearch
		
	def addObserver(self, obs):
		pass
	
	def removeObserver(self, obs):
		pass
		
	def notifyObservers(self, event):
		pass
