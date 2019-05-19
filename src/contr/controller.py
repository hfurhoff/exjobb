from integration.integrationmanager import IntegrationManager
from simulationmodel.simulationmanager import SimulationManager
from util.observer import Observer
from util.log import Log

from dto.searchareadto import SearchareaDTO
from dto.searchdto import SearchDTO

import datetime

class Controller():

	instance = None
	simManager = SimulationManager()

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
		self.simManager = None
		self.simManager = SimulationManager()
		self.simManager.setupSimulation(premises)
		print('simulation set up')
		
	def startSimulation(self):
		self.simManager.startSimulation()
		print('ready to show simulation')
		
	def simulate(self, premises):
		self.simManager = SimulationManager()
		
		before = datetime.datetime.now()
		self.simManager.setupSimulation(premises)
		self.simManager.startSimulation()
		after = datetime.datetime.now()
		dto = self.getAckumulatedSearch()
		
		dto.addRunningTime(after - before)
		print('simulation done')
		
	def getAckumulatedSearch(self):
		return self.simManager.getAckumulatedSearch()
		
	def getLog(self):
		return self.simManager.getLog()
		
	def getStrategies(self):
		return self.simManager.getStrategies()
	
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
		
