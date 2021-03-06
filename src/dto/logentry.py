from dto.pose import Pose
from dto.speed import Speed
from dto.sensor import Sensor
import copy

class LogEntry():

	timestamp = None
	pose = None
	speed = None
	sensorUsed = None

	def __init__(self, v, time):
		self.timestamp = time
		self.pose = Pose(v.getHeading(), v.getPosition())
		self.speed = v.getCurrentSpeed()
		self.sensorUsed = v.getSensor()
		
	def getPose(self):
		return self.pose
	
	def getPosition(self):
		return self.pose.getPosition()
	
	def toString(self):
		return self.pose.toString()
		
	def getTimestamp(self):
		return self.timestamp
	
	def getSpeed(self):
		return self.speed
		
	def getSensor(self):
		return self.sensorUsed