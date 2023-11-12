import board
import neopixel
import time

# Definieer de configuratie van de ledstrips
led_pin_1 = board.D18  # Pin voor de eerste ledstrip
led_pin_2 = board.D12  # Pin voor de tweede ledstrip
num_leds_per_strip = 60  # Aantal leds per ledstrip

# Maak de Neopixel-objecten aan voor elke ledstrip
strip1 = neopixel.NeoPixel(led_pin_1, num_leds_per_strip, auto_write=False)
strip2 = neopixel.NeoPixel(led_pin_2, num_leds_per_strip, auto_write=False)

# Functie om alle leds op een strip een bepaalde kleur te geven
def color_wipe(strip, color, wait):
    for i in range(len(strip)):
        strip[i] = color
        strip.show()
        time.sleep(wait)

# Voorbeeld: Alle leds op beide strips rood maken
color_wipe(strip1, (255, 0, 0), 0.1)  # Rood
color_wipe(strip2, (255, 0, 0), 0.1)  # Rood
