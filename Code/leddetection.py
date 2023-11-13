import board
import neopixel
import RPi.GPIO as GPIO
import time

# GPIO pin connected to the data input of the first LED strip
pixel_pin = board.D18

# GPIO pin connected to the presence detection of the LED strips
strip_presence_pins = [23, 24]  # Replace with the actual GPIO pins connected to each strip

leds_per_strip = 60  # LEDs on one strip

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    for pin in strip_presence_pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def detect_total_length():
    total_length = 0
    for pin in strip_presence_pins:
        if GPIO.input(pin) == GPIO.LOW:
            total_length += leds_per_strip

    return total_length

def cleanup_gpio():
    GPIO.cleanup()

try:
    setup_gpio()

    # Calculate the total length of LED strips
    total_length = detect_total_length()

    # Print the result
    print(f'Total length of LED strips: {total_length} LEDs')

finally:
    cleanup_gpio()
