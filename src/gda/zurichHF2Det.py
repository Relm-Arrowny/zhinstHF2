'''
Created on 25 Apr 2023

@author: wvx67826

@description:
    gda deector for zurich lockin amplifier, it requires ZHF2Client object

@version 1.0
    
'''

from gda.device.detector import DetectorBase
from gda.device.scannable import ScannableBase
import scisoftpy as dnp
import time

class zurichHF2Det(DetectorBase):
    def __init__(self, zur):
        self.setName("zurich")
        self.setInputNames(['collectionTime'])
        self.setExtraNames(['x', 'y', 'theta', "static", "R"])
        self.setOutputFormat(["%5.5g","%5.5g","%5.5g","%5.5g","%5.5g","%5.5g"])
        self.collectionTime = 1
        self.startCollectionTime = 0
        self.zur = zur


    def collectData(self):
        self.startCollectionTime = time.time()

    def getStatus(self):
        return (self.startCollectionTime + self.collectionTime  >= time.time())

    def readout(self):    
        self.data = map(float,self.zur.getData(self.collectionTime).split(","))
        return self.data
    
    def getDataDimensions(self):
        return 1
    
    def createsOwnFiles(self):
        return False
    

