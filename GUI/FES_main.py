from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
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

connected = False
recording = False
GREEN = [0,1,0,0.5]
RED   = [1,0,0,0.5]

serialPort = 'NONE'


# Window Classes**********************************************
class serialWindow(Screen):
    result = ListProperty(['Select Port'])
    serialIndicatorC = ListProperty(RED)
    recordIndicatorC = ListProperty(RED)
    
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
        return

    def disconnectFromSerial(self):
        global connected
        #global serialIndicatorC
        if connected == True:
            self.ser.close()
            connected = False
            self.serialIndicatorC = RED
        print('disconnected')


class calibrationWindow(Screen):
    ltval = ObjectProperty(None)
    lhval = ObjectProperty(None)
    rtval = ObjectProperty(None)
    rhval = ObjectProperty(None)
    serialIndicatorC = ListProperty(RED)
    recordIndicatorC = ListProperty(RED)
    
    def updateIndicators(self):
        print('update')
        self.serialIndicatorC = ListProperty(RED)
        self.recordIndicatorC = ListProperty(RED)
        if connected:
            self.serialIndicatorC = ListProperty(GREEN)
        if recording:
            self.recordIndicatorC = ListProperty(GREEN)

    def startFSRCalibration(self):
        print('starting calibration')
        print(self.width/2.)

    def endFSRCalibration(self):
        print('calibration ended')

    def setFSRThresholds(self):
        print('thresholds set')


class debugWindow(Screen):
    if connected:
        serialIndicatorC = ListProperty(GREEN)
    else:
        serialIndicatorC = ListProperty(RED)

    if recording:
        recordIndicatorC = ListProperty(GREEN)
    else:
        recordIndicatorC = ListProperty(RED)
    print('debug')


class fesWindow(Screen):
    if connected:
        serialIndicatorC = ListProperty(GREEN)
    else:
        serialIndicatorC = ListProperty(RED)

    if recording:
        recordIndicatorC = ListProperty(GREEN)
    else:
        recordIndicatorC = ListProperty(RED)
    print('fes')


class WindowManager(ScreenManager):
    serialIndicatorC = ListProperty(RED)
    recordIndicatorC = ListProperty(RED)
    if connected:
        serialIndicatorC = ListProperty(GREEN)
    pass


# Load in the Kivy UI layout
kv = Builder.load_file('FES_UI.kv')

# Create a window manager
sm = ScreenManager()

# Add screen widgets to the window manager
screens = [serialWindow(name = 'serial'), calibrationWindow(name = 'calibration'), debugWindow(name = 'debug'), fesWindow(name = 'fes')]
for screen in screens:
    sm.add_widget(screen)

# Make the 'serial' screen the current screen to start
sm.current = 'serial'


# Main app loop
class mainApp(App):
    def build(self):
        return sm
            

# Run main app
if __name__ == '__main__':
    mainApp().run()