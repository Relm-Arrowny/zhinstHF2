'''
Created on 24 Mar 2023

@author: wvx67826
'''

import socket
import matplotlib.pyplot as plt

#HOST = "I10-WS004" # The server's hostname or IP address
HOST = "diamrl5641"
PORT = 7891#5151  # The port used by the server
timeout = 5
from time import time, sleep

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(timeout);
    s.connect((HOST, PORT))
    data = []
    s.sendall(b"getData 4 ")
    data.append(s.recv(1024))
    print (data)
    s.sendall(b"autoVoltageInRange\n")
    data = s.recv(1024)
    print (data)
    s.sendall( b"setCurrentInRange abc\n")
    data = s.recv(1024)
    print (data)
    s.sendall( b"sdfs \n")
    data = s.recv(1024)
    print (data)
    #s.sendall(b"close\n")
    #s.sendall( b"stopSever")
    #s.close()
    if data != b"1":
        print ("Good")
