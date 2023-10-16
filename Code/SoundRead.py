import sounddevice as sd
import soundfile as sf
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

fs = 44100
duration = 3

print("Opnemen van voice data gedurende 3 seconden...")
audio_data = sd.rec(int(fs * duration), samplerate=fs, channels=2, blocking=True)


print("Afspelen van opgenomen geluidsfragment...")
sd.play(audio_data, fs)
sd.wait()

sf.write('test.wav', audio_data, fs)

sample_rate, audio_data = wavfile.read('test.wav')
channel = audio_data[:, 0]

plt.figure(figsize=(12, 5))
plt.plot(channel, color='black')
plt.title('Frequentie sample')
plt.xlabel('Tijd')
plt.ylabel('Frequentie')
plt.grid(True)

plt.tight_layout()
plt.show()
