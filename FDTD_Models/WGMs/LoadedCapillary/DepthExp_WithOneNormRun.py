import Model as M
import numpy as np
import meep as mp
import matplotlib.pyplot as plt



Model = M.Model() 

#mp.verbosity(2)

#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.


temps = [20]


Model.Width = 300
Model.BubblesNum = 1

Model.df = 0.042

#Model.TestSpectrum()

#plt.show()

depths = [5,10,15]



Model.SingleNorm = True
for D in depths:

    Model.filename = 'TR_Desktop_Depth_' + str(D)

    Model.Depth = Model.R1 + Model.R2 + D


    for T in temps:  

        Model.Datafile = "Coated_temp_" + str(T)

        Model.nCoating = np.polyval(Model.PDMSfit,T)
        Model.coreN = np.polyval(Model.SilicaFIT,T)
        Model.cladN = Model.coreN - 0.005
        
        Model.RunTRspectrumUnPolished()


    
        Model.Datafile = "Uncoated_temp_" + str(T)

        Model.nCoating = 1.00
        Model.coreN = np.polyval(Model.SilicaFIT,T)
        Model.cladN = Model.coreN - 0.005
        
        Model.RunTRspectrumUnPolished()




#plt.show()
