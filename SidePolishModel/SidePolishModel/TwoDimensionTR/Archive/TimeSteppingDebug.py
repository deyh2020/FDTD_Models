import Model as M
import numpy as np
import matplotlib.pyplot as plt
import meep as mp

Model = M.Model() 


#Set the PDMSn = 1 for effectively a uncoated side-polished fibre.

Model.GAP = 0
Model.Width = 300
Model.Depth = Model.R1 + Model.R2 + 4
Model.BubblesNum = 1

Model.filename = 'ElongatedCircTest2_batch_'

#Model.nCoating = 1.00
Model.df = 0.042
Model.res = 5

Model.nCoating = 1.000


for i in [0,5,10,15,20]:

    print("")
    print("")
    print("")
    print("Depth + " + str(i))
    print("")
    print("")
    print("")

    Model.filename = 'Topsy_batch_' + str(i)

    Model.Depth = Model.R1 + Model.R2 + i

    Model.Objlist = []	
    Model.buildNormalfibre()
    Model.ADDcircElongated()

    Model.BuildModel(NormRun=False,Plot=False) 


    Model.SimT = 4000

    Model.sim.run(
        mp.at_beginning(mp.output_epsilon),
        mp.at_every(100, mp.output_dpwr),
        until=Model.SimT
    )

    Model.sim.reset_meep()