'''
Created on 24 Mar 2023

@author: wvx67826

@deprecated: 
    Python class to create a sever that connect to HF2 data server and listen for data request
    from client. 
    It ask data server for the data and pass it back to the client.
    
    https://docs.zhinst.com/pdf/ziMFIA_UserManual.pdf
@version: 1.0 
    class take 5 optional parameters:
    ip and port for the server
    ip and port for the HF2 and the api level 

        
     start(self) :bool   start the server  
     connectHF2(self) : bool        connect to data server
'''

import socket
import zhinst.core
import numpy as np

class HF2Sever():
    
    def __init__(self, ip ="127.23.110.81", port = 63888,
                  HF2IP = "172.23.110.84", HF2Port = 8004, api_level = 1
                  , device_id = "dev4206"):
        self.HOST = ip # The server's hostname or IP address
        self.PORT = port  # The port used by the server
        self.serverRunning = False
        self.HF2IP = HF2IP
        self.HF2Port = HF2Port
        self.api_level = api_level
        self.daq = None
        self.device_id = device_id
        
    def start(self):
        self.serverRunning = True
        if(self.connectHF2()):
        
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind((self.HOST, self.PORT))
                except:
                    print("fail to start server")
                    
                while self.serverRunning:
                    s.listen()
                    conn, addr = s.accept()
                    data = conn.recv(1024)
                    if data == b"s":
                        self.serverRunning = False
                        conn.sendall(b"server stopping")
                        
                    elif data == b"getData":
                        sample = self.daq.getSample(f"/{self.device_id}/demods/0/sample")
                        X = sample['x'][0]
                        Y = sample['y'][0]
                        #R = np.abs(X + 1j*Y)
                        #Theta = np.arctan2(Y,X)
                        sendData = "%.3e, %.3e" %(X,Y)
                        conn.sendall(sendData.encode("utf_8"))
                    else:
                        sendData = b"0"
                        conn.sendall(sendData)
        else:
            return False
        return True

    def connectHF2(self):
        try:
            self.daq = zhinst.core.ziDAQServer(self.HF2IP,self.HF2Port, self.api_level)
            print("HF2 Data server connected")
        except:
            print("connection failed")
            return False
        return True
    