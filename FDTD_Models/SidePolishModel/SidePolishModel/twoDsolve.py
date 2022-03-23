import TwoDimensionTR.TwoDsolve as TwoDsolve
import sys

print ('Argument List:', str(sys.argv))

args = sys.argv

Solver = TwoDsolve.TwoDsolve()
Solver.M.Pad = 100

try:
    Solver.M.GAP      = float(sys.argv[1])
    Solver.M.Pad      = float(sys.argv[2])
    Solver.M.filename = str(sys.argv[3])
except:
    print("That didn't work")

if "enablefluxregion" in args:
    print("enabling flux region")
    Solver.M.FluxRegion = True

if "nonormal" in args:
    print("not normalising")
    Solver.M.normal = False

if "squaredips" in args:
    print("Using square dips")
    Solver.M.angle = 90



if "justplot" in args:
    print("Just plotting")
    Solver.pltStructure()
elif "square" in args:
    print("Sqr bubbles")
    Solver.sqrBubbles()
else:
    print("Standard run")
    Solver.run()
