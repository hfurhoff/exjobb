from dto.pose import Pose
from dto.course import Course
from dto.speed import Speed
from dto.turningradiusequation import TurningRadiusEquation
from util.log import Log
from dto.sensor import Sensor
from dto.point import Point
from dto.vehicledto import VehicleDTO
import numpy as np

class Vehicle():

	pose = None
	desiredHeading = None
	currentSpeed = None
	maxSpeed = None
	turningRadius = None
	log = None
	sensor = None

	def __init__(self, v):
		from dto.vehicledto import VehicleDTO
		self.pose = v.getPose()
		self.desiredHeading = self.pose.getOrientation()
		self.currentSpeed = v.getCurrentSpeed()
		self.maxSpeed = v.getMaxSpeed()
		self.turningRadius = v.getTurningRadius()
		self.sensor = v.getSensor()
		self.log = Log([self])
		
	def getTurningRadiusBasedOnCurrentSpeed(self):
		pass
		
	def moveToOrigo(self):
		self.pose.setPosition(Point(0, 0))
		self.updateLog()

	def latestLogEntry(self):
		return self.log.latestLogEntry()
		
	def sublog(self, logFrom, logTo):
		return self.log.sublog(logFrom, logTo)
		
	def logFrom(self, le):
		return self.log.getLogSince(le)
		
	def setCourseTowards(self, that):
		this = self.getPosition()
		dx = that.getX() - this.getX()
		dy = that.getY() - this.getY()
		deg = np.degrees(np.arctan2(dy, dx))
		course = (-(deg - 90) % 360) 
		self.desiredHeading = course
		self.pose = Pose(course, self.getPosition())
		
	def updatePose(self, numberOfTimesteps):
		for i in range(numberOfTimesteps):
			p = self.getPosition()
			hypo = self.currentSpeed
			course = np.radians((-self.pose.getOrientation()) + 90)
			dx = hypo * np.cos(course)
			dy = hypo * np.sin(course)
			x, y = p.getX(), p.getY()
			
			self.pose = Pose(self.pose.getOrientation(), Point(x + dx, y + dy))
			print(self.getPosition().toString())
			self.updateLog()
		
	def updateLog(self):
		self.log.update(VehicleDTO([self]))
		
	def getPose(self):
		return self.pose
		
	def getPosition(self):
		return self.pose.getPosition()
	
	def getMaxSpeed(self):
		return self.maxSpeed
		
	def getCurrentSpeed(self):
		return self.currentSpeed
		
	def getTurningRadius(self):
		return self.turningRadius
	
	def getSensor(self):
		return self.sensor
	
	def getLog(self):
		return self.log
		
	def atOrigo(self):
		p = self.getPosition()
		return int(p.getX()) == 0 and int(p.getY()) == 0