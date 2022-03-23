import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()

#Model.nCoating = 1.000
Model.df     = 2e-2
Model.res = 3
Model.filename = 'SimsizeConvergeTopsy'
Model.Notes    = ''
Model.Pad = 0    #Cladding left over from polishing
Model.SimSize = 50
Model.wl = 1.55


Resolutions = [2,4,6,8,10,12,14,16,18,20]

Sizes = [20,40,80,130]


neff = []
Model.nCoating = 1.000
Model.res = 10

for s in Sizes:  
    
    Model.Datafile = str(s)
    Model.SimSize = s
    Model.Objlist = []
    #Model.buildFibre()
    Model.buildPolishedFibre()
    Model.BuildModel(Plot=False) 
    Model.RunMPB()
    neff.append(Model.neff)
    Model.sim.reset_meep()  



fig,ax = plt.subplots(dpi=150)

ax.plot(Sizes,neff)
#ax.set_ylim(Model.cladN,Model.coreN)
#ax.set_xlim(20,80)

ax.set_ylabel("$N_{\text{neff}}$")
ax.set_xlabel("Sim Size / um")
plt.savefig(Model.workingDir+"Converge.pdf")
plt.show()#