import pyaudio
import numpy as np
import time

frArr = []
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
    while True:
        # Lees audio van de microfoon
        audio_data = np.frombuffer(stream.read(chunk_size), dtype=np.int16)
        
        # Bereken de frequentie
        frequency = calculate_frequency(audio_data, sample_rate)
        frArr.append(frequency)
        # Wacht 10 ms
        average = np.mean(frArr)
        rounded_average = round(average)
        rounded_frequency = round(frequency)
        # Druk de frequentie af
        print(f'Frequentie: {rounded_frequency} Hz')
        print("Average:   ", rounded_average, "Hz")
        print("--------------------------")
        time.sleep(0.1)



except KeyboardInterrupt:
    print("Opname gestopt.")

# Sluit de audio stream en PyAudio
stream.stop_stream()
stream.close()
p.terminate()

