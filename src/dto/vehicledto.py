from dto.pose import Pose
from dto.speed import Speed
from dto.turningradiusequation import TurningRadiusEquation
from dto.sensor import Sensor
import copy

class VehicleDTO():

	pose = None
	maxSpeed = None
	currentSpeed = None
	turningRadius = None
	sensor = None
	
	def __init__(self, args):
		if len(args) == 1:
			from simulationmodel.vehicle import Vehicle
			v = args[0]
			self.pose = v.getPose()
			self.currentSpeed = v.getCurrentSpeed()
			self.maxSpeed = v.getMaxSpeed()
			self.turningRadius = v.getTurningRadius()
			self.sensor = v.getSensor()
		else:
			self.pose = args[0]
			self.maxSpeed = args[1]
			self.currentSpeed = args[2]
			self.turningRadius = args[3]
			self.sensor = args[4]

	def getPose(self):
		return self.pose
	
	def getMaxSpeed(self):
		return self.maxSpeed
		
	def getCurrentSpeed(self):
		return self.currentSpeed
		
	def getTurningRadius(self):
		return self.turningRadius
	
	def getSensor(self):
		return self.sensor

	def getHeading(self):
		return self.pose.getOrientation()
		
	def getPosition(self):
		return self.pose.getPosition()