'''
Created on 24 Mar 2023

@author: wvx67826

@deprecated: 
    Python class to create a sever that connect to HF2 data server and listen for data request
    from client. 
    It ask data server for the data and pass it back to the client.
    
    https://docs.zhinst.com/pdf/ziMFIA_UserManual.pdf
@version: 1.2.1
    added error handling to stop server from crashing
    class take 5 optional parameters:
    ip and port for the serverm
    ip and port for the HF2 and the api level 

    start(self) :bool   start the server
    
    processRequest(self, s) :bool
    list of comment the server will react to
    
        "stopSever":             stop the server
        "autoVoltageInRange":    trigger auto range on input voltage
        "setTimeConstant"   :    set time constant on the lockin
        "setDataRate"       :    set the rate that rate is being generated
        "setCurrentInRange" :    set the gain on the input current
        "setRefFreq"        :    set the Reference Frequency
        "setRefVpk"         :    set Ref voltage
        "setRefVoff"        :    set Ref  voltage DC offset
        "setsRefOutSwitch"  :    set Set Ref "On" or "Off" 
        "setsRefHarm"       :    set Ref harmonic
        "autoCurrentInRange":    trigger auto gain on the input current
        "close"             :    close current connection
        "getData countTime" :    send averaged data for a given countTime
        "setupScope  freq #
        numDataPoint channel:     setup scope for static measurements
     connectHF2(self) : bool        connect to data server
'''

import socket
import zhinst.core
import numpy as np
from time import time, sleep

class HF2Sever():
    
    def __init__(self, ip ="", port = 7891,
                  HF2IP = "172.23.110.84", HF2Port = 8004, api_level = 6
                  , device_id = "dev4206",  freq = 5, numDataPoint = 4096, channel = 0):
        self.HOST = ip # The server's hostname or IP address
        self.PORT = port  # The port used by the server
        self.serverRunning = False
        self.HF2IP = HF2IP
        self.HF2Port = HF2Port
        self.api_level = api_level
        self.daq = None
        self.device_id = device_id
        self.conn = None
        self.scope = None
        
    def start(self):
        self.serverRunning = True
        if(self.connectHF2()):
        
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind((self.HOST, self.PORT))
                    s.listen()
                    self.conn, addr = s.accept()
                    print("Connected: %s" %addr)
                except:
                    print("fail to start server")
                
                
                while self.serverRunning:
                    self.processRequest(s)      
                    
        else:
            return False
        return True

    def connectHF2(self, freq = 5, numDataPoint = 4096, channel = 0):
        try:
            self.daq = zhinst.core.ziDAQServer(self.HF2IP,self.HF2Port, self.api_level)
            self.scopeSetup()
            print("HF2 Data server connected")
        except:
            print("connection failed")
            return False
        return True
    
    def scopeSetup(self, freq = 5, numDataPoint = 4096, channel = 0):
        #setup the scope to take a snap shot for static 
        #the choose are historical
        self.scope = self.daq.scopeModule()
        self.daq.set('/dev4206/scopes/0/time', freq)
        self.daq.set('/dev4206/scopes/0/length', numDataPoint)
        self.daq.set('/dev4206/scopes/0/channels/0/inputselect', channel)
        self.daq.set('/dev4206/scopes/0/enable', 0)
    
    def singleScopeData(self):
        #================= take a single shoot ==================
        self.scopeSetup()
        self.scope.set("scopeModule/mode", 1)
        self.scope.subscribe('/dev4206/scopes/0/wave/')
        self.scope.execute()
        self.daq.setInt('/dev4206/scopes/0/single', 1)
        self.daq.setInt('/dev4206/scopes/0/enable', 1)
        self.daq.sync()
        sleep(0.15) #wait for the single shoot to be completed
        self.scope.finish()
        result = self.scope.read(True)
        static =  result["/dev4206/scopes/0/wave"][0][0]["wave"][0].mean()
        self.scope.unsubscribe('*')
        return static
        #===============================================================
    
    def getLockinData(self,value):
        #================= get Lockin data  ==================
        x =[]
        y =[]
        EndTime = time()+value
        startTime = time() +value*0.5

        while(EndTime>time()>startTime):
            sample = self.daq.getSample(f"/{self.device_id}/demods/0/sample")
            x.append(sample['x'])
            y.append(sample['y'])
        if (not x):
            sample = self.daq.getSample(f"/{self.device_id}/demods/0/sample")
            x.append(sample['x'])
            y.append(sample['y'])
        X = np.average(x)
        Y = np.average(y)
        R = np.abs(X + 1j*Y)
        Theta = np.rad2deg(np.arctan2(Y,X))
        return X,Y,R,Theta
        #===============================================================
    
    def setRefFreq(self,freq):
        try:
            self.daq.setDouble(f"/{self.device_id}/oscs/0/freq", freq)
            self.sendAck()
        except Exception as e:
            self.sendError("Set Ref Freq failed: %s" %e)
        
    def setRefVpk(self, vpk):
        try:
            self.daq.setDouble(f"/{self.device_id}/sigouts/0/amplitudes/1", vpk)
            self.sendAck()
        except Exception as e:
            self.sendError("Set Ref voltage failed: %s" %e)
    
    def setRefVoff(self, v):
        try:
            self.daq.setDouble(f"/{self.device_id}/sigouts/0/offset", v)
            self.sendAck()
        except Exception as e:
            self.sendError("Set Ref voltage offset failed: %s" %e)
    
    def setsRefOutSwitch(self, value):
        try:
            temp = 1 if value == b"On" else 0
            self.daq.setInt(f"/{self.device_id}/sigouts/0/enables/1", temp)
            self.sendAck()
        except Exception as e:
            self.sendError("output switch failed: %s" %e)
            
    def setsRefHarm(self, value):
        try:
            self.daq.setDouble(f"/{self.device_id}/demods/1/harmonic", float(value))
            self.sendAck()
        except Exception as e:
            self.sendError("setsRefHarm failed: %s" %e)
#=================================================================================
    
    def processRequest(self, s):
        print("waiting for command")
        queued_data = self.conn.recv(1024).splitlines()
        print(queued_data)
        
        if not queued_data:
            queued_data =  [b"close"]
            
        for data in queued_data:
            
            data = data.split()   
            if data[0] == b"stopSever":
                self.serverRunning = False
                self.conn.sendall(b"server stopping")
                print("Server stopping")
                self.conn.close()
                self.daq.disconnect()
                
            elif data[0] == b"getData":
                try:
                    if len(data)>1:
                        value = float (data[1])
                    else:
                        value = 0.1
                    X,Y,R,Theta = self.getLockinData(value)    
                    static = self.singleScopeData()
                    sendData = "%e, %e, %f, %e, %e\n" %(X, Y, Theta, static, R)
                    self.conn.sendall(sendData.encode("utf_8"))
                except Exception as e:
                    self.sendError("data read failed: %s" %e)
                    
            elif data[0] == b"autoVoltageInRange":
                try:
                    self.daq.setInt(f"/{self.device_id}/sigins/0/autorange", 1)
                    self.sendAck()
                except Exception as e:
                    self.sendError("Auto Voltage Range failed: %s" %e)
                    
            elif data[0] == b"setTimeConstant":
                try:
                    self.daq.setDouble(f"/{self.device_id}/demods/0/timeconstant", float (data[1]))
                    self.sendAck()
                except Exception as e:
                    self.sendError("Cannot setTimeConstant: %s" %e)
                    
            elif data[0] == b"setDataRate":
                try:
                    self.daq.setDouble(f"/{self.device_id}/demods/0/rate", float (data[1]))
                    self.sendAck()
                except Exception as e:
                    self.sendError("Cannot setDataRate %s" %e)
            
            elif data[0] ==  b"setCurrentInRange":
                try:
                    #current range is in multiple of 10 between 1e-9 to 1e-2
                    value = np.math.floor(np.math.log(float (data[1]), 10))
                    self.daq.setDouble('/dev4206/currins/0/range', 10**value)
                    self.sendAck()
                except Exception as e:
                    self.sendError("Cannot setCurrentInRange: %s" %e)
                    
            elif data[0] ==  b"autoCurrentInRange": 
                try:
                    self.daq.setInt('/dev4206/currins/0/autorange', 1)
                    self.sendAck()
                except Exception as e:
                    self.sendError("autoCurrent failed: %s" %e)
                    
            elif data[0] == b"close":
                self.conn.close()
                self.conn = None
                print("waiting for conection")
                self.conn, addr = s.accept()
                print(f"connected: {addr}")
            
            elif data[0] == b"setRefFreq":
                if len(data)>1:
                        value = float (data[1])
                        self.setRefFreq(value)
                else:
                    self.sendError("setRefFreq failed: %s" %"missing freq value")
                
            elif data[0] == b"setRefV":
                if len(data)>1:
                        value = float (data[1])
                        self.setRefVpk(value)
                else:
                    self.sendError("setRefV failed: %s" %"missing freq value")
                    
            elif data[0] == b"setRefVoff":
                if len(data)>1:
                        value = float (data[1])
                        self.setRefVoff(value)
                else:
                    self.sendError("setRefVoff failed: %s" %"missing freq value")       
                    
                    
            elif data[0] == b"setsRefOutSwitch":
                if len(data)>1:
                        value = data[1]
                        self.setsRefOutSwitch(value)
                else:
                    self.sendError("setsRefOutSwitch failed: %s" %"missing freq value")  
                     
            elif data[0] == b"setsRefHarm":
                if len(data)>1:
                        value = data[1]
                        self.setsRefHarm(value)
                else:
                    self.sendError("setsRefHarm failed: %s" %"missing freq value")      
            
            elif data[0] == b"setupScope":
                try:
                    if len(data)==4:
                        self.scopeSetup(float (data[1]), float (data[2]), float (data[3]))
                    else:
                        self.scopeSetup()
                    self.sendAck()
                except Exception as e:
                    self.sendError("Cannot setupScope %s" %e)
            else:
                self.sendError()
        
        return True
#=====================================================================================================================
    def sendError(self, errorMessage = "Unknown request"):
        self.conn.sendall(errorMessage.encode("utf_8"))
    
    def sendAck(self):
        sendData = b"1"
        self.conn.sendall(sendData)