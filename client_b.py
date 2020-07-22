#Send all the file in aleatory sized packet.

import socket
import random
import time
import ctypes

TEL_IP = "000.000.0.00" # YOUR PHONE IP HERE
PORT = 54596            # THE PORT TO USE HERE
FILE = "_________.h264" # YOUR SAMPLE HERE

f = open(FILE, "rb") #Path to the sample

f.seek(0, 2)
fsize = f.tell()
f.seek(0, 0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TEL_IP, PORT))

read = 0
cum = 0

while f.tell() < 50000:
    b = f.read(random.randint(0, 100)*100)
    read = s.send(b)
    cum += read
    print("send", str(read), "bytes", [ctypes.c_byte(i) for i in b[-5:]]) #Write last five bytes in 0-128 range
    time.sleep(random.random())
print("cum ", cum, " bytes")
s.close()
f.close()
print("end")
input('Press ENTER to exit')
