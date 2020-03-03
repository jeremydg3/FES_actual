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
NPOINTS = 100

serialPort = 'NONE'

class mainScreen(FloatLayout):
    result = ListProperty(['Select Port'])
    serialIndicatorC = ListProperty(RED)
    recordIndicatorC = ListProperty(RED)

    def __init__(self):
        super(mainScreen, self).__init__()
        self.GYRODATASTREAM = [[0 for points in range(NPOINTS)] for i in range(3)]
        self.ACCELDATASTREAM = [[0 for points in range(NPOINTS)] for i in range(3)]
        self.PHASEDATASTREAM = [0 for points in range(NPOINTS)]
        self.plotGx = MeshLinePlot(color = [1,0,0,1])
        self.plotGy = MeshLinePlot(color = [0,1,0,1])
        self.plotGz = MeshLinePlot(color = [0,0,1,1])
        self.plotAx = MeshLinePlot(color = [1,0,0,1])
        self.plotAy = MeshLinePlot(color = [0,1,0,1])
        self.plotAz = MeshLinePlot(color = [0,0,1,1])
        self.plotP = MeshLinePlot(color = [1,0,0,1])

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
        self.ids.gyroPlot.add_plot(self.plotGx)
        self.ids.gyroPlot.add_plot(self.plotGy)
        self.ids.gyroPlot.add_plot(self.plotGz)
        self.ids.accelPlot.add_plot(self.plotAx)
        self.ids.accelPlot.add_plot(self.plotAy)
        self.ids.accelPlot.add_plot(self.plotAz)
        self.ids.phasePlot.add_plot(self.plotP)
        Clock.schedule_interval(self.getValues, 0.001)
        return

    def disconnectFromSerial(self):
        global connected
        #global serialIndicatorC
        if connected == True:
            self.ser.close()
            connected = False
            self.serialIndicatorC = RED
            Clock.unschedule(self.plotLine)
        print('disconnected')
    
    def getValues(self, dt):
        if connected:
            try:
                self.ser.flushInput()
                self.ser.readline().decode('utf8')	# reads garbage
                rawdata = self.ser.readline().decode('utf8')	# actual reading
                
                # split by the ';' delimiter
                groupValues = rawdata[:-1].split(';')
                
                # split each group of values by the ',' delimeter
                gyro = groupValues[0].split(',')
                accel = groupValues[1].split(',')
                phaseV = groupValues[2]
                #self.OTHERDATA = groupValues[3].split(',')
                for i in range(3):
                    self.GYRODATASTREAM[i].pop(0)
                    self.ACCELDATASTREAM[i].pop(0)

                    self.GYRODATASTREAM[i].append(float(gyro[i]))
                    self.ACCELDATASTREAM[i].append(float(accel[i]))

                self.PHASEDATASTREAM.pop(0)
                self.PHASEDATASTREAM.append(float(phaseV))
                self.plotLine()
            except:
                print('error')
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


# Load in the Kivy UI layout
kv = Builder.load_file('FES_UI_V2.kv')

# Main app loop
class mainApp(App):
    def build(self):
        return mainScreen()
            

# Run main app
if __name__ == '__main__':
    mainApp().run()