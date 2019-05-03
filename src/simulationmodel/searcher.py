from util.observer import Observer
from dto.settings import Settings
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.strategies.greedy import Greedy
from simulationmodel.searcharea import Searcharea 
from simulationmodel.vehicle import Vehicle
from dto.event import Event
from dto.searchareadto import SearchareaDTO
from simulationmodel.matrixmap import MatrixMap
from simulationmodel.sensormap import SensorMap
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
		if isinstance(self.strategy, Greedy):
			area.setGridsize(vehicle.getSensor())
			self.area = SensorMap(area)
		else:
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
		nextPos = Point(0, 0)
		self.vehicle.setCourseTowards(nextPos)
		print(self.vehicle.getPosition().toString())
		while not self.vehicle.atPosition(nextPos):
			self.vehicle.updatePose(1)
			foundTarget = self.strategy.foundTarget()
			if foundTarget:
				break
		
		if foundTarget:
			self.setVehicleAtTarget()
			return
		
		showProb = False
		self.updateSearch(showProb)
		showProb = True
		i = 0
		while not foundTarget and i < 200:
			print(repr(i))
			tmpPos = self.strategy.nextPos(self.vehicle, self.area)
			course = self.strategy.getCourseTowards(tmpPos)
			print(tmpPos.toString())
			if not tmpPos.equals(nextPos):
				foundTarget = self.strategy.foundTarget()
				self.updateSearch(showProb)
				nextPos = tmpPos
			elif self.vehicle.near(tmpPos):
				self.vehicle.setPosition(tmpPos)
				self.vehicle.updateLog()
				self.updateSearch(showProb)
				foundTarget = self.strategy.foundTarget()
			else:
				self.vehicle.setCourse(course)
				self.vehicle.updatePose(1)
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
