from dto.pose import Pose
from dto.pdf import PDF
from dto.target import Target
from dto.logentry import LogEntry
from dto.point import Point
from dto.searchareadto import SearchareaDTO
from dto.celldto import CellDTO
import copy

class SearchDTO():

	initialState = None
	log = None
	changes = []
	
	def __init__(self, initialState):
		self.initialState = initialState
		self.log = None
		self.changes = []

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