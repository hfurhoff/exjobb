from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
import re
import os

from view.plot import Plot
from view.settingselector import SettingSelector
from contr.controller import Controller
from dto.searchareadto import SearchareaDTO
from dto.vehicledto import VehicleDTO
from dto.pose import Pose
from dto.settings import Settings
import threading

class GUI(Frame):
	
	_HEIGHTINDEX = 0
	_WIDTHINDEX = 1
	_COURSEINDEX = 2
	_TIMESTEPINDEX = 3
	_MAXSPEEDINDEX = 4
	_TARGETXINDEX = 5
	_TARGETYINDEX = 6
	_RUNSINDEX = 7
	_GRIDSIZEINDEX = 8
	_SENSORDIAMETERINDEX = 9
	_TURNINGRADIUSINDEX = 10
	_LOOKAHEADINDEX = 11
	
	contr = Controller.getInstance()
	
	startPltBut = None
	showPltBut = None
	strategySelector = None
	execSearchBut = None
	finalPltBut = None
	speedUpBut = None
	sensorModelBut = None

	statusLabel = None

	buts = []
	entries = []
	
	textFields = [	'Searcharea height (m)', 
					'Searcharea width (m)', 
					'Initial course (degrees)', 
					'Timestep length (s)', 
					'Vehicle max speed (m/s)', 
					'Target X-coordinate (m)', 
					'Target Y-coordinate (m)', 
					'Number of runs',
					'Gridsize (m)',
					'Sensor radius (m)',
					'Turningradius (degrees/second)',
					'Lookahead-depth (times sensor-reach)']

	values = [5, 10, 30, 0.01, 1, 'n', 'n', 1, 1, 2, 25, 1]
	strategy = "greedy.py"
	speedUp = None
	threads = []
	plot = Plot()

	def newFile(self):
		print "New File!"
	def openFile(self):
		name = askopenfilename()
		print name
	def saveFile(self):
		name = asksaveasfilename()
		print name

	def readValue(self, input, v):
		try:
			v = float(input.get())
		except:
			try:
				v = int(input.get())
			except:
				pass
		return v

	def readInputFields(self):
		for i in range(len(self.values)):
			self.values[i] = self.readValue(self.entries[i], self.values[i])
			if i == self._TARGETXINDEX or i == self._TARGETYINDEX:
				self.values[i] = self.entries[i].get()
			
		self.strategy = self.strategySelector.get(ACTIVE)
	
	def showSearcharea(self):
		self.readInputFields()
		for i in range(int(self.values[self._RUNSINDEX])):
			premises = self.getPremises()
			self.contr.setupSimulation(premises)
			self.plot.showSearcharea(self.contr.getSearcharea())

	def showSimulation(self):
		self.readInputFields()
		search = self.contr.getAckumulatedSearch()
		dt = self.values[self._TIMESTEPINDEX]
		speedUp = self.speedUp.get()
		self.plot.showSimulation(search, dt, speedUp)

	def processSearch(self):
		self.readInputFields()
		premises = self.getPremises()
		#t = threading.Thread(target=self.contr.simulate, args=(premises,))
		#self.threads.append(t)
		#t.setDaemon(True)
		#t.start()
		self.contr.simulate(premises)
		
	def showSearchResult(self):
		self.readInputFields()
		self.plot.showSearchResult(self.contr.getSearcharea(), self.contr.getLog())
		
	def getPremises(self):
		return Settings(	self.values[self._HEIGHTINDEX], 
							self.values[self._WIDTHINDEX], 
							self.values[self._COURSEINDEX], 
							self.strategy[:-3], 
							None, 
							self.values[self._LOOKAHEADINDEX], 
							self.values[self._GRIDSIZEINDEX], 
							self.values[self._MAXSPEEDINDEX], 
							self.values[self._TARGETXINDEX], 
							self.values[self._TARGETYINDEX], 
							self.values[self._SENSORDIAMETERINDEX], 
							self.values[self._TURNINGRADIUSINDEX])

	def showSensorModel(self):
		self.readInputFields()
		premises = self.getPremises()
		sensor = premises.getSensor()
		self.plot.showSensorModel(sensor)

	def createWidgets(self, root):
		menu = Menu(root)
		root.config(menu=menu)
		filemenu = Menu(menu)
		menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="New", command=self.newFile)
		filemenu.add_command(label="Open...", command=self.openFile)
		filemenu.add_command(label="Save as...", command=self.saveFile)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=root.quit)

		self.sensorModelBut = Button(self)
		self.sensorModelBut["text"] = "Show sensormodel",
		self.sensorModelBut["command"] = self.showSensorModel
		self.buts.append(self.sensorModelBut)
		
		self.execSearchBut = Button(self)
		self.execSearchBut["text"] = "Process search",
		self.execSearchBut["command"] = self.processSearch
		self.buts.append(self.execSearchBut)
		
		self.startPltBut = Button(self)
		self.startPltBut["text"] = "Show search",
		self.startPltBut["command"] = self.showSimulation
		self.buts.append(self.startPltBut)
		
		self.finalPltBut = Button(self)
		self.finalPltBut["text"] = "Show final searcharea",
		self.finalPltBut["command"] = self.showSearchResult
		self.buts.append(self.finalPltBut)

		self.speedUp = BooleanVar()
		self.speedUpBut = Checkbutton(self, text = "SpeedUp", variable = self.speedUp)
		self.buts.append(self.speedUpBut)
		
		for i in range(len(self.textFields)):
			e = Entry(self)
			self.entries.append(e)
			e.grid(row = i + 1, column = 1)
			l = Label(self, text=self.textFields[i])
			l.grid(row = i + 1, column = 0, sticky = E)
			
		self.strategySelector = Listbox(self, selectmode=SINGLE)
		strategyLabel = Label(self, text='Searchstrategy')
		
		strategyLabel.grid(row = 0, column = 2)
		self.strategySelector.grid(row = 1, column = 2, rowspan = len(self.textFields))
		for i in range(len(self.buts)):
			self.buts[i].grid(row = len(self.textFields) + 1, column = i)
		
		for item in self.contr.getStrategies():
			self.strategySelector.insert(END, item)

	def __init__(self, master=None):
		master = Tk()
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets(master)
		self.mainloop()
