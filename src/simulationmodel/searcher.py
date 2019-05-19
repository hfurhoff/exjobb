from util.observer import Observer
from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.strategies.greedy import Greedy
from simulationmodel.strategies.spiral import Spiral
from simulationmodel.strategies.lookahead import Lookahead

from simulationmodel.searcharea import Searcharea 
from simulationmodel.maps.quadtreemap import QuadtreeMap
from simulationmodel.maps.coveragemap import CoverageMap
from simulationmodel.maps.matrixmap import MatrixMap
from simulationmodel.maps.sensormap import SensorMap

from simulationmodel.vehicle import Vehicle

from dto.searchareadto import SearchareaDTO
from dto.searchdto import SearchDTO
from dto.settings import Settings
from dto.sensor import Sensor
from dto.point import Point

from pydoc import locate
import numpy as np

class Searcher():

	strategy = None
	area = None
	vehicle = None
	observers = None
	firstEntry = None
	lastEntry = None
	ackumulatedSearch = None
	dto = None

	def __init__(self, strategy, area, vehicle, depth):
		str = strategy
		classname = str[:-(len(str) - 1)].upper() + str[1:]
		mod = __import__('simulationmodel.strategies.' + str, fromlist=[classname])
		klass = getattr(mod, classname)
		self.strategy = klass()
		sensor = vehicle.getSensor()
		'''bigDia = area.bigDia()
		gs = int((2 * bigDia) / 20.0) + 1
		if gs < int(sensor.getRadius()):
			gs = int(sensor.getRadius())
		if gs < 1:
			gs = 1
		area.setGridsize(gs)'''
		if isinstance(self.strategy, Greedy):
			self.area = SensorMap(area, sensor)
		elif isinstance(self.strategy, Lookahead):
			self.strategy.setDepth(depth)
			self.area = MatrixMap(area)
		elif isinstance(self.strategy, Spiral):
			self.area = CoverageMap(area)
		else:
			self.area = QuadtreeMap(area)
		self.vehicle = Vehicle(vehicle)
		self.lastEntry = self.vehicle.latestLogEntry()
		self.firstEntry = self.lastEntry
		self.strategy.test()
		dto = SearchareaDTO([self.area])
		dto.setZeroData()
		self.dto = SearchDTO(dto, classname, sensor.getRadius())
		self.ackumulatedSearch = [dto]
		
	def getSearcharea(self):
		sa = SearchareaDTO([self.area])
		return sa
		
	def startSearch(self):
		i = 0
		self.updateLatestLogEntry()
		self.strategy.setVehicleAndArea(self.vehicle, self.area)
		foundTarget = False
		nextPos = Point(0, 0)
		course = self.strategy.getCourseTowards(nextPos)
		self.vehicle.setInitialCourse(course)
		#print(self.vehicle.getPosition().toString())
		while not self.vehicle.near(nextPos):
			self.vehicle.updatePose(1)
			i += 1
			#print(repr(i))
			foundTarget = self.strategy.foundTarget()
			if foundTarget:
				break
		
		showProb = False
		self.updateSearch(showProb)
		if foundTarget:
			self.setVehicleAtTarget()
			return		

		currentSpeed = self.vehicle.getCurrentSpeed()
		self.vehicle.setDesiredSpeed(0)
		while not self.vehicle.atPosition(nextPos) and not int(round(currentSpeed)) == 0:
			self.vehicle.updatePose(1)
			i += 1
			#print(repr(i))
			currentSpeed = self.vehicle.getCurrentSpeed()
			foundTarget = self.strategy.foundTarget()
			if foundTarget:
				break

		if foundTarget:
			self.vehicle.setDesiredSpeed(self.vehicle.getMaxSpeed())
			self.setVehicleAtTarget()
			return		

		self.vehicle.updatePose(5)
		i += 5
		#print(repr(i))
		self.updateSearch(showProb)
		
		showProb = True
		self.dto.showProb(SearchareaDTO([self.area]))
		
		while not foundTarget:
			if isinstance(self.strategy, Greedy):
				tmpPos = self.strategy.nextPos(self.vehicle, self.area)
				course = self.strategy.getCourseTowards(tmpPos)
				if not tmpPos.equals(nextPos):
					foundTarget = self.strategy.foundTarget()
					self.updateSearch(showProb)
					nextPos = tmpPos
					if not foundTarget:
						self.strategy.updateSpeed(tmpPos)
						self.vehicle.updatePose(1)
				elif False and self.vehicle.near(tmpPos):
					#print('near')
					self.vehicle.setPosition(tmpPos)
					self.vehicle.updateLog()
					self.updateSearch(showProb)
					foundTarget = self.strategy.foundTarget()
				else:
					self.vehicle.setCourse(course)
					self.strategy.updateSpeed(tmpPos)
					self.vehicle.updatePose(1)
			else:
				course = self.strategy.nextCourse(self.vehicle, self.area)
				self.vehicle.setCourse(course)
				if not isinstance(self.strategy, Spiral):
					nextPos = self.strategy.getTarget()
					self.strategy.updateSpeed(nextPos)
				self.vehicle.updatePose(1)
				self.updateSearch(showProb)
				foundTarget = self.strategy.foundTarget()
			i += 1
			#print(repr(i))
		self.setVehicleAtTarget()
		
	def setVehicleAtTarget(self):
		target = self.area.getTarget()
		while not self.strategy.atPosition(self.vehicle, self.area, target):
			desiredCourse = self.strategy.getCourseTowards(target)
			self.vehicle.setCourse(desiredCourse)
			self.strategy.updateSpeed(target)
			self.vehicle.updatePose(1)
		self.vehicle.setPosition(target)
		self.vehicle.updateLog()
		self.updateSearch(False)
		self.dto.setEndState(SearchareaDTO([self.area]))
		
	def updateSearch(self, showProb):
		sublog = self.vehicle.logFrom(self.lastEntry)
		data = None
		if not showProb:
			if self.strategy.foundTarget():
				data = self.area.updateSearchBasedOnLog(sublog, showProb, self.area.getTarget())
				data.append([])
			else:
				data = self.area.updateSearchBasedOnLog(sublog, showProb, Point(0, 0))
		else:
			data = self.area.updateSearchBasedOnLog(sublog, showProb, None)
		for changes in data:
			self.dto.appendChanges(changes)
		self.updateLatestLogEntry()
		
	def updateLatestLogEntry(self):
		self.lastEntry = self.vehicle.latestLogEntry()
		
	def getAckumulatedSearch(self):
		self.dto.addLog(self.getLog())
		return self.dto
		
	def getLog(self):
		return self.vehicle.getLog()
		
	def addObserver(self, obs):
		pass
	
	def removeObserver(self, obs):
		pass
		
	def notifyObservers(self, event):
		pass
