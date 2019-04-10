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
		dto = SearchareaDTO([self.area])
		dto.setZeroData()
		self.ackumulatedSearch = [dto]
		
	def getSearcharea(self):
		sa = SearchareaDTO([self.area])
		return sa
		
	def startSearch(self):
		self.updateLatestLogEntry()
		self.strategy.setVehicleAndArea(self.vehicle, self.area)
		foundTarget = False
		self.vehicle.setCourseTowards(Point(0, 0))
		print(self.vehicle.getPosition().toString())
		while (not self.vehicle.atPosition(Point(0, 0))) and (not foundTarget):
			self.vehicle.updatePose(1)
			foundTarget = self.strategy.foundTarget()
		
		if foundTarget:
			self.setVehicleAtTarget()
			return
		
		self.updateSearch(False)
		i = 0
		while not self.strategy.foundTarget() and i < 100:
			nextCourse = self.strategy.nextCourse(self.vehicle, self.area)
			self.vehicle.setCourse(nextCourse)
			self.vehicle.updatePose(1)
			self.updateSearch(True)
			#i = i + 1
		
		self.setVehicleAtTarget()
		
	def setVehicleAtTarget(self):
		target = self.area.getTarget()
		self.vehicle.setPosition(target)
		self.vehicle.updateLog()
		self.updateSearch(True)
		
	def updateSearch(self, showProb):
		sublog = self.vehicle.logFrom(self.lastEntry)
		data = self.area.updateSearchBasedOnLog(sublog, showProb)
		for sa in data:
			self.ackumulatedSearch.append(sa)
		self.updateLatestLogEntry()
		
	def updateLatestLogEntry(self):
		self.lastEntry = self.vehicle.latestLogEntry()
		
	def getAckumulatedSearch(self):
		return self.ackumulatedSearch
		
	def getLog(self):
		return self.vehicle.getLog()
		
	def addObserver(self, obs):
		pass
	
	def removeObserver(self, obs):
		pass
		
	def notifyObservers(self, event):
		pass
