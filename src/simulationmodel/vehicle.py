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

	pose = None #TODO:convert to lat/long
	desiredHeading = None
	currentSpeed = None #m/s
	desiredSpeed = None
	maxSpeed = None
	turningRadius = None #degrees/second
	log = None
	sensorDia = None
	timestepLength = 1 #seconds

	def __init__(self, v):
		from dto.vehicledto import VehicleDTO
		self.pose = v.getPose()
		self.desiredHeading = self.pose.getOrientation()
		self.currentSpeed = v.getCurrentSpeed()
		self.maxSpeed = v.getMaxSpeed()
		self.turningRadius = v.getTurningRadius()
		self.sensorDia = v.getSensor()
		self.log = Log([self])
		
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
			hypo = self.currentSpeed * self.timestepLength
			currentHeading = self.getHeading()
			if currentHeading != self.desiredHeading:
				diff = self.desiredHeading - currentHeading
				if diff > 180:
					diff = 360 - diff
				if diff < -180:
					diff = diff + 360
				sign = diff / abs(diff)
				if abs(diff) > self.turningRadius:
					currentHeading = currentHeading + sign * self.turningRadius
				else:
					currentHeading = self.desiredHeading % 360
			course = np.radians((-currentHeading) + 90)
			
			dx = hypo * np.cos(course)
			dy = hypo * np.sin(course)
			x, y = p.getX(), p.getY()
			
			self.pose = Pose(currentHeading, Point(x + dx, y + dy))
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
		return self.sensorDia
	
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
		
	def near(self, pos):
		if self.getPosition().distTo(pos) < self.currentSpeed / self.timestepLength:
			return True
		else:
			return False