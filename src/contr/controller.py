from integration.integrationmanager import IntegrationManager
from simulationmodel.simulationmanager import SimulationManager
from util.observer import Observer
from util.log import Log
from dto.searchareadto import SearchareaDTO

class Controller():

	instance = None
	simManager = None
	im = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if Controller.instance == None:
			Controller()
		return Controller.instance

	def __init__(self):
		""" Virtually private constructor. """
		if Controller.instance != None:
			raise Exception("This class is a singleton!")
		else:
			Controller.instance = self	
			
	def getSearcharea(self):
		return self.simManager.getSearcharea()
			
	def addSimMngr(self, simMangr):
		pass
		
	def setupSimulation(self, premises):
		self.simManager = SimulationManager(premises)
		
	def startSimulation(self):
		self.simManager.startSimulation()
		
	def getAckumulatedSearch(self):
		return self.simManager.getAckumulatedSearch()
		
	def getLog(self):
		return self.simManager.getLog()
	
	def addObserver(self, obs):
		pass
		
	def removeObserver(self, obs):
		pass
		
	def availableSettings(self):
		pass
		
	def availableLogs(self):
		pass
		
	def saveLog(self, log):
		pass
		
