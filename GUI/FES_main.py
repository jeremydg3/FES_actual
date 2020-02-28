from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy_garden.graph import MeshLinePlot
import serial
from serial import Serial
import sys

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
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
			print("...Good",end="")
		except:
			print("...",end="")
		print('')
	if len(result) == 0:
		result.append('NONE')
	
	return result


# Window Classes**********************************************
class serialWindow(Screen):
    print('serial')



class calibrationWindow(Screen):
    ltval = ObjectProperty(None)
    lhval = ObjectProperty(None)
    rtval = ObjectProperty(None)
    rhval = ObjectProperty(None)

    def startFSRCalibration(self):
        print('starting calibration')

    def endFSRCalibration(self):
        print('calibration ended')

    def setFSRThresholds(self):
        print('thresholds set')


class debugWindow(Screen):
    print('debug')


class fesWindow(Screen):
    print('fes')


class WindowManager(ScreenManager):
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