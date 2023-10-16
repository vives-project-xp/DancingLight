import pyaudio
import numpy as np
import time
import matplotlib.pyplot as plt

# Functie om de frequentie te berekenen
def calculate_frequency(signal, sample_rate):
    fft_result = np.fft.fft(signal)
    magnitude = np.abs(fft_result)
    frequency = np.argmax(magnitude) * sample_rate / len(signal)
    return frequency

# Initialisatie van PyAudio
p = pyaudio.PyAudio()

# Audio-instellingen
sample_rate = 44100  # Aanpassen naar de gewenste sample rate
chunk_size = 1024

# Het creëren van een audio input stream
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True,
                frames_per_buffer=chunk_size)

try:
    plt.ion()  # Schakel interactieve modus in voor realtime plotten
    fig, ax = plt.subplots()
    x = np.arange(0, chunk_size)
    line, = ax.plot(x, np.zeros(chunk_size))
    ax.set_xlim(0, chunk_size)
    ax.set_ylim(-32768, 32767)
    
    # Stel de gewenste looptijd in (bijvoorbeeld 60 seconden)
    runtime = 60  # Duur in seconden
    start_time = time.time()
    
    while time.time() - start_time < runtime:
        # Lees audio van de microfoon
        audio_data = np.frombuffer(stream.read(chunk_size), dtype=np.int16)
        
        # Bereken de frequentie
        frequency = calculate_frequency(audio_data, sample_rate)
        
        # Druk de frequentie af
        print(f'Frequentie: {frequency:.2f} Hz')
        
        # Plot de audiogegevens
        line.set_ydata(audio_data)
        fig.canvas.flush_events()
        
except KeyboardInterrupt:
    print("Opname gestopt.")

# Sluit de audio stream en PyAudio
stream.stop_stream()
stream.close()
p.terminate()

# Sluit Matplotlib
plt.ioff()
plt.show()
