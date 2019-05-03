from util.observer import Observer
from util.log import Log
from dto.event import Event
from dto.searchareadto import SearchareaDTO
from dto.vehicledto import VehicleDTO
from dto.pose import Pose
from dto.logentry import LogEntry
from dto.pose import Pose
from dto.point import Point

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
from matplotlib.patches import Ellipse
from matplotlib.transforms import Affine2D
from matplotlib.colors import Normalize, ListedColormap
from matplotlib import cm
from scipy.stats import norm
from matplotlib.colorbar import *

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
		im = ax.imshow(data, cmap=cm.YlOrRd, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength))
		fig.colorbar(im, ax=ax)
		plt.show(block=False)
	
	def radFromCenter(self, x, ex, y, ey):
		return (np.power(x, 2) / np.power(ex, 2)) + (np.power(y, 2) / np.power(ey, 2))
		
	def showSimulation(self, data, log, timestepLength):
		#print(repr(data))
		#print(repr(range(len(data))))
		fig, ax = plt.subplots(ncols=2, figsize=[2 * 6.5, 4.8])
		
		jet = cm.jet
		newcolors = jet(np.linspace(0, 1, 256))
		white = np.array([1, 1, 1, 1])
		newcolors[:1, :] = white
		cmap = ListedColormap(newcolors)
		
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
		im = ax[0].imshow(data[0].getData(), cmap=cmap, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength))
		cbar = fig.colorbar(im, ax=ax[0], label="Probability")
		for i in range(len(data)):
			for a in ax:
				a.cla()
				a.set_xlim(-halfSideLength, halfSideLength)
				a.set_ylim(-halfSideLength, halfSideLength)
			
			#ax[1].set_axis_off()
			pos = log.get(i).getPose().getPosition()
			x = pos.getX()
			y = pos.getY()
			xpath.append(x)
			ypath.append(-y)
			ax[1].plot(targetx, -targety, 'ro')
			ax[1].plot(xpath, ypath, 'k')

			d = data[i].getData()
			
			max = 0
			for k in d:
				for l in k:
					if max < l:
						max = l
			
			cbar.remove()
			im = ax[0].imshow(d, cmap=cmap, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength), vmin=0, vmax=max)
			cbar = fig.colorbar(im, ax=ax[0], label="Probability")
			
			fig.suptitle('Timestep: ' + repr(i))
			ax[0].set_title("Probability plot")
			ax[1].set_title("Reality plot")
			plt.pause(timestepLength)
			
	def playLog(self, log):
		pass
		
	def startSimulation(self):
		pass
		
	def notify(self, event):
		pass
