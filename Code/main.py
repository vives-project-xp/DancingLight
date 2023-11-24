import paho.mqtt.client as mqttClient
import time
import threading
import RPi.GPIO as GPIO
import board
import neopixel
import datetime
from math import log10
import audioop
import pyaudio

t1 = threading.Thread()
messages = []
booleans = [False, True]#running, stoped

def on_message(client, userdata, message):
    bericht = str(message.payload.decode("utf-8"))
    messages.append(bericht)
    print(messages)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
  
        print("Connected to broker")
  
        global Connected                #Use global variable
        Connected = True                #Signal connection 
  
    else:
  
        print("Connection failed")

def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue

# Configure the Neopixel ring
num_pixels = 64
pixel_pin = board.D18
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

# Define colors
colors = [
    (255, 255, 255),    # White
    (0, 255, 0),        # Light Green
    (51, 204, 51),      # Green
    (51, 102, 0),       # Dark Green
    (51, 204, 255),     # Light Blue
    (0, 102, 255),      # Blue
    (0, 0, 204),        # Dark Blue
    (153, 102, 255),    # Light Purple
    (204, 0, 255),      # Purple
    (153, 0, 204),      # Dark Purple
    (255, 102, 255),    # Light Pink
    (255, 0, 255),      # Pink
    (153, 0, 153),      # Dark Pink
    (255, 80, 80),      # Light Red
    (255, 0, 0),        # Red
    (204, 0, 0),        # Dark Red
    (255, 153, 102),    # Light Orange
    (255, 102, 0),     # Orange
    (255, 255, 102),   # Light Yellow
    (255, 255, 0)      # Yellow
]
Pin = 16

GPIO.setup(Pin, GPIO.IN)

def rainbow():
    kleurindex = 0
    halvepixels = 0
    extra = 0
    while True:
        for i in range(halvepixels):
            pixels[60-halvepixels+i] = kleuren[(i+extra)%len(kleuren)]
            pixels[59+halvepixels-i] = kleuren[(i+extra)%len(kleuren)]
        time.sleep(0.01)
        pixels.show()
        if(halvepixels == 60):
          extra += 1
        else:
          halvepixels += 1
        if(booleans[0] == False):
            break
    booleans[1] = True

def allLights():
    pixels.fill(kleuren[0])
    booleans[1] = True

def anyColor(r, g, b, r2, g2, b2):
    for i in range(0, num_pixels/2):
        pixels[i] = (r, g, b)
    
    for i in range(num_pixels/2, num_pixels):
        pixels[i] = (r2, g2, b2)
    pixels.show()
    booleans[1] = True

def pulseColor(r, g, b):
    pixels.fill((r,g,b))
    while(True):
        for i in range(0, 255):
            pixels.setBrightness(i)
        for i in range(255,0):
            pixels.setBrightness(i)
        if(booleans[0] == False):
            break
    booleans[1] = True

Connected = False   #global variable for the state of the connection
  
broker_address= "test.mosquitto.org" #"projectmaster.devbit.be"  #Broker address
port = 1883               #Broker port
user = ""#"Elias"            #plaats dit in de repo zonder wachtwoorden
password = ""#"Elias"            #Connection password
  
client = mqttClient.Client("phillips")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
  
client.connect(broker_address, port=port)          #connect to broker
  
client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
client.subscribe("sigma")
  
try:
    while True:
        time.sleep(1)
        print("lengte list " + str(len(messages)))
        if(len(messages)>0):
            bericht = messages.pop()
            print("Message received: "  + bericht+ "; booleans[1]=",booleans[1])
            booleans[0] = False
            if booleans[1] == False:
                while booleans[1]==False:
                    time.sleep(0.1)
                    print("wait", booleans[1])
                t1.join()
            if bericht == "rainbow":
                t1 = threading.Thread(target=rainbow)
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "off":
                t1 = threading.Thread(target=anyColor(0,0,0,0,0,0))
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "bubbelKleur":
                t1 = threading.Thread(target=anyColor(98,1,1,2,1,145))
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "allLights":
                t1 = threading.Thread(target=allLights)
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "pulseColor":
                t1 = threading.Thread(target=pulseColor(90,150,90))
                booleans[0] = True
                booleans[1] = False
                t1.start()
  
except KeyboardInterrupt:
    booleans[0] = False
    print("exiting")
    client.disconnect()
    client.loop_stop()
    GPIO.cleanup()
