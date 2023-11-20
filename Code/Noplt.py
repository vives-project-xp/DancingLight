import pyaudio
import numpy as np
import time

# Function to calculate the frequency
def calculate_frequency(signal, sample_rate):
    fft_result = np.fft.fft(signal)
    magnitude = np.abs(fft_result)
    frequency = np.argmax(magnitude) * sample_rate / len(signal)
    return frequency

# Initialization of PyAudio
p = pyaudio.PyAudio()

# Audio settings
sample_rate = 44100  # Adjust to your desired sample rate
chunk_size = 1024

# Create an audio input stream
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True,
                frames_per_buffer=chunk_size)

try:
    # Set the desired duration (e.g., 60 seconds)
    runtime = 3600  # Duration in seconds
    start_time = time.time()
    
    while time.time() - start_time < runtime:
        # Read audio from the microphone
        audio_data = np.frombuffer(stream.read(chunk_size), dtype=np.int16)
        
        # Calculate the frequency
        frequency = calculate_frequency(audio_data, sample_rate)
        
        # Print the frequency to the console
        print(f'Current Frequency: {frequency:.2f} Hz')
        
except KeyboardInterrupt:
    print("Recording stopped.")

# Close the audio stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()
