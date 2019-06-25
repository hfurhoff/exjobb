from util.observer import Observer

from simulationmodel.navigationstrategy import NavigationStrategy
from simulationmodel.strategies.greedy import Greedy

from simulationmodel.searcharea import Searcharea 
from simulationmodel.vehicle import Vehicle

from dto.searchareadto import SearchareaDTO
from dto.searchdto import SearchDTO
from dto.settings import Settings
from dto.sensor import Sensor
from dto.point import Point

from pydoc import locate
from numpy import random
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
	sensor = None
	
	def __init__(self, strategy, area, vehicle, depth):
		str = strategy
		classname = str[:-(len(str) - 1)].upper() + str[1:]
		mod = __import__('simulationmodel.strategies.' + str, fromlist=[classname])
		klass = getattr(mod, classname)
		self.strategy = klass()
		sensor = vehicle.getSensor()
		self.sensor = sensor
		self.area = self.strategy.makeArea(area, sensor, depth)
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
		while not self.vehicle.near(nextPos):
			self.vehicle.updatePose(1)
			foundTarget = self.foundTarget() and self.strongConnection()
			if foundTarget:
				break
		
		showProb = False
		self.updateSearch(showProb)
		if foundTarget:
			self.moveVehicleTowardsTarget()
			return

		currentSpeed = self.vehicle.getCurrentSpeed()
		self.vehicle.setDesiredSpeed(0)
		while not self.vehicle.atPosition(nextPos) and not int(round(currentSpeed)) == 0:
			self.vehicle.updatePose(1)
			currentSpeed = self.vehicle.getCurrentSpeed()
			foundTarget = self.foundTarget() and self.strongConnection()
			if foundTarget:
				break

		if foundTarget:
			self.vehicle.setDesiredSpeed(self.vehicle.getMaxSpeed())
			self.moveVehicleTowardsTarget()
			return		

		self.vehicle.updatePose(5)
		self.updateSearch(showProb)
		
		showProb = True
		self.dto.showProb(SearchareaDTO([self.area]))
		
		while not foundTarget:
			if isinstance(self.strategy, Greedy):
				tmpPos = self.strategy.nextPos(self.vehicle, self.area)
				course = self.strategy.getCourseTowards(tmpPos)
				if not tmpPos.equals(nextPos):
					foundTarget = self.foundTarget()
					self.updateSearch(showProb)
					nextPos = tmpPos
					if not foundTarget:
						self.strategy.updateSpeed(tmpPos)
						self.vehicle.updatePose(1)
				else:
					self.vehicle.setCourse(course)
					self.strategy.updateSpeed(tmpPos)
					self.vehicle.updatePose(1)
					if self.foundTarget() and self.strongConnection():
						break
			else:
				course = self.strategy.nextCourse(self.vehicle, self.area)
				self.vehicle.setCourse(course)
				if not self.area.isCoverage():
					nextPos = self.strategy.getTarget()
					self.strategy.updateSpeed(nextPos)
				self.vehicle.updatePose(1)
				self.updateSearch(showProb)
				foundTarget = self.foundTarget()
		self.moveVehicleTowardsTarget()
		
	def moveVehicleTowardsTarget(self):
		self.strategy.localSearch(True)
		showProb = True
		while not self.strongConnection():
			if self.foundTarget():
				self.area.raiseNearby(self.sensor, self.vehicle.getPosition())
			course = self.strategy.nextCourse(self.vehicle, self.area)
			self.vehicle.setCourse(course)
			if not self.area.isCoverage():
				nextPos = self.strategy.getTarget()
				self.strategy.updateSpeed(nextPos)
			self.vehicle.updatePose(1)
			self.updateSearch(showProb)
		target = self.area.getTarget()
		while not self.strategy.atPosition(self.vehicle, self.area, target):
			desiredCourse = self.strategy.getCourseTowards(target)
			self.vehicle.setCourse(desiredCourse)
			self.strategy.updateSpeed(target)
			self.vehicle.updatePose(1)
		self.vehicle.setPosition(target)
		self.vehicle.updateLog()
		if not self.area.isCoverage():
			showProb = False
		self.updateSearch(showProb)
		self.dto.setEndState(SearchareaDTO([self.area]))
		
	def updateSearch(self, showProb):
		sublog = self.vehicle.logFrom(self.lastEntry)
		data = None
		if not showProb:
			if self.foundTarget():
				data = self.area.updateSearchBasedOnLog(sublog, showProb, self.area.getTarget())
				data.append([])
			else:
				data = self.area.updateSearchBasedOnLog(sublog, showProb, Point(0, 0))
		else:
			data = self.area.updateSearchBasedOnLog(sublog, showProb, None)
		for changes in data:
			self.dto.appendChanges(changes)
		self.updateLatestLogEntry()
		
	def foundTarget(self):
		vp = self.vehicle.getPosition()
		sensor = self.vehicle.getSensor()
		targetDist = vp.distTo(self.area.getTarget())
		probOfTargetDetection = sensor.probabilityOfDetection(targetDist)
		rand = random.random_sample()
		found = False
		if rand < probOfTargetDetection:
			found = True
		else:
			tp = self.area.getTarget()
			tpx, tpy = self.area.posToCellIndex(tp)
			vpx, vpy = self.area.posToCellIndex(vp)
			found = vpx == tpx and vpy == tpy
		if isinstance(self.strategy, Greedy) and not self.strongConnection():
			found = False
		return found
		
	def strongConnection(self):
		vp = self.vehicle.getPosition()
		targetDist = vp.distTo(self.area.getTarget())
		'''print('dist from target: ' + repr(targetDist))
		print('sensor radius: ' + repr(self.sensor.getRadius()))'''
		if targetDist < self.sensor.getRadius():
			return True
		else:
			return False
		
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
