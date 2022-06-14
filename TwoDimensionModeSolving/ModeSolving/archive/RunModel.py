import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()


Model.filename = 'ModelTrio'
Model.Notes    = ''

Model.res = 4


temps = [23,30,40,50,60,70,80]



"""
Polished and PDMS coated
"""


PDMSneff = []
Model.nCoating = 1.41

Model.tic()
for t in temps:  

    Model.Datafile = "PDMSCoated_temp_" + str(t)

    Model.nCoating = np.polyval(Model.PDMSfit,t)
    Model.coreN = np.polyval(Model.SilicaFIT,t)
    Model.cladN = Model.coreN - 0.005
    
    print(Model.nCoating)
    print(Model.coreN)


    Model.Objlist = []
    Model.buildPolishedFibre()
    Model.BuildModel(Plot=False) 
    Model.RunMPB()
    PDMSneff.append(Model.neff)
    Model.sim.reset_meep()  

Model.toc()

fig,ax = plt.subplots(dpi=150)

ax.plot(temps,PDMSneff)


ax.set_ylabel("$\Delta n_{eff}$ / $1e-3$")
ax.set_xlabel("Temp / C")

plt.show()

print(PDMSneff)

"""

"""
#Polished and Un-Coated Model
"""

python
    Model.Datafile = "Uncoated_" + str(n)

    Model.coreN = n
    Model.cladN = n - 0.005
    Model.Objlist = []
    #Model.buildFibre()
    Model.buildPolishedFibre()
    Model.BuildModel(Plot=False) 
    Model.RunMPB()
    Uncoatedneff.append(Model.neff)
    Model.sim.reset_meep()  


"""
#Standard SMF-28 Fibre
"""

NormalFibre = []

for n in Model.nSilica: 
    Model.Datafile = "NormalFibre_" + str(n)
    
    Model.coreN = n
    Model.cladN = n - 0.005
    Model.Objlist = []
    Model.buildFibre()
    Model.BuildModel(Plot=False) 
    Model.RunMPB()
    Model.RunAndPlotF()
    #Model.SaveMeta()
    NormalFibre.append(Model.neff)












fig,ax = plt.subplots(dpi=150)

ax.plot(Model.PDMStemp,PDMSneff*1e3)

ax.plot(Model.Silicatemp,neff*1e3)
#ax.set_ylim(Model.cladN,Model.coreN)
ax.set_xlim(20,80)

ax.set_ylabel("$\Delta n_{eff}$ / $1e-3$")
ax.set_xlabel("Temp / C")

plt.show()

"""