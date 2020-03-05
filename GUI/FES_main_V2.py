from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy_garden.graph import MeshLinePlot
from kivy.graphics import *
from kivy.uix.spinner import Spinner
import serial
from serial import Serial
import sys
from threading import Thread

connected = False
recording = False
GREEN = [0,1,0,0.5]
RED   = [1,0,0,0.5]
GREENB = [0,1,0,1]
REDB = [1,0,0,1]
NOCOLOR = [0,0,0,0]
NPOINTS = 100

serialPort = 'NONE'

class mainScreen(FloatLayout):
    result = ListProperty(['Select Port'])
    serialIndicatorC = ListProperty(RED)
    recordIndicatorC = ListProperty(RED)
    leftToeC = ListProperty(REDB)
    leftHeelC = ListProperty(REDB)
    leftPlantarC = ListProperty(NOCOLOR)
    leftDorsiC = ListProperty(NOCOLOR)
    rightToeC = ListProperty(REDB)
    rightHeelC = ListProperty(REDB)
    rightPlantarC = ListProperty(NOCOLOR)
    rightDorsiC = ListProperty(NOCOLOR)
    AFFECTEDLIMB = 0
    recentlyConnected = False


    def __init__(self):
        super(mainScreen, self).__init__()
        self.GYRODATASTREAM = [[0 for points in range(NPOINTS)] for i in range(3)]
        self.ACCELDATASTREAM = [[0 for points in range(NPOINTS)] for i in range(3)]
        self.PHASEDATASTREAM = [0 for points in range(NPOINTS)]
        self.OTHERDATA = 0
        self.AFFECTEDLIMB = 0
        self.CONTROLMODE = 0
        self.plotGx = MeshLinePlot(color = [1,0,0,1])
        self.plotGy = MeshLinePlot(color = [0,1,0,1])
        self.plotGz = MeshLinePlot(color = [0,0,1,1])
        self.plotAx = MeshLinePlot(color = [1,0,0,1])
        self.plotAy = MeshLinePlot(color = [0,1,0,1])
        self.plotAz = MeshLinePlot(color = [0,0,1,1])
        self.plotP = MeshLinePlot(color = [1,0,0,1])
        self.ids.gyroPlot.add_plot(self.plotGx)
        self.ids.gyroPlot.add_plot(self.plotGy)
        self.ids.gyroPlot.add_plot(self.plotGz)
        self.ids.accelPlot.add_plot(self.plotAx)
        self.ids.accelPlot.add_plot(self.plotAy)
        self.ids.accelPlot.add_plot(self.plotAz)
        self.ids.phasePlot.add_plot(self.plotP)

    # This function comes graciously from StackOverflow
    # Finds all available serial ports, and returns as a list
    def FindAllSerialPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        self.result.clear()
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.result.append(port)
            except:
                t = 0
        if len(self.result) == 0:
            self.result.append('NONE')

    def setPort(self, serialport):
        global serialPort
        print(serialport)
        serialPort = serialport

    # connect to the specified serial port
    def connectToSerial(self):
        global connected
        baudrate = 115200
        try:
            self.ser = serial.Serial(serialPort, baudrate, timeout = 0.1)
            self.ser.flushInput()
        except:
            self.serialIndicatorC = RED
            connected = False
            print('Error connecting')
            return -1
        print('Connection successful')
        connected = True
        self.serialIndicatorC = GREEN
        if self.recentlyConnected == False:
            self.recentlyConnected = True
            
        Clock.schedule_interval(self.getValues, 0.001)
        return

    def disconnectFromSerial(self):
        global connected
        #global serialIndicatorC
        if connected == True:
            self.ser.close()
            connected = False
            self.serialIndicatorC = RED
            Clock.unschedule(self.getValues)
            self.recordIndicatorC = RED
            self.plantarC = NOCOLOR
            self.dorsiC = NOCOLOR
        print('disconnected')
        return

    def sendSerial(self, string):
        wstr = "%s\n"%(string)
        try:
            self.ser.write(wstr.encode())
            print(wstr)
        except:
            print("Unable to send %s to serial."%(wstr[:-1]))
            self.nothingSent(wstr, serialPort)
        return
    
    def getValues(self, dt):
        if connected:
            # Attempt to read in the serial data from Teensy
            try:
                self.ser.flushInput()
                self.ser.readline().decode('utf8')	# reads garbage
                rawdata = self.ser.readline().decode('utf8').strip()	# actual reading
                # split by the ';' delimiter
                groupValues = rawdata.split(';')

                # split each group of values by the ',' delimeter
                gyro = groupValues[0].split(',')
                accel = groupValues[1].split(',')
                phaseV = groupValues[2]
                self.OTHERDATA = groupValues[3].split(',')
                #print(self.OTHERDATA)
            except:
                print('error reading data')
            # 0.003,0.000,0.000;0.040,0.014,-0.200;0.00;0,0,0,0,1,1,0,3
            # 0.003,0.000,0.000;0.038,0.014,-0.201;0.00;0,0,0,0,0,1,0,2


            # Now attempt to parse the read data
            try:
                # check if the SD card is working and logging
                if self.OTHERDATA[6] == '1':
                    self.recordIndicatorC = GREEN
                else:
                    self.recordIndicatorC = RED
                # set FSR indicators
                # FSR1 (left) toe
                if self.OTHERDATA[0] == '1':self.leftToeC = GREENB
                else: self.leftToeC = REDB
                # FSR1 (left) heel
                if self.OTHERDATA[1] == '1':self.leftHeelC = GREENB
                else: self.leftHeelC = REDB
                # FSR1 (right) toe
                if self.OTHERDATA[2] == '1':self.rightToeC = GREENB
                else: self.rightToeC = REDB
                # FSR1 (right) heel
                if self.OTHERDATA[3] == '1':self.rightHeelC = GREENB
                else: self.rightHeelC = REDB
                
                if self.AFFECTEDLIMB == 1:
                    self.rightDorsiC = NOCOLOR
                    self.rightPlantarC = NOCOLOR
                    if self.OTHERDATA[4] == '1': self.leftDorsiC = GREENB
                    else: self.leftDorsiC = REDB
                    if self.OTHERDATA[5] == '1': self.leftPlantarC = GREENB
                    else: self.leftPlantarC = REDB
                elif self.AFFECTEDLIMB == 2:
                    self.leftDorsiC = NOCOLOR
                    self.leftPlantarC = NOCOLOR
                    if self.OTHERDATA[4] == '1': self.rightDorsiC = GREENB
                    else: self.rightDorsiC = REDB
                    if self.OTHERDATA[5] == '1': self.rightPlantarC = GREENB
                    else: self.rightPlantarC = REDB

                    
                for i in range(3):
                    self.GYRODATASTREAM[i].pop(0)
                    self.ACCELDATASTREAM[i].pop(0)

                    self.GYRODATASTREAM[i].append(float(gyro[i]))
                    self.ACCELDATASTREAM[i].append(float(accel[i]))

                self.PHASEDATASTREAM.pop(0)
                self.PHASEDATASTREAM.append(float(phaseV))
                self.plotLine()
            except:
                print('error parsing data')
        return

    def plotLine(self):
        # Plot Gyro Data*************************
        self.plotGx.points = [(i, self.GYRODATASTREAM[0][i]) for i in range(len(self.GYRODATASTREAM[0]))]
        self.plotGy.points = [(i, self.GYRODATASTREAM[1][i]) for i in range(len(self.GYRODATASTREAM[1]))]
        self.plotGz.points = [(i, self.GYRODATASTREAM[2][i]) for i in range(len(self.GYRODATASTREAM[2]))]
        self.plotAx.points = [(i, self.ACCELDATASTREAM[0][i]) for i in range(len(self.ACCELDATASTREAM[0]))]
        self.plotAy.points = [(i, self.ACCELDATASTREAM[1][i]) for i in range(len(self.ACCELDATASTREAM[1]))]
        self.plotAz.points = [(i, self.ACCELDATASTREAM[2][i]) for i in range(len(self.ACCELDATASTREAM[2]))]
        self.plotP.points = [(i, self.PHASEDATASTREAM[i]) for i in range(len(self.PHASEDATASTREAM))]
        return

    def nothingSent(self, val, comm):
        pop = Popup(title = 'No Serial Connected', content = Label(text = 'Could not send "%s" to "%s", check serial connection. \nPress ESC to return or click main window'%(val[:-1], comm)), size_hint = (None, None), size = (400, 200))
        pop.open()

# Load in the Kivy UI layout
kv = Builder.load_file('FES_UI_V2.kv')

# Main app loop
class mainApp(App):
    def build(self):
        return mainScreen()
            

# Run main app
if __name__ == '__main__':
    mainApp().run()