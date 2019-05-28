from util.observer import Observer
from util.log import Log
from dto.event import Event
from dto.searchareadto import SearchareaDTO
from dto.vehicledto import VehicleDTO
from dto.pose import Pose
from dto.logentry import LogEntry
from dto.pose import Pose
from dto.point import Point
from dto.sensor import Sensor
from dto.searchdto import SearchDTO

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
from matplotlib.patches import Ellipse
from matplotlib.transforms import Affine2D, Bbox
from matplotlib.colors import Normalize, ListedColormap
from matplotlib import cm
from scipy.stats import norm
from matplotlib.colorbar import *

class Plot(Observer):
	
	gridsize = 1
	
	def __init__(self):
		pass
	
	def handleDTO(self, dto):
		height = dto.getHeight()
		width = dto.getWidth()
		return height, width
	
	def showSearcharea(self, dto):
		data = dto.getData()
		halfSideLength = dto.getHalfSideLength()
		fig, ax = plt.subplots()
		cmap = self.getCmap(dto.isCoverage())
		ax.cla()
		ax.set_xlim(-halfSideLength, halfSideLength)
		ax.set_ylim(-halfSideLength, halfSideLength)
		im = ax.imshow(data, cmap=cmap, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength))
		ax.grid(b=True, which='both', axis='both')
		gs = (2.0 * halfSideLength) / float(len(data))
		ax.set_xticks(np.arange(-halfSideLength, halfSideLength, gs))
		ax.set_yticks(np.arange(-halfSideLength, halfSideLength, gs))
		ax.set_xticklabels([])
		if dto.isCoverage():
			cbar = fig.colorbar(im, ax=ax, label="Coverage", ticks=[0, 0.5, 1])
			cbar.ax.set_yticklabels(['Not active', 'Visited', 'Unvisited'])
		else:
			cbar = fig.colorbar(im, ax=ax, label="Probability")
		plt.show(block=False)

	def showSensorModel(self, sensor):
		max = int(round(sensor.getMaxRange()) * 1.5)
		domain = range(-max, max + 1)
		sensorSamples = []
		for dist in domain:
			sensorSamples.append(sensor.probabilityOfDetection(dist))
		plt.plot(domain, sensorSamples)
		plt.axis([-max, max, -0.5, 1.5])
		plt.ylabel('Probability of detection')
		plt.xlabel('Distance from sensor')
		plt.show(block=False)
	
	def radFromCenter(self, x, ex, y, ey):
		return (np.power(x, 2) / np.power(ex, 2)) + (np.power(y, 2) / np.power(ey, 2))
		
	def showSimulation(self, dto, speedUp, viewingStep):
		#print(repr(data))
		#print(repr(range(len(data))))
		
		log = dto.getLog()
		data = dto.getData()
		fig, ax = plt.subplots(ncols=2, figsize=[2 * 6.5, 4.8])
		cmap = self.getCmap(dto.isCoverage())
		
		halfSideLength = dto.getHalfSideLength()
		world = [0] * len(data)
		for c in world:
			c = [0] * len(data)
		
		xpath = []
		ypath = []
		im = ax[0].imshow(data, cmap=cmap, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength))
		cbar = fig.colorbar(im, ax=ax[0], label="Probability")
		for i in range(dto.len()):
			logentry = log.get(i)
			pos = logentry.getPosition()
			x = pos.getX()
			y = pos.getY()
			xpath.append(x)
			ypath.append(-y)

			change = dto.getChange(i)
			for cell in change:
				data[cell.getY()][cell.getX()] = cell.getProb()
						
			if speedUp:
				if i % viewingStep == 0:
					im, cbar = self.displayIm(fig, ax, im, cbar, dto, i, xpath, ypath, log, data)
				elif i >= dto.len() - 10:
					im, cbar = self.displayIm(fig, ax, im, cbar, dto, i, xpath, ypath, log, data)
			else:
				im, cbar = self.displayIm(fig, ax, im, cbar, dto, i, xpath, ypath, log, data)
		for a in ax:
			a.cla()
		
				
	def displayIm(self, fig, ax, im, cbar, dto, i, xpath, ypath, log, data):
		halfSideLength = dto.getHalfSideLength()
		for a in ax:
			a.cla()
			a.set_xlim(-halfSideLength, halfSideLength)
			a.set_ylim(-halfSideLength, halfSideLength)
		target = dto.getTarget()
		sensor = log.get(0).getSensor()
		sensorRad = sensor.getRadius()
		sensorMax = sensor.getMaxRange()
		targetx = target.getX()
		targety = target.getY()
		max = 0
		for k in data:
			for l in k:
				if max < l:
					max = l
		cmap = self.getCmap(dto.isCoverage())
		cbar.remove()
		im = ax[0].imshow(data, cmap=cmap, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength), vmin=0, vmax=max)
		ax[0].grid(b=True, which='both', axis='both')
		gs = (2.0 * halfSideLength) / float(len(data))
		ax[0].set_xticks(np.arange(-halfSideLength, halfSideLength, gs))
		ax[0].set_yticks(np.arange(-halfSideLength, halfSideLength, gs))
		ax[0].set_xticklabels([])
		ax[1].plot(targetx, -targety, 'ro')
		ax[1].plot(xpath, ypath, 'k')
		ellipse = Ellipse([0, 0], dto.getWidth(), dto.getHeight(), 0, fill=False, linestyle='-')
		ax[1].add_artist(ellipse)
		outerCircle = plt.Circle((xpath[-1], ypath[-1]), sensorMax, color='green')
		innerCircle = plt.Circle((xpath[-1], ypath[-1]), sensorRad, color='blue')
		ax[1].add_artist(outerCircle)
		ax[1].add_artist(innerCircle)
		fig.suptitle('Timestep: ' + repr(i))
		
		if dto.isCoverage():
			ax[0].set_title("Coverage plot")
			cbar = fig.colorbar(im, ax=ax[0], label="Coverage", ticks=[0, 0.5, 1])
			cbar.ax.set_yticklabels(['Not active', 'Visited', 'Unvisited'])
		else:
			ax[0].set_title("Probability plot")
			cbar = fig.colorbar(im, ax=ax[0], label="Probability")
		
		ax[1].set_title("Reality plot")
		plt.pause(0.01)
		return im, cbar

	def getCmap(self, coverage):
		if not coverage:
			jet = cm.jet
			newcolors = jet(np.linspace(0, 1, 256))
			white = np.array([1, 1, 1, 1])
			newcolors[:1, :] = white
			cmap = ListedColormap(newcolors)
			return cmap
		else:
			jet = cm.jet
			newcolors = jet(np.linspace(0, 1, 3))
			white = np.array([1, 1, 1, 1])
			red = np.array([1, 0, 0, 1])
			green = np.array([0, 1, 0, 1])
			newcolors[0] = white
			newcolors[1] = green
			newcolors[2] = red
			cmap = ListedColormap(newcolors)
			return cmap

	def showSearchResult(self, data, log):
		fig, ax = plt.subplots(ncols=2, figsize=[2 * 6.5, 4.8])
		cmap = self.getCmap(data.isCoverage())
		
		halfSideLength = int(round(data.getHalfSideLength()))
		max = 0
		d = data.getData()
		for k in d:
			for l in k:
				if max < l:
					max = l
		im = ax[0].imshow(d, cmap=cmap, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength), vmin=0, vmax=max)
		ax[0].grid(b=True, which='both', axis='both')
		gs = (2.0 * halfSideLength) / float(len(d))
		ax[0].set_xticks(np.arange(-halfSideLength, halfSideLength, gs))
		ax[0].set_yticks(np.arange(-halfSideLength, halfSideLength, gs))
		ax[0].set_xticklabels([])
		
		target = data.getTarget()
		targetx = target.getX()
		targety = target.getY()
		xpath = []
		ypath = []
		sensorRad = log.get(0).getSensor().getRadius()
		circle = None
		for i in range(log.length()):
			logentry = log.get(i)
			pos = logentry.getPosition()
			x = pos.getX()
			y = pos.getY()
			xpath.append(x)
			ypath.append(-y)
		ax[1].plot(xpath, ypath, 'k')
		ellipse = Ellipse([0, 0], data.getWidth(), data.getHeight(), 0, fill=False, linestyle='-')
		ax[1].add_artist(ellipse)
		circle = plt.Circle((xpath[-1], ypath[-1]), sensorRad, color='blue')
		ax[1].plot(targetx, -targety, 'ro')
		ax[1].add_artist(circle)
		ax[1].set_xbound(-halfSideLength, halfSideLength)
		ax[1].set_ybound(-halfSideLength, halfSideLength)
		fig.suptitle('Timestep: ' + repr(i))

		if data.isCoverage():
			ax[0].set_title("Coverage plot")
			cbar = fig.colorbar(im, ax=ax[0], label="Coverage", ticks=[0, 0.5, 1])
			cbar.ax.set_yticklabels(['Not active', 'Visited', 'Unvisited'])
		else:
			ax[0].set_title("Probability plot")
			cbar = fig.colorbar(im, ax=ax[0], label="Probability")

		ax[1].set_title("Reality plot")
		plt.show(block=False)
		
	def playLog(self, log):
		pass
		
	def startSimulation(self):
		pass
		
	def notify(self, event):
		pass
