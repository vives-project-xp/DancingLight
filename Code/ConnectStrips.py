import board
import neopixel
import time

# Define and configurate LED's strips
led_pin_1 = board.D18  # Pin first Led-strip
led_pin_2 = board.D12  # Pin second Led-strip
num_leds_per_strip = 60  # Amount of LED's in 1 strip

#Turn every LED on
strip1 = neopixel.NeoPixel(led_pin_1, num_leds_per_strip, auto_write=False)
strip2 = neopixel.NeoPixel(led_pin_2, num_leds_per_strip, auto_write=False)

# Function to give every LED a color
def color_wipe(strip, color, wait):
    for i in range(len(strip)):
        strip[i] = color
        strip.show()
        time.sleep(wait)

# Put all LED's on red
color_wipe(strip1, (255, 0, 0), 0.1)  # Red
color_wipe(strip2, (255, 0, 0), 0.1)  # Red
