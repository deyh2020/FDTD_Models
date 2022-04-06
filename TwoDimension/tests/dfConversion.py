import numpy as np

c = 1.00


StartWL = 1.520
EndWl  = 1.580

dppnm   = 100
res     = (1/dppnm)/1000   #nm

fcen  = 1.0/((EndWl + StartWL)/2.0)
df    = ((1/StartWL) - (1/EndWl))
nfreq = int((EndWl-StartWL)/res)

print("fcen: "+str(fcen))
print("df: "+str(df))
print("dpts: "+str(nfreq))