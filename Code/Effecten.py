import time
import board
import neopixel


# Configure the Neopixel ring
num_pixels = 120  # Number of Neopixels in your ring
pixel_pin = board.D18  # GPIO pin connected to the data input of the Neopixel ring
ORDER = neopixel.GRBW  # Change the order if your Neopixel ring uses a different order


pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

pixels.fill((0,0,0))
pixels.show()

# Define colors

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

def Uit():
    pixels.fill(0,0,0)
    pixels.show()

def Kleur(r, g, b):
    pixels.fill(r, g, b)
    pixels.show()

def Rainbow():
    kleurindex = 0
    halvepixels = 0
    extra = 0
    while True:
        for i in range(halvepixels):
            pixels[60-halvepixels+i] = kleuren[(i+extra)%len(kleuren)]
            pixels[59+halvepixels-i] = kleuren[(i+extra)%len(kleuren)]
        time.sleep(0.01)
        pixels.show()
        if(halvepixels == 60):
          extra += 1
        else:
          halvepixels += 1

def KleurPerLeds():
    while True:
        kleur = (0,0,0)
        kleur = kleuren[kleurindex]
        
        if kleurindex == len(kleuren):
            kleurindex = 0
            
            for i in range(len(pixels)):
                color_index=(i // 3) % 3
                if color_index == 0:
                    pixels[i] = kleur
                elif color_index == 1:
                    pixels[i] = kleur
                else:
                    pixels[i] = kleur
                pixels.show()
                
def UitTrail():
    ledsoff = 7
    while True:
        for i in range(len(pixels)):
            pixels.fill(white)
            pixels[i-ledsoff:i] = [(0,0,0)] * ledsoff
            pixels.show()
            
def MiddenBounce():
    kleurindex = 0
    aantal = int(num_pixels/2)
    index = 0
    while True:
        kleur = kleuren[index]
        for i in range(aantal):
            pixel = len(pixels) - 1
            pixels[pixel-i] = kleur
            pixels[i] = kleur
            pixels.show()
        for i in range(aantal):
            pixels[aantal+i] = (0,0,0)
            pixels[aantal-i] = (0,0,0)
            pixels.show()
        index += 1
        if index == len(kleuren):
            index = 0
        pixels.fill((0,0,0))
        pixels.show()

def Flag():
    vlag = int(num_pixels/3)
    while True:
        for i in range(vlag):
            pixels[i] = black
            pixels[i+vlag] = yellow
            pixels[i+2*vlag] = red
        
        pixels.show()

Rainbow()

