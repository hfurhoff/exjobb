from dto.pose import Pose
from dto.pdf import PDF
from dto.target import Target
from dto.logentry import LogEntry
from dto.point import Point
from dto.searchareadto import SearchareaDTO
from dto.celldto import CellDTO
import copy
import time
import datetime

class SearchDTO():

	initialState = None
	endState = None
	log = None
	changes = []
	name = None
	logLengthAdded = False
	runTime = None
	runTimeStr = ''
	strategyName = ''
	
	def __init__(self, initialState, classname, sensorRange):
		self.initialState = initialState
		self.log = None
		self.changes = []
		self.strategyName = classname
		self.name = ''
		self.name = self.name + classname[:2] + classname[-2:] 
		self.name = self.name + ', sensRange: ' + repr(sensorRange)
		self.name = self.name + ', tPos: ' + self.getTarget().toString() 
		self.name = self.name + ', HxW: ' + repr(self.getHeight()) + 'x' + repr(self.getWidth())
		self.name = self.name + ', gs: ' + repr(round(self.getGridsize(), 2)) + '\t\t'

	def addLog(self, log):
		self.log = log
		
	def getLog(self):
		return self.log
	
	def len(self):
		return len(self.changes)
		
	def getTarget(self):
		return self.initialState.getTarget()
		
	def getHalfSideLength(self):
		return self.initialState.getHalfSideLength()
		
	def getWidth(self):
		return self.initialState.getWidth()
		
	def getHeight(self):
		return self.initialState.getHeight()
		
	def getData(self):
		data = copy.deepcopy(self.initialState.getData())
		return data
		
	def getChange(self, i):
		return self.changes[i]
		
	def getChangeFromTo(self, i, j):
		return self.changes[i:j]
		
	def appendChanges(self, changes):
		self.changes.append(changes)
		
	def showProb(self, sa):
		changes = self.dataDiff(self.initialState, sa)
		for change in changes:
			self.changes[-1].append(change)
		
	def dataDiff(self, oldState, newState):
		oldData = oldState.getData()
		newData = newState.getData()
		changes = []
		for y in range(len(oldData)):
			for x in range(len(oldData)):
				if not oldData[y][x] == newData[y][x]:
					changes.append(CellDTO(newData[y][x], x, y, self.cellIndexToPos(x, y)))
		return changes
		
	def getGridsize(self):
		return self.initialState.getGridsize()
		
	def cellIndexToPos(self, xindex, yindex):
		dy = yindex * self.getGridsize()
		dx = xindex * self.getGridsize()
		y = dy - self.getHalfSideLength()
		x = dx - self.getHalfSideLength()
		return Point(x, y)

	def isCoverage(self):
		return self.initialState.isCoverage()
		
	def setEndState(self, endState):
		self.endState = endState
		
	def getEndState(self):
		return self.endState
		
	def toString(self):
		if self.log == None or self.logLengthAdded == True:
			return self.name
		else:
			name = 'seconds: ' + repr(self.log.length()) + ', ' + self.name
			self.name = name
			self.logLengthAdded = True
			return self.name
			
	def addRunningTime(self, runTime):
		self.runTime = runTime
		self.runTimeMS = runTime.microseconds
		self.runTimeS = runTime.seconds
		self.runTimeStr = ''
		ms = runTime.microseconds
		microStr = str(ms).rstrip("0") or "0"
		secs = runTime.seconds
		secondStr = str(secs % 60)
		minuteStr = str(secs / 60)
		self.runTimeStr = ''
		self.runTimeStr = minuteStr + ':' + secondStr + '.' + microStr
		self.name = 'procTime: ' + self.runTimeStr + ', ' + self.name
		
	def getRTMS(self):
		return self.runTimeMS
		
	def getRTS(self):
		return self.runTimeS
		
	def getStrategyName(self):
		return self.strategyName