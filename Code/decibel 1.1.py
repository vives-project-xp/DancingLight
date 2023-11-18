import pyaudio
import time
from math import log10
import audioop  
import datetime

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

minste = 0
meeste = 1
recentmeeste = 0
recentminste = 0
nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)	#5 seconden vanaf nu

while stream.is_active(): 
    db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
    #print(f"RMS: {rms} DB: {db}") 
    barChars = 40#https://geekyisawesome.blogspot.com/2016/07/python-console-progress-bar-using-b-and.html
    positf = ((db+40))
    if positf<minste:
        minste = positf
        print("nieuw kleinste:",minste)
    if(positf>meeste):	#er is een bug waarbij positif 40 is bij eerste iteratie, ook is 40 de maximuum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
        if positf == 40:
            positf = meeste
        meeste = positf
        print("nieuw hoogste:", meeste)
    if(positf<recentminste):
        recentminste = positf
    if(positf>recentmeeste):	#er is een bug waarbij positif 40 is bij eerste iteratie, ook is 40 de maximuum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
        if positf == 40:
            positf = recentmeeste
        recentmeeste = positf
    if(datetime.datetime.now() > nieuwcheckinterval):
        print("nieuwe max-min:",recentmeeste,"-",recentminste)
        meeste = recentmeeste
        minste = recentminste
        nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)
        recentminste = positf
        recentmeeste = positf
    filled_progbar  = round((positf-minste)/(meeste-minste)*barChars)
    print('#'*filled_progbar + '-'*(barChars-filled_progbar))
    

stream.stop_stream()
stream.close()

p.terminate()
