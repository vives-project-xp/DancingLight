import pyaudio
import time
from math import log10
import audioop  
import sys

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 1
print(p.get_default_input_device_info())

def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue


stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=DEVICE,
                channels=1,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)

stream.start_stream()

while stream.is_active(): 
    db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
    #print(f"RMS: {rms} DB: {db}") 
    barChars = 40#https://geekyisawesome.blogspot.com/2016/07/python-console-progress-bar-using-b-and.html
    filled_progbar  = round(((db+40)/40)*barChars)
    print('#'*filled_progbar + '-'*(barChars-filled_progbar))
    

stream.stop_stream()
stream.close()

p.terminate()
