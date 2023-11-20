import RPi.GPIO as GPIO
import paho.mqtt.client as mqttClient
import time
import board
import neopixel
import threading


# Configure the Neopixel ring
num_pixels = 64
pixel_pin = board.D18
ORDER = neopixel.GRBW

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

# Define colors
kleuren = [
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
running = False
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

def allLights():
    pixels.fill(kleuren[0])

def anyColor(r, g, b, r2, g2, b2):
    for i in range(0, num_pixels/2):
        pixels[i] = (r, g, b)
    
    for i in range(num_pixels/2, num_pixels):
        pixels[i] = (r2, g2, b2)
    
    pixels.show()

def pulseColor(r, g, b):
    while(True):
        for i in range(0, 255):
            pixels.setBrightness(i)
        for i in range(255,0):
            pixels.setBrightness(i)


def audio():
    #TO DO
    print("audio")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
        
        
thread2 = threading.Thread(target=rainbow)
  
def on_message(client, userdata, message):
    print("Message received: "  + str(message.payload.decode("utf-8")))
    running=True
    #thread2.join()
    if(message.payload.decode("utf-8") == "rainbow"):
        running=False
        thread2 = threading.Thread(target=rainbow)
        thread2.start()
    if(message.payload.decode("utf-8") == "all"):
        #running=False
        thread2 = threading.Thread(target=allLights)
        thread2.start()
    


Connected = False

broker_address= "projectmaster.devbit.be"  #Broker address
port = 1883               #Broker port
user = "Elias"                    #Connection username
password = "Elias"            #Connection password

client = mqttClient.Client("DancingLight")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
  
client.connect(broker_address, port=port)          #connect to broker
  
client.loop_start()        #start the loop
  
while Connected != True:    #Wait for connection
    time.sleep(0.1)
  
client.subscribe("PM/DL/DL/command")
  
try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()

rainbow()
#try:
 #   while True:
  #      speakerInput = GPIO.input(Pin)
   #     if speakerInput == False:
    #        for color in colors:
     #           pixels.fill(color)  # Cycle through all the colors
      #          pixels.show()
       #         print("AAN")
        #        time.sleep(0.1)
       # else:
        #    pixels.fill((204, 0, 255))  # purple
         #   print("UIT")
          #  pixels.show()
       # time.sleep(0.1)
#except KeyboardInterrupt:
 #   pass

GPIO.cleanup()

