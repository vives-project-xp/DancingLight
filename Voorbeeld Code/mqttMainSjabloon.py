import paho.mqtt.client as mqttClient
import time
import threading

t1 = threading.Thread()
messages = []
booleans = [False, True]#running, stoped

def func1():
    while(True):
        print("gyat")
        time.sleep(0.2)
        if booleans[0] == False:
            booleans[1]=True
            break

def func2():
    while(True):
        print("rizz")
        time.sleep(0.2)
        if booleans[0] == False:
            booleans[1]=True
            break

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
  

  
Connected = False   #global variable for the state of the connection
  
broker_address= "test.mosquitto.org"  #Broker address
port = 1883               #Broker port
user = ""                    #Connection username
password = ""            #Connection password
  
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
            #print("Message received: "  + bericht+ "; booleans[1]=",booleans[1])
            booleans[0] = False
            if booleans[1] == False:
                while booleans[1]==False:
                    time.sleep(0.1)
                    print("wait", booleans[1])
                t1.join()
            if bericht == "gyat":
                t1 = threading.Thread(target=func1)
                booleans[0] = True
                booleans[1] = False
                t1.start()
            if bericht == "rizz":
                t1 = threading.Thread(target=func2)
                booleans[0] = True
                booleans[1] = False
                t1.start()

  
except KeyboardInterrupt:
    booleans[0] = False
    print("exiting")
    client.disconnect()
    client.loop_stop()