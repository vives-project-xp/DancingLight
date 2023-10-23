import time
import threading

running = False

def Rainbow():
    while True:
        print("zoem")
        time.sleep(0.2)
        if running == False:
            break


t1 = threading.Thread(target=Rainbow)
i = 0
while(True):
    if(i%4 == 3):
        if(running== False):
            t1 = threading.Thread(target=Rainbow)
            running = True
            t1.start()
    else:
        if(running):
            print("stop")
            running = False
            t1.join()
    time.sleep(1)
    i += 1

GPIO.cleanup()