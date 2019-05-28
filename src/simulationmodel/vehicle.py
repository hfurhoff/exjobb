from dto.pose import Pose
from dto.course import Course
from dto.speed import Speed
from dto.turningradiusequation import TurningRadiusEquation
from util.log import Log
from util.util import Util
from dto.sensor import Sensor
from dto.point import Point
from dto.vehicledto import VehicleDTO
import numpy as np

class Vehicle():

	pose = None #TODO:convert to lat/long
	desiredHeading = None
	currentSpeed = None #m/s
	desiredSpeed = None
	maxSpeed = None
	turningRadius = None #degrees/second
	acceleration = None #m/s2
	log = None
	sensor = None
	timestepLength = 1 #seconds
	initialPosition = None

	def __init__(self, v):
		from dto.vehicledto import VehicleDTO
		self.pose = v.getPose()
		self.initialPosition = self.getPosition()
		self.desiredHeading = self.pose.getOrientation()
		self.currentSpeed = v.getCurrentSpeed()
		self.desiredSpeed = self.currentSpeed
		self.maxSpeed = v.getMaxSpeed()
		self.turningRadius = v.getTurningRadius()
		self.acceleration = self.maxSpeed / 2.0
		self.sensor = v.getSensor()
		self.log = Log([self])
		
	def latestLogEntry(self):
		return self.log.latestLogEntry()
		
	def sublog(self, logFrom, logTo):
		return self.log.sublog(logFrom, logTo)
		
	def logFrom(self, le):
		return self.log.getLogSince(le)
		
	def setInitialCourse(self, course):
		self.desiredHeading = course
		self.pose = Pose(course, self.getPosition())
		
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
			currentHeading = self.getHeading()
			if currentHeading != self.desiredHeading:
				diff = Util.unwrap(self.desiredHeading - currentHeading)
				sign = diff / abs(diff)
				if abs(diff) > self.turningRadius:
					currentHeading = currentHeading + sign * self.turningRadius
				else:
					currentHeading = self.desiredHeading % 360
					
			if self.currentSpeed != self.desiredSpeed:
				diff = self.desiredSpeed - self.currentSpeed
				if abs(diff) > self.acceleration:
					sign = diff / abs(diff)
					self.currentSpeed = self.currentSpeed + sign * self.acceleration
				else:
					self.currentSpeed = self.desiredSpeed
			
			course = np.radians((-currentHeading) + 90)
			hypo = self.currentSpeed * self.timestepLength
			dx = hypo * np.cos(course)
			dy = hypo * np.sin(course)
			x, y = p.getX(), p.getY()
			
			self.pose = Pose(currentHeading % 360, Point(x + dx, y + dy))
			self.updateLog()
		
	def updateLog(self):
		self.log.update(VehicleDTO([self]))
		
	def getPose(self):
		return Pose(self.getHeading(), self.getPosition())
		
	def getPosition(self):
		pos = self.pose.getPosition()
		return Point(pos.getX(), pos.getY())
	
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
		
	def atPosition(self, p):
		pos = self.getPosition()
		return int(round(p.getX())) == int(round(pos.getX())) and int(round(p.getY())) == int(round(pos.getY()))
		
	def getTimestepLength(self):
		return self.timestepLength
		
	def setPosition(self, p):
		self.pose = Pose(self.pose.getOrientation(), p)
		
	def setCourse(self, course):
		self.desiredHeading = course
		
	def getHeading(self):
		return self.pose.getOrientation()
		
	def setDesiredSpeed(self, speed):
		if speed > self.maxSpeed:
			self.desiredSpeed = self.maxSpeed
		elif speed < 0:
			self.desiredSpeed = 0
		else:
			self.desiredSpeed = speed
		
	def near(self, pos):
		if self.getPosition().distTo(pos) < self.currentSpeed / self.timestepLength:
			return True
		else:
			return False
			
	def getInitialPosition(self):
		return self.initialPosition
		