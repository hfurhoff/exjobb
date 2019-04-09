import matplotlib.pyplot as plt
from util.log import Log
from dto.logentry import LogEntry
from dto.searchareadto import SearchareaDTO
from dto.pose import Pose
from dto.point import Point

import numpy as np
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
from matplotlib.patches import Ellipse
from matplotlib.transforms import Affine2D
from matplotlib.colors import Normalize
from matplotlib import cm

class RealityPlot():
	
	gridsize = 1
	
	def __init__(self, gridsize):
		self.gridsize = gridsize
		
	def playLog(self, log, area, timestepLength):
		fig, ax = plt.subplots()
		halfSideLength = area.getHalfSideLength()
		cells = 2 * halfSideLength
		data = [0] * cells
		for i in range(cells):
			data[i] = [0] * cells
			
		for i in range(log.length()):
			entry = log.get(i)
			pos = entry.getPose().getPosition()
			x, y = int(pos.getX()), int(pos.getY())
			data[y][x] = 1
			ax.cla()
			ax.set_xlim(-halfSideLength, halfSideLength)
			ax.set_ylim(-halfSideLength, halfSideLength)
			ax.imshow(data, cmap=cm.YlOrRd, extent=(-halfSideLength,halfSideLength,-halfSideLength,halfSideLength))
			ax.set_title("{}".format(i))
			plt.pause(timestepLength)