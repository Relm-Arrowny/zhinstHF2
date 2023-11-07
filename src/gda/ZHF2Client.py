'''
Created on 27 Mar 2023

@author: wvx67826

@description: 
    zurich client
    JPython class to handle all client side of HF2Sever
    It send request to the server and handle responds 
    The server and client test with python 3 can be found here@
        https://github.com/Relm-Arrowny/zhinstHF2/tree/main/src
    manual:
        https://docs.zhinst.com/pdf/ziMFIA_UserManual.pdf
@version: 1.0
    First implementation of all user requested functions.
    
'''

from beamline.TCL_Controls.TCPSocket.TCPSocket import TCPSocket
import time
from binstar_client.commands import channel


class ZHF2Client(TCPSocket):
    def __init__(self, bufferSize = 1048, timeout = 5):
        super(ZHF2Client, self).__init__(bufferSize, timeout)
        

#================== get data ==============================================================
    def getData(self, time):
        com = ("getData %s" %time)
        self.sendCom(com)
        return self.readBuffer()

# Set parameters  
#  return 1/data for success and 0/ error message for failure 
    
    def autoV(self):
        com = "autoVoltageInRange" 
        self.sendCom(com)
        return self.readBuffer()
    
    def setTCons(self, value):
        com = "setTimeConstant %s" %value
        self.sendCom(com)
        return self.readBuffer()
    
    def setDataRate(self, value):
        com = "setDataRate %s" %value
        self.sendCom(com)
        return self.readBuffer()
    
    def setCurrentInRange(self, value):
        com = "setCurrentInRange %s" %value
        self.sendCom(com)
        return self.readBuffer()
    
    def autoCurrentInRange(self):
        com = "autoCurrentInRange"
        self.sendCom(com)
        return self.readBuffer()
    def setupScope(self, freq = None, numDataPoint = None, channel = None):
        if (freq == None and numDataPoint== None and channel== None):
            com = "setupScope"
        else:
            com = "setupScope %s %s %s" %(freq, numDataPoint, channel)
        self.sendCom(com)
        return self.readBuffer()
    def setRefFreq(self, value):
        com = "setRefFreq %s" %value
        self.sendCom(com)
        return self.readBuffer()
    def setRefVpk(self, value):
        com = "setRefVpk %s" %value
        self.sendCom(com)
        return self.readBuffer()
    def setRefVoff(self, value):
        com = "setRefVoff %s" %value
        self.sendCom(com)
        return self.readBuffer()
    def setsRefOutSwitch(self, value):
        com = "setsRefOutSwitch %s" %value
        self.sendCom(com)
        return self.readBuffer()
    def setsRefHarm(self, value):
        com = "setsRefHarm %s" %value
        self.sendCom(com)
        return self.readBuffer()
     
         
HOST = "172.23.110.69" # The server's hostname or IP address for Hutch Windows computer
PORT = 7891  # The port used by the server

zur = ZHF2Client(bufferSize = 2048, timeout = 15)
print(zur.connection(HOST, PORT))
""" #tests
print zur.getData(2)
print zur.setTCons(1e-6)
print zur.setDataRate(1e4)
print zur.setCurrentInRange(1e-3)
print zur.autoCurrentInRange()
"""