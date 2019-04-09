from simulationmodel.searcher import Searcher
from dto.settings import Settings
from util.observer import Observer
from dto.searchareadto import SearchareaDTO

class SimulationManager():

	searcher = None
	premises = None

	def __init__(self, premises):
		self.setupSimulation(premises)
		
	def setupSimulation(self, premises):
		self.premises = premises
		self.searcher = Searcher(premises.getStrategy(), premises.getArea(), premises.getVehicle())
		
	def getSearcharea(self):
		return self.searcher.getSearcharea()
		
	def startSimulation(self):
		self.searcher.startSearch()
		
	def getAckumulatedSearch(self):
		return self.searcher.getAckumulatedSearch()
		
	def getLog(self):
		return self.searcher.getLog()
		
	def addObserver(self, obs):
		pass
	
	def removeObserver(self, obs):
		pass
