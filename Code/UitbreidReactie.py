import RPi.GPIO as GPIO
import time
import board
import neopixel
import pyaudio
import time
from math import log10
import audioop  
import sys

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

kleurlevels = [(20,20,20),(50,20,20),(140,20,20),(255,20,20),(20,50,20),(20,140,20),(20,255,20),(20,20,50),(20,20,140),(20,20,255)]#10 levels in totaal
#oke we zitten met een matrix van 8x4
while stream.is_active(): 
	db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
	geluidIndexMidden = round(((db+40)/10)%1*11)-1#van -1 tot 10
	#print(geluidIndexMidden)
	for j in range(3):
		color = (0,0,0)
		#print(geluidIndexMidden-j)
		if geluidIndexMidden-j >= 0 and geluidIndexMidden-j < 10:
			color = kleurlevels[geluidIndexMidden-j]
		for i in range(8):
			pixels[i*8+3-j] = color
			pixels[i*8+4+j] = color
	pixels.show()

pixels.fill((0,0,0))
pixels.show()

stream.stop_stream()
stream.close()

p.terminate()
GPIO.cleanup()
