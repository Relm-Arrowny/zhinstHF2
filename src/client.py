'''
Created on 24 Mar 2023

@author: wvx67826
'''

import socket
from time import time, sleep
#HOST = "I10-WS004" # The server's hostname or IP address
HOST = "diamrl5641"
PORT = 7891#5151  # The port used by the server
timeout = 5


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(timeout);
    s.connect((HOST, PORT))
    data = []
    for i in range(0,5,1):
        
        s.sendall(b"setsRefHarm %f" %i)
        data = s.recv(1024)
        if data == b"data read failed: '/dev4206/scopes/0/wave'":
            print(data)
        print(data)
        print("\n")
        sleep(1)
        temp = b"On" if i%2==0 else b"Off"
        s.sendall(b"setsRefOutSwitch %b" %temp)
        data = s.recv(1024)
        print(data)
        print("\n")
        
    if data != b"1":
        print ("Good")
