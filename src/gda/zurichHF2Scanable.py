'''
Created on 25 Apr 2023

@author: wvx67826
@description:
    gda scanable that take zurich client object and perform different 
    get/set function on the zurich lockin
    zurich client class:
        /dls_sw/i10/scripts/beamline/TCL_Controls/zurichHF2/ZHF2Client.py
    manual:
        https://docs.zhinst.com/pdf/ziMFIA_UserManual.pdf
@version: 1.0
     scanable require zhf2client object it return x y,R and theta from the lockin
'''
from gda.device.scannable import ScannableBase

class zurichHF2Scanable(ScannableBase):
    def __init__(self,name, zur):
        
        self.zur = zur
        self.setName(name);
        self.setInputNames(["X"])
        self.setExtraNames(["Y", "Theta","static","R"])
        self.setOutputFormat(["%.6g"])
        self.level = 110
        self.countTime = 0;
        self.data = 0
        
    def atScanStart(self):
        pass
    def atPointStart(self):
        pass
        
    def rawGetPosition(self):
        self.iambusy = 1
        
        self.data = map(float,self.zur.getData(self.countTime).split(","))
        wait(self.countTime+0.1)
        self.iambusy = 0
        return self.data
    
    def rawAsynchronousMoveTo(self,new_position):
        self.iambusy = 1
        self.countTime = new_position
        
        self.iambusy = 0

    def isBusy(self):
        return self.iambusy
    
    def atPointEnd(self):
        pass
    
    def atScanEnd(self):
        pass
