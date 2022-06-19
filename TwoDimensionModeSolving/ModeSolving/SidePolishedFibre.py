import model as m
import sys

print ('Argument List:', str(sys.argv))

args = sys.argv

Model = m.Model()
Model.SidePolish()

try:
    Model.structure.Variables['workingDir']   = str(sys.argv[1])

except:
    print("That didn't work")

if "unpolished" in args:
    Model.structure.Variables['Polished'] = False
 
if "justplot" in args:
    print("Just plotting")
    Model.PlotStructure()
else:
    print("Standard run")
    Model.RunTRspectrum()
