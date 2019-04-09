from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
import re
import os

from view.searchplot import SearchPlot
from view.realityplot import RealityPlot
from view.settingselector import SettingSelector
from contr.controller import Controller
from dto.searchareadto import SearchareaDTO
from dto.vehicledto import VehicleDTO
from dto.pose import Pose
from dto.settings import Settings

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
	
	contr = Controller.getInstance()
	
	startPltBut = None
	showPltBut = None
	strategySelector = None
	execSearchBut = None

	statusLabel = None

	buts = []
	entries = []
	
	textFields = [	'Searcharea height (m)', 
					'Searcharea width (m)', 
					'Initial course (degrees)', 
					'Timestep length (s)', 
					'Vehicle max speed (m/s)', 
					'Target X-coordinate', 
					'Target Y-coordinate', 
					'Number of runs',
					'Gridsize (m)']

	values = [5, 10, 30, 0.01, 1, 'n', 'n', 1, 1]
	strategy = "greedy.py"

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
			searchplt = SearchPlot(self.values[self._GRIDSIZEINDEX])
			premises = self.getPremises()
			self.contr.setupSimulation(premises)
			searchplt.showSearcharea(self.contr.getSearcharea())

	def showSimulation(self):
		self.readInputFields()
		searchplt = SearchPlot(self.values[self._GRIDSIZEINDEX])
		#realityplt = RealityPlot(self.values[self._GRIDSIZEINDEX])
		searchplt.showSimulation(self.contr.getAckumulatedSearch(), self.contr.getLog(), self.values[self._TIMESTEPINDEX])
		#realityplt.playLog(self.contr.getLog(), self.contr.getSearcharea(), self.values[self._TIMESTEPINDEX])

	def processSearch(self):
		self.readInputFields()
		premises = self.getPremises()
		self.contr.setupSimulation(premises)
		self.contr.startSimulation()
		print('ready to show simulation')

	def getPremises(self):
		return Settings(self.values[self._HEIGHTINDEX], self.values[self._WIDTHINDEX], self.values[self._COURSEINDEX], self.strategy[:-3], None, None, self.values[self._GRIDSIZEINDEX], self.values[self._MAXSPEEDINDEX], self.values[self._TARGETXINDEX], self.values[self._TARGETYINDEX])

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

		self.showPltBut = Button(self)
		self.showPltBut["text"] = "Show searcharea",
		self.showPltBut["command"] = self.showSearcharea
		self.buts.append(self.showPltBut)
		
		self.execSearchBut = Button(self)
		self.execSearchBut["text"] = "Process search",
		self.execSearchBut["command"] = self.processSearch
		self.buts.append(self.execSearchBut)
		
		self.startPltBut = Button(self)
		self.startPltBut["text"] = "Show search",
		self.startPltBut["command"] = self.showSimulation
		self.buts.append(self.startPltBut)
		
		
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
		
		for item in sorted(os.listdir("../simulationmodel/strategies")):
			if(re.findall("^_|.pyc$", item)):
				pass
			else:
				self.strategySelector.insert(END, item)

	def __init__(self, master=None):
		master = Tk()
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets(master)
		self.mainloop()
