'''
Created on 24 Mar 2023

@author: wvx67826

@deprecated: 
    Python class to create a sever that connect to HF2 data server and listen for data request
    from client. 
    It ask data server for the data and pass it back to the client.
    
    https://docs.zhinst.com/pdf/ziMFIA_UserManual.pdf
@version: 1.1 
    class take 5 optional parameters:
    ip and port for the server
    ip and port for the HF2 and the api level 

    start(self) :bool   start the server
    list of comment the server will react to
    
        "stopSever":             stop the server
        "autoVoltageInRange":    trigger auto range on input voltage
        "setTimeConstant":        set time constant on the lockin
        "setDataRate":            set the rate that rate is being generated
        "setCurrentInRange":     set the gain on the input current
        "autoCurrentInRange":     trigger auto gain on the input current
                    
     connectHF2(self) : bool        connect to data server
'''

import socket
import zhinst.core
import numpy as np

class HF2Sever():
    
    def __init__(self, ip ="0.0.0.0", port = 63888,
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
                    data = conn.recv(1024).split()
                    
                    if data[0] == b"stopSever":
                        self.serverRunning = False
                        conn.sendall(b"server stopping")
                        
                    elif data[0] == b"getData":
                        sample = self.daq.getSample(f"/{self.device_id}/demods/0/sample")
                        value = int (data[1])
                        X = np.average(sample['x'][0:value])
                        Y = np.average(sample['y'][0:value])
                        R = np.abs(X + 1j*Y)
                        Theta = np.rad2deg(np.arctan2(Y,X))
                        sendData = "%e, %e, %e, %f" %(X, Y, R, Theta)
                        conn.sendall(sendData.encode("utf_8"))
                    
                    elif data[0] == b"autoVoltageInRange":
                        self.daq.setInt(f"/{self.device_id}/sigins/0/autorange", 1)
                    
                    elif data[0] == b"setTimeConstant":
                        self.daq.setDouble(f"/{self.device_id}/sigins/0/autorange", float (data[1]))
                    
                    elif data[0] == b"setDataRate":
                        self.daq.setDouble(f"/{self.device_id}/demods/0/rate", float (data[1]))
                    
                    elif data[0] ==  b"setCurrentInRange": 
                        #current range is in multiple of 10 bettween 1e-9 to 1e-2
                        value = np.math.floor(np.math.log(float (data[1]), 10))
                        self.daq.setDouble('/dev4206/currins/0/range', 10**value)
                    elif data[0] ==  b"autoCurrentInRange": 
                        self.daq.setInt('/dev4206/currins/0/autorange', 1)
                    
                    else:
                        sendData = b"0"
                        #sendData = "Invalid command"
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
    