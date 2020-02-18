'''
# kivy imports
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout

# system and serial imports
import glob
import serial
from serial import Serial
import time
import sys

if getattr(sys,'frozen',False):
	application_path = path.dirname(sys.executable)
	chdir(application_path)

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
		print(port,end="")
		try:
			s = serial.Serial(port)
			s.close()
			result.append(port)
			print("...Good",end="")
		except:
			print("...",end="")
		print('')
	print("Done!")
	if len(result) == 0:
		result.append('NONE')
	
	return result

# Main widget

# graphing widgets

# leg visual widget

# serial control widget

# FES control widget

# Trial mode widget

# Debug mode widget


class MyPaintWidget(Widget):
    def __init__(self, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        #AsyncImage(source = 'legs.jpeg')


class FESapp(App):

    def build(self):
        root = GridLayout(cols = 2, rows = 3)
        self.painter = MyPaintWidget()
        img = AsyncImage(source = 'legs.jpeg')
        clearbtn = Button(text='Clear', pos_hint = (0,0))
        openbtn = Button(text = 'Hello', pos_hint = (1,0))
        clearbtn.bind(on_release=self.clear_canvas)
        root.add_widget(self.painter)
        root.add_widget(clearbtn)
        root.add_widget(openbtn)
        root.add_widget(img)
        return root

    def clear_canvas(self, obj):
        self.painter.canvas.clear()


if __name__ == '__main__':
    FESapp().run()

        


    

if __name__ == '__main__':
    FES().run()
'''
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage


class RootWidget(BoxLayout):
    pass


class CustomLayout(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(CustomLayout, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 1, 0, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class MainApp(App):

    def build(self):
        root = RootWidget()
        c = CustomLayout()
        root.add_widget(c)
        c.add_widget(
            AsyncImage(
                source="http://www.everythingzoomer.com/wp-content/uploads/2013/01/Monday-joke-289x277.jpg",
                size_hint= (1, .5),
                pos_hint={'center_x':.5, 'center_y':.5}))
        root.add_widget(AsyncImage(source='http://www.stuffistumbledupon.com/wp-content/uploads/2012/05/Have-you-seen-this-dog-because-its-awesome-meme-puppy-doggy.jpg'))
        c = CustomLayout()
        c.add_widget(
            AsyncImage(
                source="http://www.stuffistumbledupon.com/wp-content/uploads/2012/04/Get-a-Girlfriend-Meme-empty-wallet.jpg",
                size_hint= (1, .5),
                pos_hint={'center_x':.5, 'center_y':.5}))
        root.add_widget(c)
        return root

if __name__ == '__main__':
    MainApp().run()
