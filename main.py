#packages importeren
import paho.mqtt.client as mqttClient
import time
import threading
import RPi.GPIO as GPIO
import board
import neopixel
import datetime
from math import log10
import math
import audioop
import pyaudio
import queue

#Als dit programma uitgevoerd wordt bij opstart dan is dit nodig omdat het anders start voor dat audio drivers en andere essentiele dingen opgestart zijn.
time.sleep(1)
doosNummer = [3]
#t1 = thread om effect op te laten uitvoeren, mainthread gaat controle uitvoeren over welk effect er in t1 zit.
doosThreads = [threading.Thread(),threading.Thread(),threading.Thread()]
muziekLuisteraars = [0]
#messages is een queue met het doorgegeven effecten via mqtt in, (queue voor bescherming tegen spam)
messages = queue.Queue()
#standaard effect starten
messages.put(("ledsMeDbRGB",1))
messages.put(("ledsMeDbRGB",2))

#in een array om er in andere threads ook aan te kunnen
#eerste is voor als het effect mag blijven runnen (wordt op false gezet door de mainthread), tweede is voor als het effect gestopt is dan weet de mainthread dat het een ander effect mag starten.
booleans = [[False, True],[False,True],[False,True]]#running, stoped
#mqtt rgb waarden uit de rgb topics komen hierin terecht en zijn altijd berijkbaar/aanpasbaar
rgb = [[255,255,0],[0,255,255],[255,0,255]]
#voor als we de command "off" krijgen, dan moeten we onthouden aan welk effect we zaten voor als het weer op "on" komt
laatsteEffect = ["ledsMeDbRGB","ledsMeDbRGB","ledsMeDbRGB"]
#configuratie binnenlezen
mqttfile = open("/mqttCred.conf","r")
configuratie = mqttfile.readlines()
#topics binnenlezen en in variabelen steken (laatste character is een \n dus je moet deze uitsluiten)
topicPath = configuratie[9][0:len(configuratie[9])-1]
effecttopic = configuratie[11][0:len(configuratie[11])-1]
rgbtopic = configuratie[13][0:len(configuratie[13])-1]
commandtopic = configuratie[15][0:len(configuratie[15])-1]

#functie die wordt uitgevoerd als we een bericht krijgen via mqtt
def on_message(client, userdata, message):
    #bericht decoderen
    bericht = str(message.payload.decode("utf-8"))
    topicIndex = -1
    for i in range(len(Topics)):
        if(Topics[i] == message.topic):
            topicIndex = i
            break
    if(topicIndex == -1): return
    #als het bericht van de effect topic afkomstig is.. de rest van de ifs begrijp je wel zelf
    if(topicIndex%3==0):
        #print("effect van topic:",message.topic,"heeft doosindex:", math.floor(topicIndex/3))
        #effect toevoegen aan de queue
        messages.put((bericht,math.floor(topicIndex/3)))
        #laatste effect updaten
        laatsteEffect[math.floor(topicIndex/3)] = bericht
    if(topicIndex%3==2):
        if(bericht == "ON"):
            messages.put((laatsteEffect[0],math.floor(topicIndex/3)))
        elif(bericht == "OFF"):
            messages.put(("off",math.floor(topicIndex/3)))
    if(topicIndex%3==1):
        dat = bericht.split(',')
        #als er foutieve data is dan worden de rgb waarden niet geupdate
        for i in range(3):
            try:
                rgb[math.floor(topicIndex/3)][i] = int(dat[i])%256 #om binnen 0-255 te blijven
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

#root mean square berekenen
def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue

#Ledstrip instellingen definieren + pixel array (letterlijk een 1D array met de kleuren van alle leds) aanmaken
num_pixels = 96
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

def fillPixelsIndex(r,g,b,doosIndex):
    for i in range((doosIndex*32),(doosIndex*32)+32):
        pixels[i] = (r,g,b)#rgb waarden van mqtt constant uitlezen
    pixels.show()

#hier zijn alle effecten aangepast om te werken met de threading:
#dit zijn effecten maar het is een beetje veel om bij ze allemaal een concrete werking te commenten, het is wel makkelijk te begrijpen
def rainbow(doosIndex):
    kleurindex = 0
    halvepixels = 0
    extra = 0
    while True:
        for i in range(halvepixels):
            pixels[16-halvepixels+i + (doosIndex*32)] = kleuren[(i+extra)%len(kleuren)]
            pixels[15+halvepixels-i+ (doosIndex*32)] = kleuren[(i+extra)%len(kleuren)]
        time.sleep(0.01)
        pixels.show()#dit commando zorgt ervoor dat alle kleuren aangewezen aan pixels worden weergegeven
        if(halvepixels == 16):
          extra += 1
        else:
          halvepixels += 1
        if(booleans[doosIndex][0] == False):   #als effect moet stoppen voor andere effecten
            break
    booleans[doosIndex][1] = True  #stopped op true zetten

    
def rgbKleur(doosIndex):
    while(True):
        for i in range(0+ (doosIndex*32),(doosIndex*32)+32):
            pixels[i] = (rgb[doosIndex][0], rgb[doosIndex][1], rgb[doosIndex][2])#rgb waarden van mqtt constant uitlezen
        pixels.show()
        time.sleep(1)
        if(booleans[doosIndex][0] == False):   #als effect moet stoppen voor andere effecten
            break
    booleans[doosIndex][1] = True  #stopped op true zetten


def ledsMeDbFlikker(doosIndex):
    minste = 0
    meeste = 1
    stream.start_stream()#voor te beginnen naar de microfoon te luisteren
    muziekLuisteraars[0] += 1
    recentmeeste = 0
    recentminste = 0
    nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)	#5 seconden vanaf n
    RGB = [0,0,0]
    iro_index = 0
    verhoogen = True
    while stream.is_active():
        db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
        positive = ((db+40))
        if(positive<minste):
            minste = positive
        if(positive>meeste):	#er is een bug waarbij positive 40 is bij eerste iteratie, ook is 40 de maximum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
            if positive == 40:
                positive = meeste
            meeste = positive
        if(positive<recentminste):
            recentminste = positive
        if(positive>recentmeeste):	#er is een bug waarbij positive 40 is bij eerste iteratie, ook is 40 de maximum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
            if positive == 40:
                positive = recentmeeste
            recentmeeste = positive
        if(datetime.datetime.now() > nieuwcheckinterval):
            meeste = recentmeeste
            minste = recentminste
            nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)
            recentminste = positive
            recentmeeste = positive
        filled_progbar  = round((positive-minste)/(meeste-minste)*16)
        if filled_progbar > 6:
            fillPixelsIndex(filled_progbar*RGB[0],filled_progbar*RGB[1],filled_progbar*RGB[2],doosIndex)
        else:
            fillPixelsIndex(0,0,0,doosIndex)
        if(verhoogen == True):
            RGB[iro_index%3] += 1
            if(RGB[iro_index%3] == 10):
                verhoogen = False
        else:
            RGB[iro_index%3] -= 1
            if(RGB[iro_index%3] == 0):
                verhoogen = True
                iro_index +=1
        if(booleans[doosIndex][0] == False):   #als effect moet stoppen voor andere effecten
            break
    muziekLuisteraars[0] -= 1
    booleans[doosIndex][1] = True  #stopped op true zetten
    
def ledsMeDbRGB(doosIndex):
    muziekLuisteraars[0] += 1
    stream.start_stream()
    minste = 0
    meeste = 1
    recentmeeste = 0
    recentminste = 0
    nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)
    while stream.is_active(): 
        db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
        positive = ((db+40))
        if(positive<minste):
            minste = positive
        if(positive>meeste):	#er is een bug waarbij positive 40 is bij eerste iteratie, ook is 40 de maximum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
            if positive == 40:
                positive = meeste
            meeste = positive
        if(positive<recentminste):
            recentminste = positive
        if(positive>recentmeeste):	#er is een bug waarbij positive 40 is bij eerste iteratie, ook is 40 de maximum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
            if positive == 40:
                positive = recentmeeste
            recentmeeste = positive
        if(datetime.datetime.now() > nieuwcheckinterval):
            meeste = recentmeeste
            minste = recentminste
            nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)
            recentminste = positive
            recentmeeste = positive
        filled_progbar  = ((positive-minste)/(meeste-minste))*16
        for i in range((doosIndex*32),(doosIndex*32)+32):
            pixels[i] = (((rgb[doosIndex][0]/16)*filled_progbar),round((rgb[doosIndex][1]/16)*filled_progbar),round((rgb[doosIndex][2]/16)*filled_progbar))#rgb waarden van mqtt constant uitlezen
        pixels.show()
        if(booleans[doosIndex][0] == False):   #als effect moet stoppen voor andere effecten
            break
    muziekLuisteraars[0] -= 1
    booleans[doosIndex][1] = True  #stopped op true zetten

def vlakMuziek(doosIndex):
    minste = 0
    meeste = 1
    recentmeeste = 0
    recentminste = 0
    nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)	#5 seconden vanaf nu
    index = 0
    verander = False
    stream.start_stream()
    muziekLuisteraars[0] += 1
    while stream.is_active(): 
        db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
        positive = ((db+40))
        if(positive<minste):
            minste = positive
        if(positive>meeste):	#er is een bug waarbij positive 40 is bij eerste iteratie, ook is 40 de maximwum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
            if positive == 40:
                positive = meeste
            meeste = positive
        if(positive<recentminste):
            recentminste = positive
        if(positive>recentmeeste):	#er is een bug waarbij positive 40 is bij eerste iteratie, ook is 40 de maximum waarde van het geluid toestel dus dit zullen we bijna nooit in de code als resultaat krijgen
            if positive == 40:
                positive = recentmeeste
            recentmeeste = positive
        if(datetime.datetime.now() > nieuwcheckinterval):
            meeste = recentmeeste
            minste = recentminste
            nieuwcheckinterval = datetime.datetime.now() + datetime.timedelta(0,5)
            recentminste = positive
            recentmeeste = positive
        filled_progbar  = round((positive-minste)/(meeste-minste))
        if filled_progbar> 0.5 and verander == False:
            verander = True
            index += 1
            fillPixelsIndex(kleuren[index%len(kleuren)][0],kleuren[index%len(kleuren)][1],kleuren[index%len(kleuren)][2],doosIndex)
        if(filled_progbar < 0.5):
            verander = False
        if(booleans[doosIndex][0] == False):   #als effect moet stoppen voor andere effecten
            break
    muziekLuisteraars[0] -= 1
    booleans[doosIndex][1] = True  #stopped op true zetten

def uitbreidReactie(doosIndex):
    stream.start_stream()
    muziekLuisteraars[0] += 1
    fillPixelsIndex(0,0,0,doosIndex)
    kleurlevels = [(20,20,20),(50,20,20),(140,20,20),(255,20,20),(20,50,20),(20,140,20),(20,255,20),(20,20,50),(20,20,140),(20,20,255)]#10 levels in totaal
    stream.start_stream()
    while stream.is_active(): 
        db = 20 * log10(rms)#db gaat van -40 tot 0 somehow op dit apparaat
        geluidIndexMidden = round(((db+40)/10)%1*11)-1#van -1 tot 10
        for j in range(3):
            color = (0,0,0)
            if geluidIndexMidden-j >= 0 and geluidIndexMidden-j < 10:
                color = kleurlevels[geluidIndexMidden-j]
            for i in range(4):
                pixels[i*8+3-j+32*doosIndex] = color
                pixels[i*8+4+j+32*doosIndex] = color
        pixels.show()
        if(booleans[doosIndex][0] == False):   #als effect moet stoppen voor andere effecten
            break
    muziekLuisteraars[0] -= 1
    booleans[doosIndex][1] = True  #stopped op true zetten
    
def MiddenBounce(doosIndex):
    kleurindex = 0
    aantal = 16
    index = 0
    while True:
        kleur = kleuren[index]
        for i in range(aantal):
            pixel = 32*doosIndex
            furtherpixel = 32*(doosIndex+1)-1
            pixels[pixel+i] = kleur
            pixels[furtherpixel-i] = kleur
            pixels.show()
        for i in range(aantal):
            pixel = 32*doosIndex
            furtherpixel = 32*(doosIndex+1)-1
            pixels[pixel+aantal-i] = (0,0,0)
            pixels[furtherpixel-aantal+i] = (0,0,0)
            pixels.show()
        index += 1
        if index == len(kleuren):
            index = 0
        fillPixelsIndex(0,0,0,doosIndex)
        if(booleans[doosIndex][0] == False):   #als effect moet stoppen voor andere effecten
            break
    booleans[doosIndex][1] = True  #stopped op true zetten

Connected = False   #global variable for the state of the connection
#deze code wordt nog steeds enkel in het begin uitgevoert, hiervoor waren het 
#mqtt instellingen configureren
broker_address= configuratie[3][0:len(configuratie[3])-1] #"projectmaster.devbit.be"  #Broker address
port =int(configuratie[1])               #Broker port
print(port)
user = configuratie[5][0:len(configuratie[5])-1]#plaats dit in de repo zonder wachtwoorden
password = configuratie[7][0:len(configuratie[7])-1]#Connection password
  
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
sublist = []
Topics = []
for i in range(doosNummer[0]):
    Topics.append(topicPath+str(i)+effecttopic)
    Topics.append(topicPath+str(i)+rgbtopic)
    Topics.append(topicPath+str(i)+commandtopic)
    for j in range(3):
        sublist.append((Topics[i*3+j],0))
client.subscribe(sublist)
print(Topics)

try:
    #oneindige lus starten in de main thread
    while True:
        #wordt elke seconde uitgevoerd (als hij niet ergens blijft hangen)(1 seconde + loop tijd)
        time.sleep(1)
        #als er een bericht binnen kwam (effect)
        if (messages.qsize()>0):
            short = messages.get()
            bericht = short[0]
            Topicindex = short[1]
            print("Message received:",bericht,"voor doos:", Topicindex)#voor debug
            booleans[Topicindex][0] = False #sein geven aan effect thread om op te houden
            if booleans[Topicindex][1] == False:
                while booleans[Topicindex][1]==False:
                    time.sleep(0.1)
                    print("wait", booleans[Topicindex][1])#zolang dat de thread nog niet gestopt is
                doosThreads[Topicindex].join()#alleen joinen als hij al aan het runnen was (dus niet voor het eerste effect)
            if(muziekLuisteraars[0] == 0):
                stream.stop_stream()
            if bericht == "rainbow":#als bericht == effect naam: t1 = thread(effect), altijd hetzelfde
                doosThreads[Topicindex] = threading.Thread(target=rainbow, kwargs={"doosIndex":Topicindex})
                booleans[Topicindex][0] = True
                booleans[Topicindex][1] = False
                doosThreads[Topicindex].start()
            if bericht == "rgbKleur":
                doosThreads[Topicindex] = threading.Thread(target=rgbKleur, kwargs={"doosIndex":Topicindex})
                booleans[Topicindex][0] = True
                booleans[Topicindex][1] = False
                doosThreads[Topicindex].start()
            if bericht == "off":
                fillPixelsIndex(0,0,0,Topicindex)
            if bericht == "ledsMeDbFlikker":
                doosThreads[Topicindex] = threading.Thread(target=ledsMeDbFlikker, kwargs={"doosIndex":Topicindex})
                booleans[Topicindex][0] = True
                booleans[Topicindex][1] = False
                doosThreads[Topicindex].start()
            if bericht == "ledsMeDbRGB":
                doosThreads[Topicindex] = threading.Thread(target=ledsMeDbRGB, kwargs={"doosIndex":Topicindex})
                booleans[Topicindex][0] = True
                booleans[Topicindex][1] = False
                doosThreads[Topicindex].start()
            if bericht == "vlakMuziek":
                doosThreads[Topicindex] = threading.Thread(target=vlakMuziek, kwargs={"doosIndex":Topicindex})
                booleans[Topicindex][0] = True
                booleans[Topicindex][1] = False
                doosThreads[Topicindex].start()
            if bericht == "uitbreidReactie":
                doosThreads[Topicindex] = threading.Thread(target=uitbreidReactie, kwargs={"doosIndex":Topicindex})
                booleans[Topicindex][0] = True
                booleans[Topicindex][1] = False
                doosThreads[Topicindex].start()
            if bericht == "MiddenBounce":
                doosThreads[Topicindex] = threading.Thread(target=MiddenBounce, kwargs={"doosIndex":Topicindex})
                booleans[Topicindex][0] = True
                booleans[Topicindex][1] = False
                doosThreads[Topicindex].start()
#dingen afhandelen als ctrl+c wordt ingedrukt
except KeyboardInterrupt:
    tel = 0
    for threa in doosThreads:
        booleans[tel][0] = False
        if booleans[tel][1] == False:
            while booleans[tel][1]==False:
                time.sleep(0.1)
            threa.join()
        tel+=1
    print("exiting")
    client.disconnect()
    client.loop_stop()
    GPIO.cleanup()
    stream.close()
    p.terminate()
