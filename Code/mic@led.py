import RPi.GPIO as GPIO
import time
import board
import neopixel

# Configure the Neopixel ring
num_pixels = 120
pixel_pin = board.D18
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

# Define colors
white = (255, 255, 255)
lightgreen = (0, 255, 0)
green = (51, 204, 51)
darkgreen = (51, 102, 0)
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

Pin = 16

GPIO.setup(Pin, GPIO.IN)

try:
    while True:
        speakerInput = GPIO.input(Pin)
        if speakerInput == True:
            pixels.fill((200, 30, 30))  # Red color for Neopixel ring
            pixels.show()
        else:
			pixels.fill(0,0,0)
			pixels.show()
				
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

GPIO.cleanup()
