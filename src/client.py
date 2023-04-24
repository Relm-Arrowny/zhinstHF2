'''
Created on 24 Mar 2023

@author: wvx67826
'''

import socket

HOST = "127.23.110.81" # The server's hostname or IP address
PORT = 6388  # The port used by the server
timeout = 5
from time import time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(timeout);
    s.connect((HOST, PORT))
    s.sendall(b"getData 1")
    data = s.recv(1024)
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

