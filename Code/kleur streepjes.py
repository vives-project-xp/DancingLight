import time
import random
import math
import board
import neopixel
import dequeue

num_pixels = 120  # Number of Neopixels in your ring
pixel_pin = board.D18  # GPIO pin connected to the data input of the Neopixel ring
ORDER = neopixel.GRBW  # Change the order if your Neopixel ring uses a different order


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

pixels.fill((0,0,0))
pixels.show()

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

rows = 12
colums = 10

class streepje:
    kleur
    richting    #-1 is naar links (naar de 0 toe), 1 is naar rechts (rechter grens toe)
    curpos

#random.seed(69)
streepjes = dequeue()
while True:
    #alle streepjes bewegen
    #pixels legen
    for i in range(colums*rows):
        pixels[i] = (0,0,0)
    popcount = 0
    verwijderbaar = True
    for strip in streepje:
        #tekenen van lijntje
        for i in range(strip, strip+rows):
        pixels[i] = strip.kleur

        strip.curpos += rows*richting
        if verwijderbaar:
            if (curpos==0 and richting==-1) or (curpos==colums*rows):
                popcount += 1
            else: 
                verwijderbaar = False
    for i in range(popcount):
        streepje.popleft()
    #soms streepje genereren
    if randint(1, 10) == 5:
        seter = streepje()
        seter.kleur = kleuren[randint(0,len(kleuren)-1)]
        if(randint(1,2) == 1):
            seter.richting = 1
            seter.curpos = 0
        else:
            seter.richting = -1
            seter.curpos = (colums-1)*rows
        streepje.append(seter)
    pixels.show()
    time.sleep(0.4)

