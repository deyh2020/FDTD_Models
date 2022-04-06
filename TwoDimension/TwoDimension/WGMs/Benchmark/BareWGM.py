import meep as mp
import numpy as np
from datetime import date
import pickle,json
import MyMeepFunctions as myF
import sys, getopt

# -r for runtime in fs
# -f for filename




def main(argv):
   runtime = 1e2
   filename = 'test'
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         runtime = float(arg)
      elif opt in ("-o", "--ofile"):
         filename = str(arg)
   return runtime,filename


Simtime,filename = main(sys.argv[1:])

print(Simtime,filename)



Gap = 6.434e-01


fsrc = 1/1.5475 # frequency of eigenmode or constant-amplitude source
df = 16e-3


nfreq = 3000
resolution = 10 #pixels per distance unit, so 10 px/um rn. (ideal)


#flux_freqs = mp.get_flux_freqs(src)

sim,src,tran,sphereMode = myF.buildWGMmodel(40,1/2,Gap,fsrc,df,resolution,nfreq)


t = (1e-6/3e8)
tFactor = 1e-15/t # converts femptoseconds into unitless MEEP 



from matplotlib import pyplot as plt
#plt.figure(dpi=200)
#sim.plot2D()
#plt.savefig("Model.pdf")

print("Actual Simtime:", Simtime*t)

from matplotlib import pyplot as plt
plt.figure(dpi=200)
sim.plot2D()
plt.savefig("data/"+filename+"ModelatStart.pdf")


sim.run(until=(Simtime*tFactor))


plt.figure(dpi=200)
sim.plot2D(fields=mp.Ez,plot_sources_flag=True,plot_monitors_flag=True)
plt.savefig("data/"+filename+"FieldsAtEnd.pdf")

myF.dumpData2File('data/'+filename,sim,src,tran,sphereMode,nfreq)

