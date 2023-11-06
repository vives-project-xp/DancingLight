import time
# import board
# import neopixel


# # Configure the Neopixel ring
# num_pixels = 120  # Number of Neopixels in your ring
# pixel_pin = board.D18  # GPIO pin connected to the data input of the Neopixel ring
# ORDER = neopixel.GRBW  # Change the order if your Neopixel ring uses a different order


# pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

# pixels.fill((0,0,0))
# pixels.show()

# # Define colors

# white = (255,255,255)
# lightgreen = (0,255,0)
# green = (51,204,51)
# darkgreen = (51,102,0)
# lightblue = (51, 204, 255)
# blue = (0, 102, 255)
# darkblue = (0, 0, 204)
# lightpurple = (153, 102, 255)
# purple = (204, 0, 255)
# darkpurple = (153, 0, 204)
# lightpink = (255, 102, 255)
# pink = (255, 0, 255)
# darkpink = (153, 0, 153)
# lightred = (255, 80, 80)
# red = (255, 0, 0)
# darkred = (204, 0, 0)
# lightorange = (255, 153, 102)
# orange = (255, 102, 0)
# lightyellow = (255, 255, 102)
# yellow = (255, 255, 0)
# kleuren = [white, lightgreen, green, darkgreen, lightblue, blue, darkblue, lightpurple, purple, darkpurple, lightpink, pink, darkpink, lightred, red, darkred, lightorange, orange, lightyellow, yellow]

# Sound logics
import pyaudio
import numpy as np

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

        # print(f'Frequentie: {rounded_frequency} Hz')
        # print("Average:   ", rounded_average, "Hz")
        # print("--------------------------")y
        time.sleep(0.1)

        if(rounded_frequency > 30000):
            print("----------")
        elif(rounded_frequency > 15000):
            print("---------")
        elif(rounded_frequency > 5000):
            print("--------")
        elif(rounded_frequency > 1000):
            print("-------")
        elif(rounded_frequency > 500):
            print("------")
        elif(rounded_frequency > 400):
            print("-----")
        elif(rounded_frequency > 300):
            print("----")
        elif(rounded_frequency > 200):
            print("---")
        elif(rounded_frequency > 100):
            print("--")
        


except KeyboardInterrupt:
    print("Opname gestopt.")

# Sluit de audio stream en PyAudio
stream.stop_stream()
stream.close()
p.terminate()









# Effects
# def Uit():
#     pixels.fill(0,0,0)
#     pixels.show()

# def Kleur(r, g, b):
#     pixels.fill(r, g, b)
#     pixels.show()

# def Rainbow():
#     kleurindex = 0
#     halvepixels = 0
#     extra = 0
#     while True:
#         for i in range(halvepixels):
#             pixels[60-halvepixels+i] = kleuren[(i+extra)%len(kleuren)]
#             pixels[59+halvepixels-i] = kleuren[(i+extra)%len(kleuren)]
#         time.sleep(0.01)
#         pixels.show()
#         if(halvepixels == 60):
#           extra += 1
#         else:
#           halvepixels += 1

# def KleurPerLeds():
#     while True:
#         kleur = (0,0,0)
#         kleur = kleuren[kleurindex]
        
#         if kleurindex == len(kleuren):
#             kleurindex = 0
            
#             for i in range(len(pixels)):
#                 color_index=(i // 3) % 3
#                 if color_index == 0:
#                     pixels[i] = kleur
#                 elif color_index == 1:
#                     pixels[i] = kleur
#                 else:
#                     pixels[i] = kleur
#                 pixels.show()
                
# def UitTrail():
#     ledsoff = 7
#     while True:
#         for i in range(len(pixels)):
#             pixels.fill(white)
#             pixels[i-ledsoff:i] = [(0,0,0)] * ledsoff
#             pixels.show()
            
# def MiddenBounce():
#     kleurindex = 0
#     aantal = int(num_pixels/2)
#     index = 0
#     while True:
#         kleur = kleuren[index]
#         for i in range(aantal):
#             pixel = len(pixels) - 1
#             pixels[pixel-i] = kleur
#             pixels[i] = kleur
#             pixels.show()
#         for i in range(aantal):
#             pixels[aantal+i] = (0,0,0)
#             pixels[aantal-i] = (0,0,0)
#             pixels.show()
#         index += 1
#         if index == len(kleuren):
#             index = 0
#         pixels.fill((0,0,0))
#         pixels.show()

# def Flag():
#     vlag = int(num_pixels/3)
#     while True:
#         for i in range(vlag):
#             pixels[i] = black
#             pixels[i+vlag] = yellow
#             pixels[i+2*vlag] = red
        
#         pixels.show()

# Rainbow()

