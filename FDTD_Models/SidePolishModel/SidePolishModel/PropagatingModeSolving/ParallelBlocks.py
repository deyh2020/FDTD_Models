import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt

Model = M.Model()


Model.filename = 'ModelTrio'
Model.Datafile = "NormalFibre"
Model.Notes    = ''

Model.res = 3
Model.SimT=19


Types = ['Standard','Polished','Polished']
ncoating = [1.00,1.00,1.41]

Model.nCoating = 1.00

Model.SimSize= 100
Model.height = 40

Model.FibreType = 'Polished'
Model.BuildAndSolveParallel()

plt.show()