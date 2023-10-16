import librosa
import matplotlib.pyplot as plt

# Load the WAV file
wav_file = "test.wav"
audio_array, sample_rate = librosa.load(wav_file)

# Compute the STFT of the audio signal
stft = librosa.core.stft(audio_array)

# Compute the spectrogram
spectrogram = librosa.core.amplitude_to_db(stft)

# Plot the spectrogram
plt.imshow(spectrogram)
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")
plt.title("Spectrogram of WAV file")
plt.show()
