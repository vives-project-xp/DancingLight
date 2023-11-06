import RPi.GPIO as GPIO
import time
import board
import neopixel
# Configure the Neopixel ring
num_pixels = 120
pixel_pin = board.D18
Pin = 12
ORDER = neopixel.GRBW
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
GPIO.setup(Pin, GPIO.IN)
pixels.fill((255,255,255))
pixels.show()
