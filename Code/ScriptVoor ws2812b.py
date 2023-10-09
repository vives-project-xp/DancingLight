#https://www.thegeekpub.com/16187/controlling-ws2812b-leds-with-a-raspberry-pi/
#eerst: sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel

import board
import neopixel
import time
pixels = neopixel.NeoPixel(board.D18, 30)

#eerste led rood maken
pixels[0] = (255, 0, 0)
sleep(1)

#eerste 10 leds groen maken
for x in range(0, 9):
    pixels[x] = (0, 255, 0)
    sleep(1)

#geen idee of dit script iets anders doet dan het ding die we al deden
#ook vreemd dat je in dit script niet frequentie en invert moet ingeven