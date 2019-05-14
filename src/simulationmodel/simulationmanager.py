from simulationmodel.searcher import Searcher
from dto.settings import Settings
from util.observer import Observer
from dto.searchareadto import SearchareaDTO
import os
import re

class SimulationManager():

	searcher = None
	premises = None

	def __init__(self):
		self.searcher = None
		self.premises = None
		
	def setupSimulation(self, premises):
		self.premises = premises
		self.searcher = Searcher(premises.getStrategy(), premises.getArea(), premises.getVehicle(), premises.getLookaheadDepth())
		
	def getSearcharea(self):
		return self.searcher.getSearcharea()
		
	def startSimulation(self):
		self.searcher.startSearch()
		
	def getAckumulatedSearch(self):
		return self.searcher.getAckumulatedSearch()
		
	def getLog(self):
		return self.searcher.getLog()
		
	def getStrategies(self):
		strats = []
		for item in sorted(os.listdir("../simulationmodel/strategies")):
			if(re.findall("^_|.pyc$", item)):
				pass
			else:
				strats.append(item)
		return strats
		
	def addObserver(self, obs):
		pass
	
	def removeObserver(self, obs):
		pass
