import numpy as np
from scipy.stats import norm

class Sensor():

	diameter = 1
	mean = 0
	stddev = 0.2
	
	def __init__(self, diameter):
		self.diameter = diameter
		self.stddev = diameter / 10.0
		
	def getDiameter(self):
		return self.diameter
		
	def probabilityOfDetection(self, dist):
		if dist > self.diameter / 2:
			return 0
		return norm.pdf(dist, self.mean, self.stddev)