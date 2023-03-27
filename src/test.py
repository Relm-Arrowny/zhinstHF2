'''
Created on 24 Mar 2023

@author: wvx67826
'''
import zhinst.core
import numpy as np
device_id = "dev4206"

server_host = "172.23.110.84"
server_port = 8004
api_level = 1

# Create an API session to the Data Server.
zhinst.core.ziDAQServer("172.23.110.84",8004, 1)
daq = zhinst.core.ziDAQServer(server_host, server_port, api_level)

sample = daq.getSample(f"/{device_id}/demods/0/sample")
print(sample)
X = sample['x'][0]
Y = sample['y'][0]
Phase = sample["phase"][0]

print(f"Measured in-phase component:\t {X:.3e} A")
print(f"Measured quadrature component:\t {Y:.3e} A")
print(f"Measured quadrature component:\t {Phase:.3e} V")

R = np.abs(X + 1j*Y)
Theta = np.arctan2(Y,X)
print(f"Measured RMS amplitude:\t {R:.3e} V")
print(f"Measured signal phase:\t {(180/np.pi)*Theta:.2f} deg")
