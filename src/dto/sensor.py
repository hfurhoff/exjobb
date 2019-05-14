import numpy as np
from scipy.stats import norm

class Sensor():

	radius = 1
	mean = 0
	coverage = False
	
	def __init__(self, radius, coverage):
		self.radius = radius
		self.stddev = radius
		self.coverage = coverage
		
	def getDiameter(self):
		return self.radius * 2.0
		
	def getRadius(self):
		return self.radius
		
	def probabilityOfDetection(self, dist):
		prob = 1
		dist = abs(dist)
		if dist > self.radius:
			max = norm.pdf(self.mean, loc = self.mean, scale = self.stddev)
			prob = norm.pdf(dist, loc = self.mean, scale = self.stddev) / (max)
		if dist > self.getMaxRange():
			prob = 0
		return prob
		
	def getMaxRange(self):
		return self.radius * 2.0