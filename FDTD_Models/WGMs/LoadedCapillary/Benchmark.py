import Model as M
import numpy as np
import meep as mp
import matplotlib.pyplot as plt



Model = M.Model() 

#mp.verbosity(2)

#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.


Model.filename = 'Benchmarks'

Model.Width = 300
Model.Depth = Model.R1 + Model.R2 + 4
Model.BubblesNum = 1


Model.res = 8
Model.df = 0.042

#Model.TestSpectrum()

#plt.show()

 
Model.Datafile = "Bench"

Model.nCoating = 1.00

Model.RunTRspectrumUnPolished()



#plt.show()
