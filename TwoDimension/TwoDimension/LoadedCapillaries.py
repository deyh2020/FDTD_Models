import model as m
import sys

print ('Argument List:', str(sys.argv))

args = sys.argv

Model = m.Model()
Model.LoadedCap()

try:
    Model.structure.Variables['workingDir']   = str(sys.argv[1])
    Model.structure.Variables['roundTrips'] = float(sys.argv[2])
    Model.structure.Variables['WallThick'] = float(sys.argv[3])
except:
    print("That didn't work")

if "solidCore" in args:
    print("Solid Clad Core")
    Model.structure.Variables['nPDMS'] = Model.structure.Variables['nClad']

if "justplot" in args:
    print("Just plotting")
    Model.PlotStructure()
else:
    print("Standard run")
    Model.RunTRspectrum()