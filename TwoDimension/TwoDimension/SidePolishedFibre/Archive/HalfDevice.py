import Model as M
import numpy as np
import meep as mp
import matplotlib.pyplot as plt



Model = M.Model() 

#mp.verbosity(2)

#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.


Model.GAP = 0
Model.Width = 322.4
Model.Depth = 55.7
Model.angle = 121.4


Model.filename = 'SingleDip_PDMS_Desktop_Wideband2'

Model.df = 10e-2
Model.res = 10/1.55  # at least 10 px per wavelength
Model.Courant = 1/np.sqrt(2)
Model.fcen = 1/1.55

#Model.TestSpectrum()

#plt.show()

 
Model.Datafile = "Bench"

Model.nCoating = 1.41

Model.RunTRspectrum()



#plt.show()
