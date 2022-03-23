import TwoDimensionTR.TwoDsolve as TwoDsolve
import sys

print ('Argument List:', str(sys.argv))

args = sys.argv

Solver = TwoDsolve.TwoDsolve()
Solver.M.Pad = 100

try:
    #Solver.M.GAP      = float(sys.argv[1])
    #Solver.M.Pad      = float(sys.argv[2])
    Solver.M.Variables['filename'] = str(sys.argv[3])
except:
    print("That didn't work")

if "nonormal" in args:
    print("not normalising")
    Solver.M.Variables['normal'] = False



if "justplot" in args:
    print("Just plotting")
    Solver.pltStructure()
else:
    print("Standard run")
    Solver.run()
