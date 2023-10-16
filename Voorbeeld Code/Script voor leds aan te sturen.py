import time
import board
import neopixel

# Configure the Neopixel ring
num_pixels = 12  # Number of Neopixels in your ring
pixel_pin = board.D18  # GPIO pin connected to the data input of the Neopixel ring
ORDER = neopixel.RGB  # Change the order if your Neopixel ring uses a different order

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

# Define colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Turn on the Neopixel ring with a color
pixels.fill(red)  # Change 'red' to 'green' or 'blue' to change the color
pixels.show()

# Delay for a few seconds
time.sleep(5)

# Turn off the Neopixel ring
pixels.fill((0, 0, 0))
pixels.show()