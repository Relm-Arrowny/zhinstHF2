'''
Created on 24 Mar 2023

@author: wvx67826
'''
import socket
import zhinst.core
import time
import matplotlib.pyplot as plt

daq = zhinst.core.ziDAQServer("172.23.110.84",8004,6)

h = daq.scopeModule()

#=========== setup scope ==================================
daq.set('/dev4206/scopes/0/time', 5)
daq.set('/dev4206/scopes/0/length', 4096)
daq.set('/dev4206/scopes/0/channels/0/inputselect', 0)
daq.set('/dev4206/scopes/0/enable', 1)

#================= take a single shoot ==================
#result = h.read(True)
h.subscribe('/dev4206/scopes/0/wave/')
h.execute()
daq.setInt('/dev4206/scopes/0/single', 1)
daq.setInt('/dev4206/scopes/0/enable', 1)
daq.sync()
time.sleep(0.1)
h.finish()
#h.unsubscribe('*')

result = h.read()

print (result)
h.unsubscribe('*')
#===============================================================
plt.plot(result ["dev4206"]["scopes"]["0"]["wave"][0][0]["wave"][0])
plt.show()