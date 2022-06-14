import SidePolishFibre.OneDsolve as OneDsolve
import sys


Solver = OneDsolve.OneDsolve()


print ('Argument List:', str(sys.argv))

args = sys.argv

try:
    Solver.M.workingDir   = str(sys.argv[1])
    Solver.M.filename     = str(sys.argv[2])


except:
    print("That didn't work")

Solver.run()