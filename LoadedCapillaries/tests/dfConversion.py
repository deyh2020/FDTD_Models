import numpy as np

c = 1.00


StartWL = 1.520
StopWl  = 1.580
res     = 0.01/1000   #nm

dpts = (StopWl-StartWL)/res
df  = ((1/StartWL) - (1/StopWl))
fcen = c/((StopWl + StartWL)/2.0)

print("fcen: "+str(fcen))
print("df: "+str(df))
print("dpts: "+str(dpts))