import RPi.GPIO as GPIO
import time

Pin = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Pin, GPIO.IN)

while(True):
    print('pin ', Pin, ' status = ', GPIO.input(Pin))

GPIO.cleanup()