import Model as M
import numpy as np
import matplotlib.pyplot as plt
import meep as mp

Model = M.Model() 

print(Model.sim)


#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.

Model.Width = 10



Model.df = 0.042


Model.res = 10/1.55  # at least 10 px per wavelength

Model.cladN = 1.000
Model.R1 = 8

Model.Courant = 1/np.sqrt(2)

Model.filename = 'CapillaryAnimationQuater3'


Model.WallThick = 3

Model.buildFilledCapillary()
Model.BuildModel()


Model.SimT = 1000


Model.sim.run(
    mp.at_beginning(mp.output_epsilon),
    until_after_sources=5000
    )

Model.sim.run(
    mp.at_every(100, mp.output_efield_z), 
    until=Model.SimT
)