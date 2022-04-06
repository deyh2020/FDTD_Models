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
resolution = 20 #pixels per distance unit, so 10 px/um rn. (ideal)


#flux_freqs = mp.get_flux_freqs(src)

WGMr = 40
WGr = 0.5

sim,src,tran,sphereMode,pt = myF.buildWGMmodel(WGMr,WGr,Gap,fsrc,df,resolution,nfreq)


t = (1e-6/3e8)
tFactor = 1e-15/t # converts femptoseconds into unitless MEEP 


print("Actual Simtime:", Simtime*t)


today = str(date.today())

sim.use_output_directory('data/'+today)


from matplotlib import pyplot as plt
plt.figure(dpi=200)
sim.plot2D()
plt.savefig("data/" +today+"/"+filename+"ModelatStart.pdf")


myF.tic()
sim.run(mp.at_beginning(mp.output_epsilon),
        mp.at_every(10500, mp.output_dpwr),
        until=(Simtime*tFactor))
#sim.run(until_after_sources=mp.stop_when_fields_decayed(50,mp.Ez,pt,1e-3))

T = myF.toc()



plt.figure(dpi=200)
sim.plot2D(fields=mp.Ez,plot_sources_flag=True,plot_monitors_flag=True)
plt.savefig("data/"+today+"/"+filename+"FieldsAtEnd.pdf")

meta = {
        "Simtime": Simtime,
        "Walltime": T,
        "Gap": Gap,
        "fsrc": fsrc,
        "df": df,
        "nfreq":nfreq,
        "resolution":resolution,
        "WGMradius":WGMr,
        "WGradius":WGr
    }


myF.dumpData2File(,today,filename,sim,src,tran,sphereMode,nfreq)

