import Model as M
import numpy as np
import meep as mp


Model = M.Model() 

#mp.verbosity(2)

#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.


Model.nCoating = 1.41

Model.Notes    = ''
Model.Datafile = "Data"


#Model.filename = 'SingleBubble_Temp_' + str(T)

Model.GAP = 0

Model.Width = 300

Model.Objlist = []

Model.buildPolishedFibre()

#Build model with everything.
Model.sqrBubbles(Num=1)
Model.BuildModel(NormRun=False,Plot=True) 
# for normal run, load negated fields to subtract incident from refl. fields
#Model.sim.load_minus_flux_data(Model.refl, Model.norm_refl)
#Run until fields decayed by 1e3

#Model.tic()
#Model.AutoRun()
#Model.toc()
#Model.SaveMeta()
#


"""

temps = [23,30,40,50,60,70,80]


for T in temps:  

    Model.filename = 'SingleBubble_Temp_' + str(T)

    Model.GAP = g
    Model.Objlist = []
    
    Model.buildPolished()

    #do normalisation run only needs to be done once
    #build model without defects

    Model.BuildModel(NormRun=True,Plot=False) 

    Model.tic()
    Model.NormRun()
    Model.toc()

    #resetMEEP
    Model.sim.reset_meep()
    #Build model with everything.
    Model.sqrBubbles(Num=1)
    Model.BuildModel(NormRun=False,Plot=False) 
    # for normal run, load negated fields to subtract incident from refl. fields
    Model.sim.load_minus_flux_data(Model.refl, Model.norm_refl)
    #Run until fields decayed by 1e3

    Model.tic()
    Model.AutoRun()
    Model.toc()
    Model.SaveMeta()

    Model.sim.reset_meep()

"""
