from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
import threading
import re
import os
import time
import datetime

from view.plot import Plot
from view.settingselector import SettingSelector

from contr.controller import Controller

from dto.searchareadto import SearchareaDTO
from dto.vehicledto import VehicleDTO
from dto.settings import Settings
from dto.point import Point
from dto.pose import Pose

class GUI(Frame):
	
	_HEIGHTINDEX = 0
	_WIDTHINDEX = 1
	_COURSEINDEX = 2
	_MAXSPEEDINDEX = 3
	_TARGETXINDEX = 4
	_TARGETYINDEX = 5
	_RUNSINDEX = 6
	_GRIDSIZEINDEX = 7
	_SENSORDIAMETERINDEX = 8
	_TURNINGRADIUSINDEX = 9
	_LOOKAHEADINDEX = 10
	
	contr = Controller.getInstance()
	
	startPltBut = None
	showAreaBut = None
	strategySelector = None
	searchSelector = None
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
					'Vehicle max speed (m/s)', 
					'Target X-coordinate (m)', 
					'Target Y-coordinate (m)', 
					'Number of runs',
					'Gridsize (m)',
					'Sensor radius (m)',
					'Turningradius (degrees/second)',
					'Lookahead-depth (times sensor-reach)']

	values = [20, 20, 30, 1, 'n', 'n', 1, 1, 1, 25, 1]
	strategies = ["greedy.py"]
	processedSearches = dict()
	searchKey = None
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
					
		self.strategies = []
		for i in map(int, self.strategySelector.curselection()):
			self.strategies.append(self.strategySelector.get(i))
		if self.strategies == []:
			self.strategies.append("greedy.py")
		
		self.searchKey = self.searchSelector.get(ACTIVE)
	
	def showSearcharea(self):
		self.readInputFields()
		for i in range(len(self.strategies)):
			premises = self.getPremises(self.strategies[i])
			self.contr.setupSimulation(premises)
			sa = self.contr.getSearcharea()
			self.plot.showSearcharea(sa)

	def showSimulation(self):
		self.readInputFields()
		search = self.processedSearches[self.searchKey]
		speedUp = self.speedUp.get()
		self.plot.showSimulation(search, speedUp)

	def processSearch(self):
		ackSimLength = dict()
		ackProcTime = dict()
		targets = []
		self.readInputFields()
		originalTargetX = self.values[self._TARGETXINDEX]
		originalTargetY = self.values[self._TARGETYINDEX]
		for strat in self.strategies:
			ackSimLength[strat] = 0
			ackProcTime[strat] = 0
		runs = int(self.values[self._RUNSINDEX])
		for i in range(runs):
			self.values[self._TARGETXINDEX] = originalTargetX
			self.values[self._TARGETYINDEX] = originalTargetY
			premises = self.getPremises(self.strategies[0])
			self.contr.simulate(premises)
			sa = self.contr.getSearcharea()
			dto = self.contr.getAckumulatedSearch()
			self.processedSearches[dto.toString()] = dto
			self.searchSelector.insert(0, dto.toString())
			ackSimLength[self.strategies[0]] = ackSimLength[self.strategies[0]] + dto.len()
			ackProcTime[self.strategies[0]] = ackProcTime[self.strategies[0]] + dto.getRTS() + (0.000001 * dto.getRTMS())
			target = sa.getTarget()
			x, y = target.getX(), target.getY()
			orTar = Point(x, y)
			targets.append(orTar)
			if len(self.strategies) > 1:
				self.values[self._TARGETXINDEX] = x
				self.values[self._TARGETYINDEX] = -y
				for j in range(1, len(self.strategies)):
					strat = self.strategies[j]
					premises = self.getPremises(strat)
					self.contr.simulate(premises)
					dto = self.contr.getAckumulatedSearch()
					self.processedSearches[dto.toString()] = dto
					self.searchSelector.insert(0, dto.toString())
					ackSimLength[strat] = ackSimLength[strat] + dto.len()
					ackProcTime[strat] = ackProcTime[strat] + dto.getRTS() + (0.000001 * dto.getRTMS())
		mttds = dict()
		for strat in self.strategies:
			mttds[strat] = ackSimLength[strat] / float(runs)
			
		averageProcTime = dict()
		for strat in self.strategies:
			averageProcTime[strat] = ackProcTime[strat] / float(runs)
			
		totDist = 0
		origo = Point(0, 0)
		for p in targets:
			totDist = totDist + p.distTo(origo)
		
		dto = self.contr.getAckumulatedSearch()
		h = str(dto.getHeight())
		w = str(dto.getWidth())
		filename = "../../mttds/" + str(runs) + '_' + h + 'x' + w
		for strat in self.strategies:
			tmp = strat[:-3]
			filename = filename + '_' + tmp[:2] + tmp[-2:]
		file = open(filename + ".txt", "a")
		file.write('*****************************************************************\n')
		file.write(str(datetime.datetime.now()))
		file.write('\nUNITS : SECONDS AND METERS')
		file.write('\nAVERAGE DISTANCE TO TARGET FROM ORIGO: ' + str(totDist / runs))
		file.write('\nRUNS: ' + str(runs))
		file.write('\nHEIGHTxWIDTH: ' + h + 'x' + w + '\n')
		file.write('-----------------------------------------------------------------\n')
		file.write('Strategy\t|MTTD\t\t|MEAN PROC TIME\t\t|\n')
		file.write('-----------------------------------------------------------------\n')
		for strat in self.strategies:
			stratname = strat[:2] + strat[-5:-3] 
			apt = str(averageProcTime[strat])
			mttd = str(round(mttds[strat], 2))
			if len(apt) < 7:
				apt = apt + '\t'
			file.write(stratname + '\t\t|' + mttd + '\t\t|' + apt + '\t\t|\n')
		file.write('*****************************************************************\n')
		
	def showSearchResult(self):
		self.readInputFields()
		search = self.processedSearches[self.searchKey]
		sa = search.getEndState()
		log = search.getLog()
		self.plot.showSearchResult(sa, log)
		
	def getPremises(self, strategy):
		return Settings(	self.values[self._HEIGHTINDEX], 
							self.values[self._WIDTHINDEX], 
							self.values[self._COURSEINDEX], 
							strategy[:-3], 
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
		premises = self.getPremises('greedy.py')
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

		self.showAreaBut = Button(self)
		self.showAreaBut["text"] = "Show searcharea",
		self.showAreaBut["command"] = self.showSearcharea
		self.buts.append(self.showAreaBut)

		self.sensorModelBut = Button(self)
		self.sensorModelBut["text"] = "Show sensormodel",
		self.sensorModelBut["command"] = self.showSensorModel
		self.buts.append(self.sensorModelBut)
		
		self.execSearchBut = Button(self)
		self.execSearchBut["text"] = "Process search",
		self.execSearchBut["command"] = self.processSearch
		self.buts.append(self.execSearchBut)
		
		self.finalPltBut = Button(self)
		self.finalPltBut["text"] = "Show final searcharea",
		self.finalPltBut["command"] = self.showSearchResult
		self.buts.append(self.finalPltBut)
		
		self.startPltBut = Button(self)
		self.startPltBut["text"] = "Show search",
		self.startPltBut["command"] = self.showSimulation
		self.buts.append(self.startPltBut)
		
		self.speedUp = BooleanVar()
		self.speedUpBut = Checkbutton(self, text = "SpeedUp", variable = self.speedUp)
		self.buts.append(self.speedUpBut)
		
		for i in range(len(self.textFields)):
			e = Entry(self)
			self.entries.append(e)
			e.grid(row = i + 1, column = 1)
			l = Label(self, text=str(self.textFields[i]))
			l.grid(row = i + 1, column = 0, sticky = E)
			
		self.strategySelector = Listbox(self, selectmode=EXTENDED)
		strategyLabel = Label(self, text='Searchstrategy')
		strategyLabel.grid(row = 0, column = 2)
		self.strategySelector.grid(row = 1, column = 2, rowspan = len(self.textFields))
		
		fr = Frame(self, bd=2, relief=SUNKEN)

		yscroll = Scrollbar(fr, orient = VERTICAL)
		yscroll.pack(side=RIGHT, fill=Y)
		
		xscroll = Scrollbar(fr, orient = HORIZONTAL)
		xscroll.pack(side=BOTTOM, fill=X)

		w = 40
		self.searchSelector = Listbox(fr, selectmode=SINGLE, width = w, yscrollcommand=yscroll.set, xscrollcommand=xscroll.set, bd = 2)
		searchesLabel = Label(self, text='Processed searches')
		searchesLabel.grid(row = 0, column = 3)
		self.searchSelector.pack()
		yscroll.config(command=self.searchSelector.yview)
		xscroll.config(command=self.searchSelector.xview)
		fr.pack()
		
		fr.grid(row = 1, column = 3, rowspan = len(self.textFields), columnspan = (w / 20))
		
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
