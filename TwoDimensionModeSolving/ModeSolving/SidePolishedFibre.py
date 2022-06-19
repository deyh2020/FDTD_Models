"""
This file is the setup for the sidepolished fibre mode and NEFF experiment. This file has arguments so in the format of:

python SidepolishedFibre.py workingDirectory 

where the first argument is the working directory. 

flags can be added such as:

justplot   -- only builds structure and plots 

unpolished -- builds a unpolished fibre.


"""

import model as m
import sys

print ('Argument List:', str(sys.argv))
args = sys.argv



#import your strucutre file
import SidePolishedFibre.structure as structure
device = structure.structure()


Model = m.Model(device)



try:
    Model.structure.Variables['workingDir']   = str(sys.argv[1])

except:
    print("filename not given")



if "unpolished" in args:
    Model.structure.Variables['FibreType'] = "unpolished"
 

if "PDMS" in args:
    Model.structure.Variables['nCoating'] = 1.410
else:
    Model.structure.Variables['nCoating'] = 1.000


if "justplot" in args:
    print("Just plotting")
    Model.PlotStructure()


if "solve" in args:
    print("Solving mode")
    Model.BuildAndSolve()

if "solveNEFF" in args:
    print("Solving NEFF")
    Model.BuildAndSolveNEFF()


import experiments.NEFFvsTemp as exp


if "NEFFvsTemp" in args:
    print("Exicuting NEFF experiment")
    exp.experiment(Model)

