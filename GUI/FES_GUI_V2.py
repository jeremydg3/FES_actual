# GUI for FES control

# Import statements
from os import path, chdir

from tkinter import Tk,StringVar,Message,Label,SUNKEN,LabelFrame,Button,OptionMenu,\
Entry,DISABLED,NORMAL,IntVar,Checkbutton, NW, RIGHT

import tkinter as tk
from PIL import ImageTk, Image
import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import glob
import serial
from serial import Serial
import time

# ==================================================================
# This is needed to allow for proper importing of default data files
import sys

if getattr(sys,'frozen',False):
	application_path = path.dirname(sys.executable)
	chdir(application_path)
	
	
# load image


# GUI Parameters
backgroundColor = 'white'
ONLY_USE_BLUETOOTH_PORT = False
PRINT_SERIAL_SENDING_SIGNALS = True
MANUAL_SERIAL_ENTRY = False
DATADELIMITER = ','
TIMEDELAY = 1
NINPUTS = 15 # There will be exactly this many datastream inputs for displaying
PLOTRATIO = (5,2)
PLOTDPI = 100
LABELFONTSIZE = 10
INDICATORFONTSIZE = 25
LABELFONT = ("Arial",LABELFONTSIZE,"bold")
INDICATORFONT = LABELFONT
NPOINTS = 100 # Number of points on which to plot the data stream
global img
global imgLabel


# Prints the argument, but after sending the timestamp as well.
def printtime(s,end=None):
	t = time.strftime("%R:%S")
	if end == None:
		print("%s - %s"%(t,s))
	else:
		print("%s - %s"%(t,s),end=end)
	return
	
	
# This function comes graciously from StackOverflow
# Finds all available serial ports, and returns as a list
def FindAllSerialPorts():
	if sys.platform.startswith('win'):
		ports = ['COM%s' % (i + 1) for i in range(256)]
	elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
		ports = glob.glob('/dev/tty[A-Za-z]*')
	elif sys.platform.startswith('darwin'):
		ports = glob.glob('/dev/tty.*')
	else:
		raise EnvironmentError('Unsupported platform')

	result = []
	print("Refreshing USB COM ports.")
	for port in ports:
		printtime(port,end="")
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
			print("...Good",end="")
		except:
			print("...",end="")
		print('')
	printtime("Done!")
	if len(result) == 0:
		result.append('NONE')
	
	return result


class FES:
	def __init__(self, master):
		self.master = master
		master.title("FES Control Console")
		master.configure(background = backgroundColor)
		
		self.IS_SERIAL_CONNECTED = False

		# other parameters
		self.IN_DEBUG_MODE = False
		self.IN_PHASEV_MODE = False
		self.IN_FSR_MODE = False
		self.OPERATIONMODE = 0
		self.AFFECTEDLIMB = 2 # 1: left leg, 2: right leg

		#			        left T	 left H   right T  right H   plantar  dorsal
		self.FSRRELs = 	   [False,   False,   False,   False,    False,   False]
		self.lastFSRRELs = [False,   False,   False,   False,    False,   False]

		#					left T     left H     right T    right H
		self.imgFSRlocs = [(35, 305), (75, 280), (230,305), (185, 280)]
		#					left D	  left P	 right D	right P
		self.imgRELlocs = [(60, 90), (85, 150), (205, 90), (180, 150)]

		
		# plotting data stream init
		self.GYRODATASTREAM = [[0 for points in range(NPOINTS)] for i in range(3)]
		self.ACCELDATASTREAM = [[0 for points in range(NPOINTS)] for i in range(3)]
		self.PHASEDATASTREAM = [0 for points in range(NPOINTS)]

		self.GYRODATASTREAM_LINE = []
		self.ACCELDATASTREAM_LINE = []
		self.PHASEDATASTREAM_LINE = []

		for i in range(3):
			self.GYRODATASTREAM_LINE.append(self.GYRODATASTREAM[i][-NPOINTS:])
			self.ACCELDATASTREAM_LINE.append(self.ACCELDATASTREAM[i][-NPOINTS:])
		self.PHASEDATASTREAM_LINE = self.PHASEDATASTREAM[-NPOINTS:]
		self.OTHERDATA = 0
		
		self.PLOTTITLES = ['Gyrometer Data', 'Accelerometer Data', 'Phase Variable']
		self.PLOTLIMS = [5,5,1]
		
		# packet loss attributes
		self.PERCENT_LOSS = 0
		self.NUMPACKETS = 0
		self.BADPACKETS = 0

		# bring in images to update the FSR relay display image
		self.legs = Image.open('legs.jpg')
		self.redC = Image.open('redCircle.png')
		self.greenC = Image.open('greenCircle.png')

		
		
		# init plot windows
		self.initializePlots(master)
		
		# init interactions (buttons, data entry, etc)
		self.initializeInteractions(master)
		
		# init updating textboxes
		self.TextFeedStringVar = StringVar(master, value = 'No connection\n')
		self.TextFeed = Message(master, textvar = self.TextFeedStringVar, relief = SUNKEN, width = 150, anchor = NW, justify = RIGHT)
		
		# recording to SD indicator
		self.loggingToSDLabel = Label(master, text = 'Logging Data:', font = LABELFONT)
		self.loggingToSDIndicator_StringVar = StringVar(master, value = "•")
		self.loggingToSDIndicator = Label(master, textvar = self.loggingToSDIndicator_StringVar, font = INDICATORFONT, fg = 'grey')
		
		# Serial Connection Indicator
		self.SerialConnectionLabel = Label(master,text="Serial Connected :",font=LABELFONT)
		self.SerialConnectionIndicator_StringVar = StringVar(master,value="•")
		self.SerialConnectionIndicator = Label(master,textvar=self.SerialConnectionIndicator_StringVar,font=INDICATORFONT,fg='grey')
		
		# grid layout assignments
		self.TextFeed.grid(row = 0, column = 0, columnspan = 1, rowspan = 2, sticky = 'NSWE')
		self.loggingToSDLabel.grid(row = 2, column = 0, sticky = 'NW')
		self.loggingToSDIndicator.grid(row = 2, column = 0, sticky = 'NE')
		self.SerialConnectionLabel.grid(row = 2, column = 0, sticky = 'W')
		self.SerialConnectionIndicator.grid(row = 2, column = 0, sticky = 'E')
		
		# set backgrounds to white 
		for widget in master.winfo_children():
			widget.config(background = backgroundColor)
			if len(widget.winfo_children()):
				for w in widget.winfo_children():
					w.config(background = backgroundColor)
					
		self.buttonStartTrial.config(fg = 'black', bg = 'green')
		self.buttonEndTrial.config(fg = 'black', bg = 'red')
		
		
		
	# Runs the mainloop function of tkinter 
	def mainloop(self):
		self.master.mainloop()
		return
		
		
	# connect to the specified serial port
	def connectToSerial(self):
		port = self.SERIAL_PORT.get()
		baudrate = 115200
		printtime('Attempting to connect to %s at %d baudrate'%(port, baudrate))
		
		try:
			self.ser = serial.Serial(port, baudrate, timeout = 0.1)
			self.ser.flushInput()
			printtime('Serial connection successful')
			self.TextFeedStringVar.set('Waiting')
			self.buttonStandby.config(state = NORMAL)
		except:
			printtime('Error connecting to serial')
			self.SetSerialConnectionLabel(0)
			return-1
		self.SetSerialConnectionLabel(1)
		self.IS_SERIAL_CONNECTED = True
		self.getSerialValues()
		return
		
	# disconnect form the serial if it is already connected
	def disconnectFromSerial(self):
		if self.IS_SERIAL_CONNECTED:
			self.ser.close()
			self.SetSerialConnectionLabel(0)
			self.IS_SERIAL_CONNECTED = False
			printtime('Disconnected from Serial')
			self.TextFeedStringVar.set('No connection')
		return
		
	# set the serial com port label
	def SetSerialConnectionLabel(self, connected):
		if connected:
			self.SerialConnectionIndicator_StringVar.set("•")
			self.SerialConnectionIndicator.config(fg='green')
		else:
			self.SerialConnectionIndicator_StringVar.set("•")
			self.SerialConnectionIndicator.config(fg = 'grey')
		return

	# set the logging label
	def setLoggingConnectionLabel(self, logging):
		if logging:
			self.loggingToSDIndicator_StringVar.set("•")
			self.loggingToSDIndicator.config(fg = 'green')
		else:
			self.loggingToSDIndicator_StringVar.set("•")
			self.loggingToSDIndicator.config(fg = 'grey')
		return


	# data collection and parsing*******************************************************************
	def getSerialValues(self):
		if not self.IS_SERIAL_CONNECTED:
			return
		try:
			self.ser.flushInput()
			self.ser.readline().decode('utf8')	# reads garbage
			rawdata = self.ser.readline().decode('utf8')	# actual reading
			updateDisp = False
			
			# split by the ';' delimiter
			groupValues = rawdata[:-1].split(';')
			
			# split each group of values by the ',' delimeter
			gyro = groupValues[0].split(',')
			accel = groupValues[1].split(',')
			phaseV = groupValues[2]
			self.OTHERDATA = groupValues[3].split(',')

			# check if the SD card is working and logging
			if self.OTHERDATA[6] == '1':
				self.setLoggingConnectionLabel(1)
			else:
				self.setLoggingConnectionLabel(0)

			# check if relay/fsr status has changed to update leg image
			for i in range(6):
				if self.OTHERDATA[i] == '1':
					self.FSRRELs[i] = True
				else:
					self.FSRRELs[i] = False

				if self.FSRRELs[i] != self.lastFSRRELs[i]:
					self.lastFSRRELs[i] = self.FSRRELs[i]
					updateDisp = True
			if updateDisp == True:
				updateDisp = False
				self.dispImages()
			
			# split up the gyro, accel, and phaseV into datastream objects
			for i in range(3):
				self.GYRODATASTREAM[i].pop(0)
				self.ACCELDATASTREAM[i].pop(0)

				self.GYRODATASTREAM[i].append(float(gyro[i]))
				self.ACCELDATASTREAM[i].append(float(accel[i]))

			self.PHASEDATASTREAM.pop(0)
			self.PHASEDATASTREAM.append(float(phaseV))
			self.master.after_idle(self.plotLine)  # updateValues()
		except:
			printtime('Error')

		self.master.after(1,self.getSerialValues)
		return
		
		
	
	# data visualization****************************************************************************
	def UpdateValues(self):
		self.plotLine()
		#self.updateTextFeed()
		return

	# initialize and display image
	def dispImages(self):
		self.redC = self.redC.resize((30, 15), Image.ANTIALIAS)
		self.greenC = self.greenC.resize((30, 15), Image.ANTIALIAS)
		#printtime(str(self.FSRRELs[0]) + '\t' + str(self.FSRRELs[1]))
		# update the FSR displays first
		for i in range(4):
			if self.FSRRELs[i] == False:
				self.legs.paste(self.redC, self.imgFSRlocs[i], self.redC.convert('RGBA'))
			else:
				self.legs.paste(self.greenC, self.imgFSRlocs[i], self.greenC.convert('RGBA'))
		
		RELlocs = [0,0]
		if self.AFFECTEDLIMB == 1:
			# affected limb is left
			RELlocs[0] = self.imgRELlocs[0]
			RELlocs[1] = self.imgRELlocs[1]
		else:
			# affected limb is right
			RELlocs[0] = self.imgRELlocs[2]
			RELlocs[1] = self.imgRELlocs[3]

		# update the relay displays
		for i in range(2):
			if self.FSRRELs[i+4] == False:
				self.legs.paste(self.redC, RELlocs[i], self.redC.convert('RGBA'))
			else:
				self.legs.paste(self.greenC, RELlocs[i], self.greenC.convert('RGBA'))
	

		self.tkimg = ImageTk.PhotoImage(self.legs)
		self.imgLabel = Label(image = self.tkimg)
		self.imgLabel.grid(row = 0, column = 1,  sticky = 'E', rowspan = 2, columnspan = 2)
		return

	def plotLine(self):
		# Plot Gyro Data*************************
		a1 = self.AXES[0]
		c1 = self.CANVASES[0]

		a1.clear()
		gx = self.GYRODATASTREAM[0]
		gy = self.GYRODATASTREAM[1]
		gz = self.GYRODATASTREAM[2]
		gxPlot, = a1.plot(gx, 'r', label = 'x')
		gyPlot, = a1.plot(gy, 'g', label = 'y')
		gzPlot, = a1.plot(gz, 'b', label = 'z')
		#a1.grid()
		a1.set_title('Gyroscope')
		a1.set_ylim([-1, 1])
		a1.set_xlim([0, 100])
		a1.legend(handles = [gxPlot, gyPlot, gzPlot], loc = 'upper left')
		c1.draw()

		# Plot Accel Data*************************
		a2 = self.AXES[1]
		c2 = self.CANVASES[1]

		a2.clear()
		ax = self.ACCELDATASTREAM[0]
		ay = self.ACCELDATASTREAM[1]
		az = self.ACCELDATASTREAM[2]
		axPlot, = a2.plot(ax, 'r', label = 'x')
		ayPlot, = a2.plot(ay, 'g', label = 'y')
		azPlot, = a2.plot(az, 'b', label = 'z')
		# a2.grid()
		a2.set_title('Accelerometer')
		a2.set_ylim([-0.5, 0.5])
		a2.set_xlim([0, 100])
		a2.legend(handles = [axPlot, ayPlot, azPlot], loc = 'upper left')
		c2.draw()

		# Plot Phase V Data**********************
		a3 = self.AXES[2]
		c3 = self.CANVASES[2]

		a3.clear()
		pv = self.PHASEDATASTREAM
		a3.plot(pv, 'r')
		#a3.grid()
		a3.set_title('Phase Variable')
		#a3.set_ylim([-0.2, 0.2])
		a3.set_xlim([0, 100])
		c3.draw()

		return
	

	# signal sending to Teensy**********************************************************************
	def sendSignal(self, signal):
		wstr = "%s\n"%(signal)
		try:
			self.ser.write(wstr.encode())
		except:
			printtime("Unable to send %s to serial."%(wstr[:-1]))
		return

	# interaction buttons***************************************************************************
	def buttonStandbyCommand(self):
		self.OPERATIONMODE = 1
		self.buttonTrialMode.config(state = NORMAL)
		self.buttonDebugMode.config(state = NORMAL)
		self.buttonPlantarOFF.config(state = DISABLED)
		self.buttonPlantarON.config(state = DISABLED)
		self.buttonDorsalOFF.config(state = DISABLED)
		self.buttonDorsalON.config(state = DISABLED)
		self.buttonStartTrial.config(state = DISABLED)
		self.buttonEndTrial.config(state = DISABLED)
		self.buttonFSRMode.config(state = DISABLED)
		self.buttonPHVMode.config(state = DISABLED)
		self.sendSignal('1')
		return

	def buttonTrialModeCommand(self):
		self.OPERATIONMODE = 2
		self.buttonPlantarOFF.config(state = DISABLED)
		self.buttonPlantarON.config(state = DISABLED)
		self.buttonDorsalOFF.config(state = DISABLED)
		self.buttonDorsalON.config(state = DISABLED)
		self.buttonStartTrial.config(state = DISABLED)
		self.buttonEndTrial.config(state = DISABLED)
		self.buttonFSRMode.config(state = DISABLED)
		self.buttonPHVMode.config(state = DISABLED)
		self.buttonLeftAff.config(state = NORMAL)
		self.buttonRightAff.config(state = NORMAL)
		self.sendSignal('2')
		return

	def buttonDebugModeCommand(self):
		self.OPERATIONMODE = 3
		self.buttonPlantarOFF.config(state = NORMAL)
		self.buttonPlantarON.config(state = NORMAL)
		self.buttonDorsalOFF.config(state = NORMAL)
		self.buttonDorsalON.config(state = NORMAL)
		self.buttonStartTrial.config(state = DISABLED)
		self.buttonEndTrial.config(state = DISABLED)
		self.buttonFSRMode.config(state = DISABLED)
		self.buttonPHVMode.config(state = DISABLED)
		self.buttonLeftAff.config(state = DISABLED)
		self.buttonRightAff.config(state = DISABLED)
		self.sendSignal('3')
		return

	def buttonFSRModeCommand(self):
		self.buttonStartTrial.config(state = NORMAL)
		self.buttonEndTrial.config(state = NORMAL)
		self.buttonPHVMode.config(state = DISABLED)
		self.sendSignal('21')
		return

	def buttonPHVModeCommand(self):
		self.buttonStartTrial.config(state = NORMAL)
		self.buttonEndTrial.config(state = NORMAL)
		self.buttonFSRMode.config(state = DISABLED)
		self.sendSignal('22')
		return

	def buttonStartTrialCommand(self):
		self.buttonStartTrial.config(state = DISABLED)
		self.buttonEndTrial.config(state = NORMAL)
		self.sendSignal('2s')
		return

	def buttonEndTrialCommand(self):
		self.buttonStartTrial.config(state = NORMAL)
		self.buttonEndTrial.config(state = DISABLED)
		self.sendSignal('2e')
		return

	def buttonLeftAffCommand(self):
		self.buttonFSRMode.config(state = NORMAL)
		self.buttonPHVMode.config(state = NORMAL)
		self.buttonRightAff.config(state = DISABLED)
		self.AFFECTEDLIMB = 1
		self.sendSignal('2a1')
		return

	def buttonRightAffCommand(self):
		self.buttonFSRMode.config(state = NORMAL)
		self.buttonPHVMode.config(state = NORMAL)
		self.buttonLeftAff.config(state = DISABLED)
		self.AFFECTEDLIMB = 2
		self.sendSignal('2a2')
		return

	def buttonDorsalONCommand(self):
		self.sendSignal('311')
		return
	
	def buttonDorsalOFFCommand(self):
		self.sendSignal('310')
		return

	def buttonPlantarONCommand(self):
		self.sendSignal('321')
		return
	
	def buttonPlantarOFFCommand(self):
		self.sendSignal('320')
		return

	def buttonSerialRefreshCommand(self):
		printtime("Refreshing serial ports.")
		if not ONLY_USE_BLUETOOTH_PORT:
			self.AvailablePorts = FindAllSerialPorts()
		# Refresh the serial port optionmenu
		try:
			menu = self.SerialPortOptionMenu['menu']
			menu.delete(0,"end")
			for port in self.AvailablePorts:
				menu.add_command(label=port)
		except:
			printtime("Error refreshing serial ports.")
			return

		return

	def buttonSerialConnectCommand(self):
		self.connectToSerial()
		return

	def buttonSerialDisconnectCommand(self):
		self.sendSignal('0')
		self.buttonStandby.config(state = DISABLED)
		self.buttonTrialMode.config(state = DISABLED)
		self.buttonDebugMode.config(state = DISABLED)
		self.buttonPlantarOFF.config(state = DISABLED)
		self.buttonPlantarON.config(state = DISABLED)
		self.buttonDorsalOFF.config(state = DISABLED)
		self.buttonDorsalON.config(state = DISABLED)
		self.buttonStartTrial.config(state = DISABLED)
		self.buttonEndTrial.config(state = DISABLED)
		self.buttonFSRMode.config(state = DISABLED)
		self.buttonPHVMode.config(state = DISABLED)
		self.disconnectFromSerial()
		return


	# initialize stuff******************************************************************************
	def initializeInteractions(self, master):
		self.dispImages()

		# FES control buttons
		self.FESbuttonsLabelFrame = LabelFrame(master, text = 'FES Control')
		
		self.buttonStandby = Button(self.FESbuttonsLabelFrame, text = 'Standby', command = self.buttonStandbyCommand)
		self.buttonTrialMode = Button(self.FESbuttonsLabelFrame, text  = 'Trial Mode', command = self.buttonTrialModeCommand)
		self.buttonDebugMode = Button(self.FESbuttonsLabelFrame, text = 'Debug Mode', command = self.buttonDebugModeCommand)
		
		self.buttonStandby.grid(row = 0, column = 0)
		self.buttonTrialMode.grid(row = 1, column = 0)
		self.buttonDebugMode.grid(row = 1, column = 1)

		# Trial mode control buttons
		self.TrialButtonsLabelFrame = LabelFrame(master, text = 'Trial Mode Control')

		self.buttonStartTrial = Button(self.TrialButtonsLabelFrame, text = 'Start Trial', command = self.buttonStartTrialCommand)
		self.buttonEndTrial = Button(self.TrialButtonsLabelFrame, text = 'End Trial', command = self.buttonEndTrialCommand)
		self.buttonFSRMode = Button(self.TrialButtonsLabelFrame, text = 'FSR Mode', command = self.buttonFSRModeCommand)
		self.buttonPHVMode = Button(self.TrialButtonsLabelFrame, text = 'Phase Variable', command = self.buttonPHVModeCommand)
		self.buttonLeftAff = Button(self.TrialButtonsLabelFrame, text = 'Left Leg', command = self.buttonLeftAffCommand)
		self.buttonRightAff = Button(self.TrialButtonsLabelFrame, text = 'Right Leg', command = self.buttonRightAffCommand)
		
		self.buttonLeftAff.grid(row = 0, column = 0)
		self.buttonRightAff.grid(row = 0, column = 1)
		self.buttonFSRMode.grid(row = 1, column = 0)
		self.buttonPHVMode.grid(row = 1, column = 1)
		self.buttonStartTrial.grid(row = 2, column = 0)
		self.buttonEndTrial.grid(row = 2, column = 1)
		

		# Debug mode control buttons
		self.DebugButtonsLabelFrame = LabelFrame(master, text = 'Debug Mode Control')
		
		self.buttonDorsalON = Button(self.DebugButtonsLabelFrame, text = 'Dorsal ON', command = self.buttonDorsalONCommand)
		self.buttonDorsalOFF = Button(self.DebugButtonsLabelFrame, text = 'Dorsal OFF', command = self.buttonDorsalOFFCommand)
		self.buttonPlantarON = Button(self.DebugButtonsLabelFrame, text = 'Plantar ON', command = self.buttonPlantarONCommand)
		self.buttonPlantarOFF = Button(self.DebugButtonsLabelFrame, text = 'Plantar OFF', command = self.buttonPlantarOFFCommand)
		
		self.buttonDorsalON.grid(row = 0, column = 0)
		self.buttonDorsalOFF.grid(row = 0, column = 1)
		self.buttonPlantarON.grid(row = 1, column = 0)
		self.buttonPlantarOFF.grid(row = 1, column = 1)

		# Serial control buttons
		self.SerialButtonsLabelFrame = LabelFrame(master, text = 'Serial Control')

		self.buttonSerialConnect = Button(self.SerialButtonsLabelFrame, text = 'Connect', command = self.buttonSerialConnectCommand)
		self.buttonSerialDisconnect = Button(self.SerialButtonsLabelFrame, text = 'Disconnect', command = self.buttonSerialDisconnectCommand)
		self.buttonSerialRefresh = Button(self.SerialButtonsLabelFrame, text = 'Refresh', command = self.buttonSerialRefreshCommand)
		        
		self.buttonSerialRefreshCommand()
		serialportinitval = self.AvailablePorts[0]
		self.SERIAL_PORT = StringVar(master,value=serialportinitval)
		if MANUAL_SERIAL_ENTRY: # Create an entry for manually typing serial values
			self.SerialPortEntry = Entry(self.SerialButtonsLabelFrame,textvariable=self.SERIAL_PORT)
			self.SerialPortEntry.grid(row=0,column=0)
		else:
			self.SerialPortOptionMenu = OptionMenu(self.SerialButtonsLabelFrame,self.SERIAL_PORT,*self.AvailablePorts)
			self.SerialPortOptionMenu.grid(row=0,column=0)

		self.buttonSerialConnect.grid(row = 2, column = 0)
		self.buttonSerialDisconnect.grid(row = 2, column = 2)
		self.buttonSerialRefresh.grid(row = 0, column = 2)

		
		# grid layout framework
		self.SerialButtonsLabelFrame.grid(row = 2, column = 1, sticky = 'NW')
		self.FESbuttonsLabelFrame.grid(row = 2, column = 2, columnspan = 1, sticky = 'NE')
		self.TrialButtonsLabelFrame.grid(row = 2, column = 1, columnspan = 1, sticky = 'SW')
		self.DebugButtonsLabelFrame.grid(row = 2, column = 2, columnspan = 1, sticky = 'SE')
		

		# start with all buttons except serial control off
		self.buttonPlantarOFF.config(state = DISABLED)
		self.buttonPlantarON.config(state = DISABLED)
		self.buttonDorsalOFF.config(state = DISABLED)
		self.buttonDorsalON.config(state = DISABLED)
		self.buttonStartTrial.config(state = DISABLED)
		self.buttonEndTrial.config(state = DISABLED)
		self.buttonStandby.config(state = DISABLED)
		self.buttonTrialMode.config(state = DISABLED)
		self.buttonDebugMode.config(state = DISABLED)
		self.buttonFSRMode.config(state = DISABLED)
		self.buttonPHVMode.config(state = DISABLED)
		self.buttonLeftAff.config(state = DISABLED)
		self.buttonRightAff.config(state = DISABLED)
		return

	def initializePlots(self, master):
		self.f1 = plt.figure(figsize = PLOTRATIO)#, dpi = PLOTDPI)
		self.a1 = self.f1.add_subplot(111)
		self.a1.grid()
		self.a1.set_title("Gyroscope")
		self.canvas1 = FigureCanvasTkAgg(self.f1, master)
		self.canvas1.get_tk_widget().grid(sticky = 'NW', row = 0, rowspan = 1, column = 3, columnspan = 2)

		self.f2 = plt.figure(figsize = PLOTRATIO)#, dpi = PLOTDPI)
		self.a2 = self.f2.add_subplot(111)
		self.a2.grid()
		self.a2.set_title("Accelerometer")
		self.canvas2 = FigureCanvasTkAgg(self.f2, master)
		self.canvas2.get_tk_widget().grid(sticky = 'NW', row = 1, rowspan = 1, column = 3, columnspan = 2)

		self.f3 = plt.figure(figsize = PLOTRATIO)#, dpi = PLOTDPI)
		self.a3 = self.f3.add_subplot(111)
		self.a3.grid()
		self.a3.set_title("Phase Variable")
		self.canvas3 = FigureCanvasTkAgg(self.f3, master)
		self.canvas3.get_tk_widget().grid(sticky = 'NW', row = 2, rowspan = 1, column = 3, columnspan = 2)

		self.AXES = [self.a1, self.a2, self.a3]
		self.CANVASES = [self.canvas1, self.canvas2, self.canvas3]
		return
# If running this as a script
if __name__ == '__main__':
	root = Tk()
	useGUI = FES(root)
	useGUI.mainloop()