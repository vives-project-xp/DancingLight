import RPi.GPIO as GPIO
import time
import board
import neopixel
import pyaudio
import time
from math import log10
import audioop  
import sys
import datetime

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 1
print(p.get_default_input_device_info())

def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue

white = (255,255,255)
lightgreen = (0,255,0)
green = (51,204,51)
darkgreen = (51,102,0)
lightblue = (51, 204, 255)
blue = (0, 102, 255)
darkblue = (0, 0, 204)
lightpurple = (153, 102, 255)
purple = (204, 0, 255)
darkpurple = (153, 0, 204)
lightpink = (255, 102, 255)
pink = (255, 0, 255)
darkpink = (153, 0, 153)
lightred = (255, 80, 80)
red = (255, 0, 0)
darkred = (204, 0, 0)
lightorange = (255, 153, 102)
orange = (255, 102, 0)
lightyellow = (255, 255, 102)
yellow = (255, 255, 0)
kleuren = [white, lightgreen, green, darkgreen, lightblue, blue, darkblue, lightpurple, purple, darkpurple, lightpink, pink, darkpink, lightred, red, darkred, lightorange, orange, lightyellow, yellow]

stream = p.open(format=p.get_format_from_width(WIDTH),
	input_device_index=DEVICE,
	channels=1,
	rate=RATE,
	input=True,
	output=False,
	stream_callback=callback)

stream.start_stream()

# Configure the Neopixel ring
num_pixels = 120
pixel_pin = board.D18
Pin = 12
ORDER = neopixel.GRBW
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
GPIO.setup(Pin, GPIO.IN)

minste = 0
meeste = 1
recentmeeste = 0
recentminste = 0
nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)	#5 seconden vanaf nu
index = 0
verander = False

while stream.is_active(): 
	db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
	positf = ((db+40))
	if(positf<minste):
		minste = positf
		print("nieuw kleinste:",minste)
	if(positf>meeste):	#er is een bug waarbij positif 40 is bij eerste iteratie, ook is 40 de maximuum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
		if positf == 40:
			positf = meeste
		meeste = positf
		print("nieuw hoogste:", meeste)
	if(positf<recentminste):
		recentminste = positf
	if(positf>recentmeeste):	#er is een bug waarbij positif 40 is bij eerste iteratie, ook is 40 de maximuum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
		if positf == 40:
			positf = recentmeeste
		recentmeeste = positf
	if(datetime.datetime.now() > nieuwcheckinterval):
		print("nieuwe max-min:",recentmeeste,"-",recentminste)
		meeste = recentmeeste
		minste = recentminste
		nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)
		recentminste = positf
		recentmeeste = positf
	filled_progbar  = round((positf-minste)/(meeste-minste))
	if filled_progbar> 0.5 and verander == False:
		verander = True
		index += 1
		pixels.fill(kleuren[index%len(kleuren)])
		pixels.show()
	if(filled_progbar < 0.5):
		verander = False


stream.stop_stream()
stream.close()

p.terminate()
GPIO.cleanup()
