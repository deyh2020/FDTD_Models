import SidePolishFibre.Model as M
import matplotlib.pyplot as plt
import csv
import numpy as np

import h5py


class OneDsolve: 

    def __init__(self):

        self.M = M.Model()

        self.M.filename = 'default'
        self.M.Datafile = 'default'

        self.Air = 1.00
        self.Core = 1.445
        self.Clad = 1.440
        self.PDMS = 1.410 

        self.M.Mthick         = 65
        self.M.Pad           = 100
        self.M.BackgroundN = self.Core  
        self.M.N1          = self.Air

        #self.M.N2          = self.M.N1    


        #Simulation source Properties
        StartWL = 1.5
        EndWL   = 1.6
        WLres   = 0.001/1000 #res in um so 1pm
        Courant = 1


        self.M.fcen    = 1.0/((EndWL + StartWL)/2.0)
        self.M.df      = ((1/StartWL) - (1/EndWL))
        self.M.dfreq   = int((EndWL-StartWL)/WLres)

        self.M.res     = 10/1.55  # at least 10 px per wavelength
        self.M.Courant = 1

        


    def run(self):

        #self.mode_1()
        #self.mode_2(    
        #self.plotEXP()
        self.full1D()
        plt.show()


    def full1D(self):

        self.M.Datafile    = 'All'
        self.M.BackgroundN = self.Core
        self.M.N1          = self.Air
        self.M.N2          = self.Air

        #Layer width is in um
        self.M.GAP         = 1000
    
        self.M.Mthick      = 65#322

        self.M.RunTRspectrumSingleFP()
        #self.M.RunTRspectrumDoubleFP()
        self.plotEPS()



    def plotEPS(self):  
        filename = self.M.workingDir + "oneDsolve-eps-000000.00.h5"
        with h5py.File(filename,'r') as f:    
            eps = np.flipud(np.array(f['eps']).transpose())

        
        sx = self.M.sx

        x = np.linspace(-sx/2,sx/2,len(eps))

        fig,ax = plt.subplots(dpi=200)

        ax.plot(x,np.sqrt(eps))


        ax.set_title("Structure",fontsize=16)
        ax.set_xlabel("Position / um",fontsize=16)
        ax.set_ylabel("refractive index",fontsize=16)
        plt.savefig(self.M.workingDir+"Structure.pdf")

        plt.show()


    def mode_1(self):
        #single layer, one dimention cavity composed of glass surrounded by air.
        #is the cavity created by having dips at either end.

        self.M.Datafile    = 'Mode_1'
        self.M.BackgroundN = self.Air
        self.M.N1          = self.Core

        #Layer width is in um
        self.M.Width         = 1682.8

        self.M.RunTRspectrumSingleFP()

    def mode_2(self):
        #single layer, one dimention cavity composed of air surroinded by glass, made through
        #evaporating the glass using a CO2 laser

        self.M.Datafile    = 'Mode_2'
        self.M.BackgroundN = self.Core
        self.M.N1          = self.Air

        #Width of dips
        self.M.Width         = 2000
    

        self.M.RunTRspectrumSingleFP()


    def plotEXP(self):
        filename = "../data/Experimental/FPRS without PDMS coated/0_5.csv"
        wlLine = 14
        pwrLine = 15

       

        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            line = 0
            for row in spamreader:
                #print(line)
                if line == wlLine:
                    wl = np.array(row,dtype=float)

                if line == pwrLine:
                    Ts = np.array(row,dtype=float)  
                    
                               
                line += 1 
        
        
        ax2 = self.M.axes.twinx()
        
        color = 'tab:red'
        ax2.plot(wl,Ts,color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.set_ylabel('db', color=color)


    def plotSim(self):
        print("Not Complete")