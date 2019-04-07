from abc import ABCMeta, abstractmethod
from dto.event import Event

class Observer:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def notify(self, event):
		pass