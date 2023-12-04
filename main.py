#packetten importeren
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
import queue

#Als dit programma uitgevoert wordt bij opstart dan is dit nodig omdat het anders start voordat audio drivers en andere essentiele dingen opgestart zijn.
time.sleep(15)

#t1 = thread voor effect op te laten uitvoeren, mainthread gaat controle uitvoeren over welk effect er in t1 zit.
t1 = threading.Thread()

#messages is een queue met de doorgegeven effecten via mqtt in, (queue voor bescherming tegen spam)
messages = queue.Queue()
#standaard effect starten
messages.put("ledsMeDbRGB")

#in een array om er in andere threads ook aan te kunnen
#eerste is voor als het effect mag blijven runnen (wordt op false gezet door de mainthread), tweede is voor als het effect gestopt is dan weet de mainthread dat het een ander effect mag starten.
booleans = [False, True]#running, stoped
#mqtt rgb waarden uit de rgb topics komen hierin terecht en zijn altijd berijkbaar/aanpasbaar
rgb = [0,255,80]
rgb2 = [0,255,80]
#voor als we de command "off" krijgen, dan moeten we onthouden aan welk effect we zaten voor als het weer op "on" komt
laatsteEffect = ["ledsMeDbRGB"]
#configuratie binnenlezen
mqttfile = open("/mqttCred.conf","r")
configuratie = mqttfile.readlines()
#topics binnenlezen en in variabelen steken (laatste charakter is een \n dus je moet deze uitsluiten)
effecttopic = configuratie[9][0:len(configuratie[9])-1]
rgbtopic = configuratie[11][0:len(configuratie[11])-1]
commandtopic = configuratie[13][0:len(configuratie[13])-1]
rgbtopic2 = configuratie[15][0:len(configuratie[15])-1]

#functie die wordt uitgevoert als we een bericht krijgen via mqtt
def on_message(client, userdata, message):
    #bericht decoderen
    bericht = str(message.payload.decode("utf-8"))
    #als het bericht van de effect topic afkomstig is.. de rest van de ifs begrijp je wel zelf
    if(message.topic==effecttopic):
        #effect toevoegen aan de queue
        messages.put(bericht)
        #laatste effect updaten
        laatsteEffect[0] = bericht
    if(message.topic==commandtopic):
        if(bericht == "ON"):
            messages.put(laatsteEffect[0])
        elif(bericht == "OFF"):
            messages.put("off")
    if(message.topic == rgbtopic):
        dat = bericht.split(',')
        #als er foutive data is dan worden de rgb waarden niet upgedated
        for i in range(3):
            try:
                rgb[i] = int(dat[i])%256 #om binnen 0-255 te blijven
            except:
                print("error data")
    if(message.topic == rgbtopic2):
        dat = bericht.split(',')
        for i in range(3):
            try:
                rgb2[i] = int(dat[i])%256
            except:	
                print("error data")
    print(message.topic,bericht)#snel bugs vinden

#functie wanneer de mqtt client verbinding maakt
def on_connect(client, userdata, flags, rc):
    if rc == 0:
  
        print("Connected to broker")
  
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

#root mean square berekenen maar ik weet niet waar dit wordt opgeroepen
def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue

#Ledstrip instellingen definieren + pixel array (letterlijk een 1D array met de kleuren van alle leds) aanmaken
num_pixels = 64
pixel_pin = board.D18
ORDER = neopixel.GRBW
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

#audio componenten initialiseren
p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 1
print(p.get_default_input_device_info())

#audio stream initialiseren maar nog niet starten
stream = p.open(format=p.get_format_from_width(WIDTH),
    input_device_index=DEVICE,
    channels=1,
    rate=RATE,
    input=True,
    output=False,
    stream_callback=callback)
#doe stream.start_stream() bij start van elke audio reactieve functie
#doe stream.stop_stream() bij het einde van elke audio reactieve functie
#doe stream.close() enkel maar op het einde (ander werkt het niet)

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
#pin voor de ledstrip data
Pin = 16
#nodig voor aansturen pin
GPIO.setup(Pin, GPIO.IN)


#hier zijn alle effecten aangepast om te werken met de threading:
#dit zijn effecten maar het is een beetje veel om bij ze allemaal een concrete werking te commenten, het is wel makkelijk te begrijpen
def rainbow():
    kleurindex = 0
    halvepixels = 0
    extra = 0
    while True:
        for i in range(halvepixels):
            pixels[30-halvepixels+i] = kleuren[(i+extra)%len(kleuren)]
            pixels[29+halvepixels-i] = kleuren[(i+extra)%len(kleuren)]
        time.sleep(0.01)
        pixels.show()#dit commando zorgt ervoor dat alle kleuren aangewezen aan pixels worden weergegeven
        if(halvepixels == 30):
          extra += 1
        else:
          halvepixels += 1
        if(booleans[0] == False):   #als effect moet stoppen voor andere effecten
            break
    booleans[1] = True  #stopped op true zetten

def anyColor(r, g, b, r2, g2, b2):
    print(r, g, b, r2, g2, b2)
    for i in range(0, int(num_pixels/2)):
        pixels[i] = (r, g, b)
    
    for i in range(int(num_pixels/2), num_pixels):
        pixels[i] = (r2, g2, b2)
    pixels.show()
    booleans[1] = True
    
def rgbKleur():
    while(True):
        for i in range(0, int(num_pixels/2)):
            pixels[i] = (rgb[0], rgb[1], rgb[2])#rgb waarden van mqtt constant uitlezen
        
        for i in range(int(num_pixels/2), num_pixels):
            pixels[i] = (rgb2[0], rgb2[1], rgb2[2])
        pixels.show()
        time.sleep(1)
        if(booleans[0]==False):
            break;
    booleans[1] = True

def pulseColor(r, g, b):    #oud effect, er is geen manier om de helderheid intestellen, kan niet worden opgeroepen uit de mainthread
    pixels.fill((r,g,b))
    while(True):
        for i in range(0, 255):
            pixels.setBrightness(i)
        for i in range(255,0):
            pixels.setBrightness(i)
        if(booleans[0] == False):
            break
    booleans[1] = True

def ledsMeDbFlikker():
    minste = 0
    meeste = 1
    stream.start_stream()#voor te beginnen naar de microfoon te luisteren
    recentmeeste = 0
    recentminste = 0
    nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)	#5 seconden vanaf n
    RGB = [0,0,0]
    iro_index = 0
    verhoogen = True
    while stream.is_active():
        db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
        positf = ((db+40))
        if(positf<minste):
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
        filled_progbar  = round((positf-minste)/(meeste-minste)*16)
        if filled_progbar > 6:
            pixels.fill((filled_progbar*RGB[0],filled_progbar*RGB[1],filled_progbar*RGB[2]))
        else:
            pixels.fill((0,0,0))
        if(verhoogen == True):
            RGB[iro_index%3] += 1
            if(RGB[iro_index%3] == 10):
                verhoogen = False
        else:
            RGB[iro_index%3] -= 1
            if(RGB[iro_index%3] == 0):
                verhoogen = True
                iro_index +=1
        pixels.show()
        if(booleans[0] == False):
            break
    stream.stop_stream()#stoppen met naar de audio invoer te luisteren
    booleans[1] = True

def ledsMeDb():
    stream.start_stream()
    minste = 0
    meeste = 1
    recentmeeste = 0
    recentminste = 0
    nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)
    while stream.is_active(): 
        db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
        positf = ((db+40))
        if(positf<minste):
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
        filled_progbar  = round((positf-minste)/(meeste-minste)*255)
        
        pixels.fill((filled_progbar,filled_progbar,filled_progbar))
        pixels.show()
        if(booleans[0] == False):
            break
    stream.stop_stream()
    booleans[1] = True
    
def ledsMeDbRGB():
    stream.start_stream()
    minste = 0
    meeste = 1
    recentmeeste = 0
    recentminste = 0
    nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)
    while stream.is_active(): 
        db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
        positf = ((db+40))
        if(positf<minste):
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
        filled_progbar  = ((positf-minste)/(meeste-minste))*16
        pixels.fill((round((rgb[0]/16)*filled_progbar),round((rgb[1]/16)*filled_progbar),round((rgb[2]/16)*filled_progbar)))
        pixels.show()
        if(booleans[0] == False):
            break
    stream.stop_stream()
    booleans[1] = True

def vlakMuziek():
    minste = 0
    meeste = 1
    recentmeeste = 0
    recentminste = 0
    nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)	#5 seconden vanaf nu
    index = 0
    verander = False
    stream.start_stream()
    while stream.is_active(): 
        db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
        positf = ((db+40))
        if(positf<minste):
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
        filled_progbar  = round((positf-minste)/(meeste-minste))
        if filled_progbar> 0.5 and verander == False:
            verander = True
            index += 1
            pixels.fill(kleuren[index%len(kleuren)])
            pixels.show()
        if(filled_progbar < 0.5):
            verander = False
        if(booleans[0] == False):
            break
    stream.stop_stream()
    booleans[1] = True

def uitbreidReactie():
    pixels.fill((0,0,0))
    kleurlevels = [(20,20,20),(50,20,20),(140,20,20),(255,20,20),(20,50,20),(20,140,20),(20,255,20),(20,20,50),(20,20,140),(20,20,255)]#10 levels in totaal
    stream.start_stream()
    while stream.is_active(): 
        db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
        geluidIndexMidden = round(((db+40)/10)%1*11)-1#van -1 tot 10
        for j in range(3):
            color = (0,0,0)
            if geluidIndexMidden-j >= 0 and geluidIndexMidden-j < 10:
                color = kleurlevels[geluidIndexMidden-j]
            for i in range(8):
                pixels[i*8+3-j] = color
                pixels[i*8+4+j] = color
        pixels.show()
        if(booleans[0] == False):
            break
    stream.stop_stream()
    booleans[1] = True
    
def MiddenBounce():
    kleurindex = 0
    aantal = int(num_pixels/2)
    index = 0
    while True:
        kleur = kleuren[index]
        for i in range(aantal):
            pixel = len(pixels) - 1
            pixels[pixel-i] = kleur
            pixels[i] = kleur
            pixels.show()
        for i in range(aantal):
            pixels[aantal+i] = (0,0,0)
            pixels[aantal-i] = (0,0,0)
            pixels.show()
        index += 1
        if index == len(kleuren):
            index = 0
        pixels.fill((0,0,0))
        pixels.show()
        if(booleans[0] == False):
            break
    booleans[1] = True

Connected = False   #global variable for the state of the connection
#deze code wordt nogsteeds enkel in het begin uitgevoert, hiervoor waren het 
#mqtt instellingen configureren
broker_address= configuratie[3][0:len(configuratie[3])-1] #"projectmaster.devbit.be"  #Broker address
port =int(configuratie[1])               #Broker port
print(port)
user = configuratie[5][0:len(configuratie[5])-1]#            #plaats dit in de repo zonder wachtwoorden
password = configuratie[7][0:len(configuratie[7])-1]#          #Connection password
  
#paho mqtt client aanzetten
client = mqttClient.Client("raspberry pi")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
client.loop_start()        #start the loop

#wacht tot er verbinding is met de mqtt broker
while Connected != True:
    time.sleep(0.1)

#subscriben op alle topics die in het config bestand stonden
client.subscribe([(effecttopic,0),(rgbtopic,0),(commandtopic,0),(rgbtopic2,0)])

try:
    #oneindige lus starten in de main thread
    while True:
        #wordt elke seconde uitgevoert (als hij niet ergens blijft hangen)(1 seconde + loop tijd)
        time.sleep(1)
        print("lengte list " + str(messages.qsize()))#voor debug

        #als er een bericht binnen kwam (effect)
        if (messages.qsize()>0):
            bericht = messages.get()
            print("Message received: "  + bericht+ "; booleans[1]=",booleans[1])#voor debug
            booleans[0] = False #sijn geven aan effect thread om op te houden
            if booleans[1] == False:
                while booleans[1]==False:
                    time.sleep(0.1)
                    print("wait", booleans[1])#zolang dat de thread nog niet gestopt is
                t1.join()#alleen joinen als ie al aan het runnen was (dus niet voor het eerste effect)
            if bericht == "rainbow":#als bericht == effect naam: t1 = thread(effect), altijd hetzelfde
                t1 = threading.Thread(target=rainbow)
                booleans[0] = True  #toelaten om te runnen
                booleans[1] = False #klaarzetteen voor als een nieuw effect moet gestart worden
                t1.start()          #thread starten
            if bericht == "off":
                t1 = threading.Thread(target=anyColor, kwargs={"r":0,"g":0,"b":0,"r2":0,"g2":0,"b2":0})#doe dit om argumenten mee te geven kwargs={"argument naam":waarde}
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "rgbKleur":
                t1 = threading.Thread(target=rgbKleur)
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "ledsMeDbFlikker":
                t1 = threading.Thread(target=ledsMeDbFlikker)
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "ledsMeDb":
                t1 = threading.Thread(target=ledsMeDb)
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "ledsMeDbRGB":
                t1 = threading.Thread(target=ledsMeDbRGB)
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "vlakMuziek":
                t1 = threading.Thread(target=vlakMuziek)
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "uitbreidReactie":
                t1 = threading.Thread(target=uitbreidReactie)
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "MiddenBounce":
                t1 = threading.Thread(target=MiddenBounce)
                booleans[0] = True
                booleans[1] = False
                t1.start()
#dingen afhandelen als ctrl+c wordt ingedrukt
except KeyboardInterrupt:
    booleans[0] = False
    if booleans[1] == False:
        while booleans[1]==False:
            time.sleep(0.1)
        t1.join()
    print("exiting")
    client.disconnect()
    client.loop_stop()
    GPIO.cleanup()
    stream.close()
    p.terminate()
