import meep as mp
import numpy as np
import matplotlib.pyplot as plt

class experiment:

    def __init__(self,Model):
        
        self.Variables = Model.structure.Variables

        self.Variables['Tdependance'] = True

        temps = [20,30,40,50,60,70,80]
        neff  = []

        for T in temps:
            self.Variables['T'] = T
            Model.BuildAndSolveNEFF()
            neff.append(Model.structure.neff)

        
        print(temps)
        print(neff)

        plt.plot(temps,neff)
        plt.show

