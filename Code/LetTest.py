#install rpi_ws281x
#!/usr/bin/python3

from rpi_ws281x import PixelStrip, Color

import time



LEDCOUNT = 2       # Number of LEDs

GPIOPIN = 18

FREQ = 800000

DMA = 5

INVERT = True       # Invert required when using inverting buffer

BRIGHTNESS = 255



# Intialize the library (must be called once before other functions).

strip = PixelStrip(LEDCOUNT, GPIOPIN, FREQ, DMA, INVERT, BRIGHTNESS)



strip.begin()



while True:

    # First LED white

    strip.setPixelColor(0, Color(255,255,255, 255))

    strip.setPixelColor(1, Color(0,0,0))

    strip.show()

    

    time.sleep(0.5)

    # Second LED white

    strip.setPixelColor(0, Color(0,0,0))

    strip.setPixelColor(1, Color(255,255,255, 255))

    strip.show()

    time.sleep(1)

    # LEDs Green

    strip.setPixelColor(0, Color(255,255,255, 255))

    strip.setPixelColor(1, Color(255,0,0))

    strip.show()

    time.sleep(0.5)

    # LEDs Red

    strip.setPixelColor(0, Color(0,255,0))

    strip.setPixelColor(1, Color(255,255,255, 255))

    strip.show()

    time.sleep(0.5)

    # LEDs Blue

    strip.setPixelColor(0, Color(255,255,255, 255))

    strip.setPixelColor(1, Color(0,0,255))

    strip.show()

    time.sleep(1)
