from abc import ABCMeta, abstractmethod
from dto.pose import Pose
from dto.pdf import PDF
from dto.target import Target
from util.log import Log


class Searcharea:
	__metaclass__ = ABCMeta

	height = None
	width = None
	pdf = None
	target = None
	sampledSpace = None
	gridsize = None
	
	def __init__(self):
		pass
		
	@abstractmethod
	def updateSearchBasedOnLog(self, log):
		pass