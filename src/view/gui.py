from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
import threading
import re
import os
import gc
import time
import datetime
import sys, traceback
from numpy import random

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
	_SPEEDUPFACTORINDEX = 11
	
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
					'Lookahead-depth (times sensor-reach)',
					'SpeedUp-factor']

	values = [20, 20, 30, 1, 'n', 'n', 1, 1, 1, 25, 1, 2]
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
		
		c = self.entries[self._COURSEINDEX].get()
		try:
			f = float(c)
			i = int(c)
		except:
			self.values[self._COURSEINDEX] = int(random.random_sample() * 360)
		
		try:
			self.values[self._SPEEDUPFACTORINDEX] = int(self.values[self._SPEEDUPFACTORINDEX])
			if self.values[self._SPEEDUPFACTORINDEX] < 1:
				self.values[self._SPEEDUPFACTORINDEX] = 1
		except:
			self.values[self._SPEEDUPFACTORINDEX] = 1
		
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
		self.plot.showSimulation(search, speedUp, self.values[self._SPEEDUPFACTORINDEX])

	def processSearch(self):
		startTime = str(datetime.datetime.now())
		self.readInputFields()
		randCourse = False
		try:
			c = self.entries[self._COURSEINDEX].get()
			f = float(c)
			i = int(c)
		except:
			randCourse = True
			
		try:
			tx = self.entries[self._TARGETXINDEX].get()
			ty = self.entries[self._TARGETYINDEX].get()
			f = float(tx)
			i = int(tx)
			f = float(ty)
			i = int(ty)
		except:
			self.values[self._TARGETXINDEX] = 'r'
			self.values[self._TARGETYINDEX] = 'r'
		ackSimLength = dict()
		ackProcTime = dict()
		gridsizes = dict()
		targets = []
		originalTargetX = self.values[self._TARGETXINDEX]
		originalTargetY = self.values[self._TARGETYINDEX]
		for strat in self.strategies:
			ackSimLength[strat] = 0
			ackProcTime[strat] = 0
		runs = int(self.values[self._RUNSINDEX])
		executedRuns = 0
		latestDTO = None
		try:
			gc.disable()
			for i in range(runs):
				print(repr(i) + '.0')
				if randCourse:
					self.values[self._COURSEINDEX] = int(random.random_sample() * 360)
				self.values[self._TARGETXINDEX] = originalTargetX
				self.values[self._TARGETYINDEX] = originalTargetY
				strat = self.strategies[0]
				premises = self.getPremises(strat)
				self.contr.simulate(premises)
				sa = self.contr.getSearcharea()
				latestDTO = self.contr.getAckumulatedSearch()
				self.processedSearches[latestDTO.toString()] = latestDTO
				self.searchSelector.insert(0, latestDTO.toString())
				ackSimLength[strat] = ackSimLength[strat] + latestDTO.len()
				rt = latestDTO.getRTS() + (0.000001 * latestDTO.getRTMS())
				print('running time: ' + repr(rt) + '\n')
				ackProcTime[strat] = ackProcTime[strat] + rt
				target = sa.getTarget()
				x, y = target.getX(), target.getY()
				orTar = Point(x, y)
				targets.append(orTar)
				if i == 0:
					gridsizes[strat] = latestDTO.getGridsize()
				if len(self.strategies) > 1:
					self.values[self._TARGETXINDEX] = x
					self.values[self._TARGETYINDEX] = -y
					for j in range(1, len(self.strategies)):
						print(repr(i) + '.' + repr(j))
						strat = self.strategies[j]
						premises = self.getPremises(strat)
						self.contr.simulate(premises)
						latestDTO = self.contr.getAckumulatedSearch()
						rt = latestDTO.getRTS() + (0.000001 * latestDTO.getRTMS())
						print('running time: ' + repr(rt) + '\n')
						self.processedSearches[latestDTO.toString()] = latestDTO
						self.searchSelector.insert(0, latestDTO.toString())
						ackSimLength[strat] = ackSimLength[strat] + latestDTO.len()
						ackProcTime[strat] = ackProcTime[strat] + rt
						if i == 0:
							gridsizes[strat] = latestDTO.getGridsize()
				executedRuns += 1
				if executedRuns % 3 == 0 and not executedRuns > runs - 4:
					self.searchSelector.delete(0, END)
					self.processedSearches.clear()
					gc.collect()
					print(gc.garbage)
		except:
			print "Exception in user code:"
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60
		finally:
			if not gc.isenabled():
				gc.collect()
				gc.enable()
		self.values[self._TARGETXINDEX] = originalTargetX
		self.values[self._TARGETYINDEX]	= originalTargetY
		totDist = 0
		origo = Point(0, 0)
		for p in targets:
			totDist = totDist + p.distTo(origo)
		
		mttds = dict()
		averageProcTime = dict()
		h = str(latestDTO.getHeight())
		w = str(latestDTO.getWidth())
		filename = "../../mttds/" + h + 'x' + w
		for strat in self.strategies:
			mttds[strat] = ackSimLength[strat] / float(executedRuns)
			averageProcTime[strat] = ackProcTime[strat] / float(executedRuns)
			tmp = strat[:-3]
			filename = filename + '_' + tmp[:2] + tmp[-2:]
		file = open(filename + ".txt", "a")
		file.write('*************************************************************************\n')
		file.write('STARTED: \t' + startTime + '\n')
		endTime = str(datetime.datetime.now())
		file.write('FINISHED:\t' + endTime + '\n')
		file.write('PARAMETERS: ')
		if randCourse:
			self.values[self._COURSEINDEX] = 'r'
		for i in range(len(self.values)):
			if i % 2 == 0:
				file.write('\n' + self.textFields[i] + ' : ' + str(self.values[i]))
			else:
				file.write('\t' + self.textFields[i] + ' : ' + str(self.values[i]))
		file.write('\n\nUNITS : SECONDS AND METERS')
		file.write('\nAVERAGE DISTANCE TO TARGET FROM ORIGO: ' + str(totDist / executedRuns))
		file.write('\nRUNS PROCESSED: ' + str(executedRuns))
		file.write('\nHEIGHTxWIDTH: ' + h + 'x' + w + '\n')
		file.write('-------------------------------------------------------------------------\n')
		file.write('Strategy\t|MTTD\t\t|MEAN PROC TIME\t\t|GRIDSIZE\t|\n')
		file.write('-------------------------------------------------------------------------\n')
		for strat in self.strategies:
			stratname = strat[:2] + strat[-5:-3] 
			apt = str(averageProcTime[strat])
			mttd = str(round(mttds[strat], 2))
			if len(mttd) < 7:
				mttd = mttd + '\t'
			if len(apt) < 7:
				apt = apt + '\t'
			gs = str(gridsizes[strat])
			if len(gs) < 7:
				gs = gs + '\t'
			file.write(stratname + '\t\t|' + mttd + '\t|' + apt + '\t\t|' + gs + '\t|\n')
		file.write('*************************************************************************\n')
		print('processing done')
		
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
