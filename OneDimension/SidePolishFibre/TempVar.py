import numpy as np
import Model as M
import matplotlib.pyplot as plt




Model = M.Model() 

Model.df = 0.2e-2
Model.res = 10/1.55  # at least 10 px per wavelength
Model.Courant = 1
Model.fcen = 1/1.60

Model.GAP = 1000

Model.BackgroundN = 1.00


Model.filename = '1D_TempVar_Air'
Model.Datafile = 'yes'

Model.fig,Model.axes = plt.subplots(1,1,dpi=200)


temps = [40,65,80]

Model.tic()
for t in temps:  

    Model.Datafile = str(t)

    Model.BackgroundN = 1.00 #np.polyval(Model.PDMSfit,t)
    Model.N1 = np.polyval(Model.SilicaFIT,t)


    Model.RunTRspectrum()



Model.toc()

