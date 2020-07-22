#Very minimal client to send the sample to the phone
#You can easly write each line in the shell to have a total control to do some test

import socket

TEL_IP = "000.000.0.00" # YOUR PHONE IP HERE
PORT = 54596            # THE PORT TO USE HERE
FILE = "_________.h264" # YOUR SAMPLE HERE

#Open end read file
f = open(FILE, "rb")

b = f.read()

f.close()

#send data
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TEL_IP, PORT))

s.send(b) #s.send(b[:5000]) s.send(b[5000:7000]) s.send(b[7000:])

s.close()
