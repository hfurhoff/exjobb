from dto.logentry import LogEntry
import time
import copy

class Log():

	entries = None
	created = None
	vehicle = None
	
	def __init__(self, args):
		self.entries = []
		self.created = time.time()
		self.vehicle = args[0]
		if len(args) > 1:
			self.entries = copy.copy(args[1])
		else:
			self.update(self.vehicle)
	
	def getLogSince(self, entry):
		subentries = self.entries[self.entries.index(entry):]
		return Log([self.vehicle, subentries])
		
	def update(self, v):
		self.entries.append(LogEntry(v, time.time()))

	def latestLogEntry(self):
		return self.entries[-1]
		
	def get(self, i):
		return self.entries[i]
		
	def sublog(self, logFrom, logTo):
		subentries = self.entries[self.entries.index(logFrom):self.entries.index(logTo) + 1]
		return Log([self.vehicle, subentries])
		
	def length(self):
		return len(self.entries)
		
	def toString(self):
		s = []
		for i in range(len(self.entries)):
			le = self.entries[i]
			s.append('Entry ' + repr(i) + ': ' + le.toString())
		return s
		
	def getTimestepLength(self):
		return self.vehicle.getTimestepLength()