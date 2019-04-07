import matplotlib.pyplot as plt
from util.observer import Observer
from util.log import Log
from dto.event import Event
from dto.searchareadto import SearchareaDTO
from dto.vehicledto import VehicleDTO
from dto.pose import Pose

import numpy as np
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
from matplotlib.patches import Ellipse
from matplotlib.transforms import Affine2D
from matplotlib.colors import Normalize
from matplotlib import cm
from scipy.stats import norm

class Plot(Observer):
	
	gridsize = 1
	
	def __init__(self, gridsize):
		self.gridsize = gridsize
	
	def handleDTO(self, dto):
		height = dto.getHeight()
		width = dto.getWidth()
		return height, width
	
	def showSearcharea(self, dto):
		data = dto.getData()
		halfSideLength = dto.getHalfSideLength()
		fig, ax = plt.subplots()
		ax.cla()
		ax.set_xlim(-halfSideLength, halfSideLength)
		ax.set_ylim(-halfSideLength, halfSideLength)
		ax.imshow(data, cmap=cm.YlOrRd, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength))
		plt.show(block=False)
	
	def radFromCenter(self, x, ex, y, ey):
		return (np.power(x, 2) / np.power(ex, 2)) + (np.power(y, 2) / np.power(ey, 2))
		
	def showSimulation(self, data, timestepLength):
		#print(repr(data))
		#print(repr(range(len(data))))
		fig, ax = plt.subplots()
		halfSideLength = int(data[0].getHalfSideLength())

		for i in range(len(data)):
			ax.cla()
			ax.set_xlim(-halfSideLength, halfSideLength)
			ax.set_ylim(-halfSideLength, halfSideLength)
			ax.imshow(data[i].getData(), cmap=cm.YlOrRd, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength))
			ax.set_title("{}".format(i))
			plt.pause(timestepLength)
			
	def playLog(self, log):
		pass
		
	def startSimulation(self):
		pass
		
	def notify(self, event):
		pass
