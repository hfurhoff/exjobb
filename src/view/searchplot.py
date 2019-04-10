import matplotlib.pyplot as plt
from util.observer import Observer
from util.log import Log
from dto.event import Event
from dto.searchareadto import SearchareaDTO
from dto.vehicledto import VehicleDTO
from dto.pose import Pose
from dto.logentry import LogEntry
from dto.pose import Pose
from dto.point import Point

import numpy as np
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
from matplotlib.patches import Ellipse
from matplotlib.transforms import Affine2D
from matplotlib.colors import Normalize
from matplotlib import cm
from scipy.stats import norm

class SearchPlot(Observer):
	
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
		
	def showSimulation(self, data, log, timestepLength):
		#print(repr(data))
		#print(repr(range(len(data))))
		fig, ax = plt.subplots(ncols=2, figsize=[2 * 6, 4.8])
		halfSideLength = int(round(data[0].getHalfSideLength()))
		world = [0] * len(data)
		for c in world:
			c = [0] * len(data)
		
		target = data[0].getTarget()
		targetx = target.getX()
		targety = target.getY()
		ax[1].set_axis_off()
		xpath = []
		ypath = []
		
		for i in range(len(data)):
			for a in ax:
				a.cla()
				a.set_xlim(-halfSideLength, halfSideLength)
				a.set_ylim(-halfSideLength, halfSideLength)
			
			ax[1].set_axis_off()
			pos = log.get(i).getPose().getPosition()
			x = pos.getX()
			y = pos.getY()
			xpath.append(x)
			ypath.append(-y)
			ax[1].plot(targetx, -targety, 'ro')
			ax[1].plot(xpath, ypath, 'k')

			ax[0].cla()
			ax[0].set_xlim(-halfSideLength, halfSideLength)
			ax[0].set_ylim(-halfSideLength, halfSideLength)
			im = ax[0].imshow(data[i].getData(), cmap=cm.YlOrRd, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength))
			if i == 0:
				fig.colorbar(im, ax=ax[0])
			ax[0].set_title("{}".format(i))
			plt.pause(timestepLength)
			
	def playLog(self, log):
		pass
		
	def startSimulation(self):
		pass
		
	def notify(self, event):
		pass
