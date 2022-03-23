import meep as mp
import numpy as np
from datetime import date
import MyMeepFunctions as myF
import sys, getopt,os
from matplotlib import pyplot as plt


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
         gapDelta = int(str(arg))
      elif opt in ("-o", "--ofile"):
         filename = str(arg)
   return gapDelta,filename


gapIDX,filename = main(sys.argv[1:])

DecayFactor = 5e-4

#print(Simtime,filename)

print(gapIDX)
print(type(gapIDX))

print(filename)

gapDelta = np.array([4,5,6,7,8,9,10,11,12,13])*50e-3


Gap = 6.434e-01 + gapDelta[gapIDX]

print(Gap)

fsrc = 1/1.5475 # frequency of eigenmode or constant-amplitude source
df = 16e-3


nfreq = 3000
resolution = 20 #pixels per distance unit, so 10 px/um rn. (ideal)


#flux_freqs = mp.get_flux_freqs(src)

WGMr = 40
WGr = 0.5

sim,src,tran,sphereMode = myF.buildWGMmodel(WGMr,WGr,Gap,fsrc,df,resolution,nfreq)


t = (1e-6/3e8)
tFactor = 1e-15/t # converts femptoseconds into unitless MEEP 


#print("Actual Simtime:", Simtime*t)


today = str(date.today())

workingDir = 'data/'+today+'/'+filename+'/'

print('WD:',workingDir)

try:
   os.makedirs(workingDir)
except:
   print('AlreadyDir')

sim.use_output_directory(workingDir)


#print('figure')
plt.figure(dpi=200)
sim.plot2D(eps_parameters={'alpha':0.8, 'interpolation':'none'})
plt.savefig(workingDir+"ModelatStart.pdf")
#print('savefig')

#10500

pt = mp.Vector3(x=0,y=39.5)
myF.tic()
#sim.run(mp.at_beginning(mp.output_epsilon),
#        mp.at_every(10500, mp.output_dpwr),
#        until=(Simtime*tFactor))
#sim.run(mp.at_beginning(mp.output_epsilon),
#      mp.at_every(50000, mp.output_dpwr),
#      until_after_sources=mp.stop_when_fields_decayed(750,mp.Ez,pt,DecayFactor))



sim.run(
      #mp.at_beginning(mp.output_epsilon),
      #mp.at_every(50000, mp.output_dpwr),
      until=mp.stop_on_interrupt())


T = myF.toc()



plt.figure(dpi=200)
sim.plot2D(fields=mp.Ez,plot_sources_flag=True,plot_monitors_flag=True)
plt.savefig(workingDir+"FieldsAtEnd.pdf")

meta = {
        "GapDelta": gapDelta[gapIDX],
        "DecayFactor": DecayFactor,
        "Walltime": T,
        "Gap": Gap,
        "fsrc": fsrc,
        "df": df,
        "nfreq":nfreq,
        "resolution":resolution,
        "WGMradius":WGMr,
        "WGradius":WGr
    }


myF.dumpData2File(meta,today,workingDir,sim,src,tran,sphereMode,nfreq)

