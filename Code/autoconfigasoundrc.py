import os
import time

time.sleep(15) #randem interval wachten omdat werkt net na bootup maar daarna start de bureaubladomgeving en hierdoor stopt ie weer

os.system("arecord -l > temp.txt")
file1 = open("temp.txt","r")
Lines = file1.readlines()
cardnr = Lines[1][Lines[1].index("card ")+5]
devnr = Lines[1][Lines[1].index("device ")+7]
file1.close()
file2 = open("/home/pi/.asoundrc","w")
file2.write("pcm.!default {")
file2.write("  type asym")
file2.write("  capture.pcm \"mic\"")
file2.write("}")
file2.write("pcm.mic {")
file2.write("  type plug")
file2.write("  slave {")
file2.write("    pcm \"hw:")
file2.write(cardnr)
file2.write(",")
file2.write(devnr)
file2.write("\"")
file2.write("  }")
file2.write("}")
file2.close()
os.remove("temp.txt")
