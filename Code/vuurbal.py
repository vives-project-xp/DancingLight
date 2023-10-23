import time
import random
import math
import board
import neopixel

num_pixels = 120  # Number of Neopixels in your ring
pixel_pin = board.D18  # GPIO pin connected to the data input of the Neopixel ring
ORDER = neopixel.GRBW  # Change the order if your Neopixel ring uses a different order


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

pixels.fill((0,0,0))
pixels.show()

Levels = [(50,0,0),(100,0,0),(150,0,0),(200,0,0),(255,0,0)]
sizes = [1,2,3,4,5,4,3,2,1]

rows = 12
colums = 10
ywaarde=4
xwaarde=4
middelindex = math.floor(len(sizes)/2)
#random.seed(69)
while True:
    for height in range(9):
        ba = 0
        for i in range(-(sizes[height] -1), sizes[height]):
            if(xwaarde+i >= 0 and xwaarde+i < colums):
                pixels[xwaarde+i, ywaarde+(height+middelindex-height)] = Levels[ba]
            if i > 0:
                ba -= 1
            else:
                ba += 1
    pixels.show()
    xwaarde += 1
    time.sleep(5)

