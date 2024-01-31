'''
Created on 24 Mar 2023

@author: wvx67826
'''

import socket
from time import time, sleep
#HOST = "I10-WS004" # The server's hostname or IP address
HOST = "localhost" #"diamrl5641"
PORT = 7892#5151  # The port used by the server
timeout = 15


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(timeout);
    s.connect((HOST, PORT))
    start = time()
    s.sendall(b"getData 4")
    data = s.recv(1024)
    print (data, time()-start)
        
    if data != b"1":
        print ("Good")
