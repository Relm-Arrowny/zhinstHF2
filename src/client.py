'''
Created on 24 Mar 2023

@author: wvx67826
'''

import socket

HOST = "127.23.110.81" # The server's hostname or IP address
PORT = 63888  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"getData")
    data = s.recv(1024)
    if data == b"0":
        print ("Unexpected request")

print(data)