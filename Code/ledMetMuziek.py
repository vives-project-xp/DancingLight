import time
import board
import neopixel

# Configure the Neopixel ring
num_pixels = 20  # Number of Neopixels in your ring
pixel_pin = board.D18  # GPIO pin connected to the data input of the Neopixel ring
ORDER = neopixel.GRBW  # Change the order if your Neopixel ring uses a different order

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

# Define colors

def SetLevel(i):
    if(i>255):
        return
    pixels.fill((i,i,i))
    pixels.show()



