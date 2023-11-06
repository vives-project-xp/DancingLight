import RPi.GPIO as GPIO
import time
import os

Pin = 16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Pin, GPIO.IN)

while(True):
    if GPIO.input(Pin):
        os.system("python3 aan.py")
        while(GPIO.input(Pin)):
            print("aan")
    else:
        os.system("python3 uit.py")
        while(GPIO.input(Pin)==False):
            print("uit")
GPIO.cleanup()
