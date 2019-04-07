from dto.pose import Pose
from dto.pdf import PDF
from dto.target import Target
from util.log import Log
from simulationmodel.searcharea import Searcharea

class QuadtreeMap(Searcharea):

	pose = None
	height = None
	width = None
	pdf = None
	target = None
	sampledSpace = None
	
	def __init__(self):
		pass
		
	def updateSearchBasedOnLog(self, samples):
		pass