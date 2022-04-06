import model as m
import sys

print ('Argument List:', str(sys.argv))

args = sys.argv

Model = m.Model()

try:
    Model.structure.Variables['filename']   = str(sys.argv[1])
    Model.structure.Variables['roundTrips'] = float(sys.argv[2])
except:
    print("That didn't work")

"""
if "enablefluxregion" in args:
    print("enabling flux region")
    Solver.M.FluxRegion = True
"""

if "justplot" in args:
    print("Just plotting")
    Model.PlotStructure()
else:
    print("Standard run")
    Model.RunTRspectrum()