import model as m
import sys

print ('Argument List:', str(sys.argv))

args = sys.argv

Model = m.Model()
Model.SidePolish()

try:
    Model.structure.Variables['workingDir']   = str(sys.argv[1])
    Model.structure.Variables['roundTrips'] = float(sys.argv[2])
except:
    print("That didn't work")

if "square" in args:
    Model.structure.Variables['angle'] = 90

if "justplot" in args:
    print("Just plotting")
    Model.PlotStructure()
else:
    print("Standard run")
    Model.RunTRspectrum()