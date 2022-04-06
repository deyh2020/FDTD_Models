import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()


Model.filename = 'NEFFSolver'
Model.Datafile = ""
Model.Notes    = ""

Model.res = 10/1.55



Model.FibreType = "Polished"

ncoating = [1.00,1.41]

temps = [23,30,40,50,60,70,80]


neffPDMS = []
neff = []

Model.tic()

for t in temps:  

    print("")
    print("Working at "+ str(t))
    print("")

    Model.Datafile = "temp_" + str(t)

    Model.nCoating = 1
    Model.coreN = np.polyval(Model.SilicaFIT,t)
    Model.cladN = Model.coreN - 0.005

    Model.BuildAndSolveNEFF()

    neff.append(Model.neff)

for t in temps:  

    print("")
    print("Working at "+ str(t))
    print("")

    Model.Datafile = "PDMSCoated_temp_" + str(t)

    Model.nCoating = np.polyval(Model.PDMSfit,t)
    Model.coreN = np.polyval(Model.SilicaFIT,t)
    Model.cladN = Model.coreN - 0.005


    Model.BuildAndSolveNEFF()

    neffPDMS.append(Model.neff)

Model.toc()

print("Neffs")
print(neff)


fig,ax = plt.subplots(dpi=150)

ax.plot(temps,neff,label="Uncoated")
ax.plot(temps,neffPDMS,label="PDMS Coated")


ax.set_ylabel("$n_{eff}$")
ax.set_xlabel("Temp / C")
plt.legend()
plt.savefig(Model.workingDir+"NEFF" +".pdf")
#plt.show()
