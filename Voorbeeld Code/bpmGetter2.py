import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs = 44100  
duration = 5

def getTotal(data):
    total = 0
    for i in range(len(data)):
        total += data[i]
    return total

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

with sd.Stream(channels=2, callback=callback):
    sd.sleep(int(duration * 1000))

print("Opnemen... druk ctrl+c om te stoppen")
audio_data = sd.Stream()