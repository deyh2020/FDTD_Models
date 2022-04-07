import SidePolishModel.SidePolishModel.TwoDimensionTR.ModelOld as ModelOld
import sys

print ('Argument List:', str(sys.argv))

args = sys.argv

ModelOld = ModelOld.Model()


try:
    ModelOld.Variables['filename'] = str(sys.argv[1])
    ModelOld.Variables['roundTrips'] = float(sys.argv[2])
except:
    print("That didn't work")

if "nonormal" in args:
    print("not normalising")
    Solver.M.Variables['normal'] = False



if "justplot" in args:
    print("Just plotting")
    Solver.pltStructure()
elif "debug" in args:
    print("Debug Run")
    Solver.M.Variables['debug'] = True
    Solver.run()
else:
    print("Standard run")
    Solver.run()
