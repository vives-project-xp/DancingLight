import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt

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
    plt.ion()  # Enable interactive mode for real-time plotting
    fig, ax_low = plt.subplots(1, 1)
    fig, ax_high = plt.subplots(1, 1)
    x = np.arange(0, chunk_size)
    line_low, = ax_low.plot(x, np.zeros(chunk_size))
    line_high, = ax_high.plot(x, np.zeros(chunk_size))
    ax_low.set_xlim(0, chunk_size)
    ax_high.set_xlim(0, chunk_size)
    ax_low.set_ylim(-2500, 2500)
    ax_high.set_ylim(-40000, 40000)
    
    # Set the desired duration (e.g., 60 seconds)
    runtime = 3600  # Duration in seconds
    start_time = time.time()
    
    while time.time() - start_time < runtime:
        # Read audio from the microphone
        audio_data = np.frombuffer(stream.read(chunk_size), dtype=np.int16)
        
        # Calculate the frequency
        frequency = calculate_frequency(audio_data, sample_rate)
        
        # Plot the audio data based on frequency
        line_low.set_ydata(audio_data)
        line_high.set_ydata(audio_data)
        ax_low.set_title(f'Low Frequency Sound: {frequency:.2f} Hz')
        ax_high.set_title(f'High Frequency Sound: {frequency:.2f} Hz')
        
        fig.canvas.flush_events()
        
except KeyboardInterrupt:
    print("Recording stopped.")

# Close the audio stream and PyAudio
stream.stop_stream()
stream.close()
p.terminate()

# Close Matplotlib
plt.ioff()
plt.show()
