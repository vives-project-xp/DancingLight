import soundfile as sf
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from scipy import signal


# Read the audio file
audio_data, fs = sf.read('test.wav')

# Plot the audio waveform
time = np.arange(0, audio_data.shape[0]) / fs
plt.figure(figsize=(12, 6))
for i in range(audio_data.shape[1]):
    plt.subplot(audio_data.shape[1], 1, i+1)
    plt.plot(time, audio_data[:, i], label=f'Channel {i+1}')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()

plt.tight_layout()
plt.show()
