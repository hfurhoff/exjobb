from integration.dbhandler import DBHandler
from integration.settingsretriever import SettingsRetriever
from integration.rosintegrator import ROSintegrator
from dto.course import Course

class IntegrationManager():
	instance = None
	ros = None
	db = None
	sr = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if IntegrationManager.instance == None:
			IntegrationManager()
		return IntegrationManager.instance

	def __init__(self):
		""" Virtually private constructor. """
		if IntegrationManager.instance != None:
			raise Exception("This class is a singleton!")
		else:
			IntegrationManager.instance = self	
			
	def availableSettings(self):
		pass
		
	def availableLogs(self):
		pass
		
	def saveLog(self, log):
		pass
			
	def sendCourse(self):
		pass