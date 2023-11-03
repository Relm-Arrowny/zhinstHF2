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
    for i in range(1000,20000,1000):
        s.sendall(b"setRefFreq %f" %i)
        data = s.recv(1024)
        if data == b"data read failed: '/dev4206/scopes/0/wave'":
            print(data)
        print(data)
        print("\n")
       
    if data != b"1":
        print ("Good")
