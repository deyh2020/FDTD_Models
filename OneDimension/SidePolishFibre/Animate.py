import Model as M
import numpy as np
import matplotlib.pyplot as plt
import meep as mp

Model = M.Model() 

print(Model.sim)


#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.

Model.GAP = 100
Model.Mthick = 5

Model.df = 15e-2

Model.res = 10/1.55  # at least 10 px per wavelength



Model.Courant = 1



Model.BackgroundN = 1.41
Model.N1 = 1.00
Model.N2 = Model.N1

Model.filename = '1D_Test'
Model.buildFaboryPeriot()
Model.BuildModel()


Model.SimT = Model.sx*10


#Model.sim.run(
#    mp.at_beginning(mp.output_epsilon),
#    until_after_sources=5000
#    )

Model.sim.run(
    #mp.at_beginning(mp.output_epsilon),
    #mp.at_every(100, mp.output_efield_z), 
    until=Model.SimT
)



flux_freqs = np.array(mp.get_flux_freqs(Model.refl))
#Rs = mp.get_fluxes(Model.refl)
Ts = mp.get_fluxes(Model.tranE)

wl = 1/flux_freqs

plt.figure()
plt.plot(wl,Ts,label='transmittance')
#plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")
plt.legend(loc="upper right")
plt.xlim(1.50,1.60)

plt.savefig(Model.workingDir+"TransRef_" + str(Model.Datafile) +".pdf")

