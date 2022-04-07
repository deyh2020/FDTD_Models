import Model as M



Model = M.Model() 


#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.
#Model.PDMSn = 1.41


Model.CladLeft = 5
Model.GAP = 110
Model.Width = 100
Model.fcen   = 1/1.55
Model.df     = 1.2e-2
Model.nfreq  = 10
Model.res = 3
Model.DecayF = 1e-3
Model.filename = 'LargerDeviceWPDMS'
Model.Notes    = ''

Model.buildPolished()




#do normalisation run
#build model without defects

Model.BuildModel(NormRun=False,Plot=False) 


Model.NormRun()



#resetMEEP
Model.sim.reset_meep()


#Build model with everything.
Model.sqrBubbles(Num=2)
Model.BuildModel(NormRun=False,Plot=False) 



# for normal run, load negated fields to subtract incident from refl. fields
Model.sim.load_minus_flux_data(Model.refl, Model.norm_refl)

#Run until fields decayed by 1e3
Model.AutoRun()

Model.SaveMeta()

