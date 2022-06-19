from re import S
import Model as M
import time as time
import numpy as np
import matplotlib.pyplot as plt
import h5py
from os import listdir


class CWsolve:

    def __init__(self):

        self.M = M.Model()
        self.M.res = 4
        self.M.FibreType = "Polished"
        self.M.SimSize = 20
        
        self.temps = np.array([23,30,40,50,60,70,80])
        self.neffPDMS = np.array([])
        self.neff     = np.array([])
        self.neffPDMS = np.array([])
           
    def run(self):


       
        

        self.M.filename = 'Air'
        self.M.nCoating = 1.00

        self.RUN("TL")
        
        
        self.M.filename = 'PDMS'
        self.M.nCoating = 1.41
        
        self.RUN("BR")

        plt.show()
    

    def RUN(self,figPos):

        fig, ax1 = plt.subplots(figsize=[12,9])
        # inset smaller axis
        xlim = ax1.get_xlim()
        ylim = ax1.get_ylim()

        ax2Size = 0.45
        if figPos == "TL":
            ax2 = ax1.inset_axes([xlim[0] + 0.025, ylim[1] - ax2Size - 0.05 , ax2Size, ax2Size])
        elif figPos == "BR":
            ax2 = ax1.inset_axes([xlim[1] - 0.025 - ax2Size, ylim[0] + 0.1 , ax2Size, ax2Size])

        ax2.text(-5.5, 5.5 ,self.M.filename,fontsize=16,color="white")
        

        self.M.BuildAndSolve() #Runs CW sim and saves eps and ey fields. 
        
        self.plotFieldProfile(ax2)

        self.runNEFFexp(ax1)
        

        plt.savefig(self.M.workingDir+"FullFigure"+ self.M.filename +".pdf")
        self.M.sim.reset_meep()

    
    def importh5(self):
        directory = self.M.workingDir
        epsFile = "runner-eps-000000.00.h5"
        eyFile = "runner-ey-000000.00.h5"
        eps = np.flip( np.transpose( np.array( h5py.File(directory + epsFile,'r')['eps'] ) ),0 )
        ey = np.flip( np.transpose( np.array( h5py.File(directory + eyFile,'r')['ey.r'] ) ),0 )
        return eps,ey
    
    def plotFieldProfile(self,ax):

        eps,ey = self.importh5()

        dx = self.M.SimSize/2

        ext = (-dx,dx,-dx,dx)


        ax.imshow(ey,
                extent=ext,
                interpolation='antialiased',
                cmap='viridis',
                vmax= np.max(ey),
                vmin= 0
                )

        ax.autoscale(False)
        ax.set_xlim(-self.M.R1*1.8,self.M.R1*1.8)
        ax.set_ylim(-self.M.R1*1.8,self.M.R1*1.8)
        

        from matplotlib.patches import Circle, Rectangle
        

        circ = Circle((0,0),self.M.R1,fill=False)
        ax.add_patch(circ)

        Rect = Rectangle((-dx,self.M.R1 + self.M.Pad),2*dx,0,fill=False)
        ax.add_patch(Rect)
       
        eps = (eps - 1.00)**15  #scale the eps values to show small contrasts better
        
        """
        axes.imshow(eps,
                alpha=0.25,
                interpolation="none",
                extent=ext,
                cmap='binary',
                vmax=np.max(eps),
                vmin=0.00
                )
        """

        ax.set_xlabel("X / um",fontsize=16)
        ax.set_ylabel("Y / um",fontsize=16)
        ax.ticklabel_format(style='sci',scilimits=(-1,5),axis='both',useOffset=False)

        #plt.savefig(self.M.workingDir+"FieldProfile"+ self.M.filename +".pdf")


    def runNEFFexp(self,ax):

        self.neff = np.array([])
        
        for t in self.temps:  

            print("")
            print("Working at "+ str(t))
            print("")

            self.M.Datafile = self.M.Coating + "_temp_" + str(t)

            if self.M.filename == "Air":
                self.M.nCoating = 1
            elif self.M.filename == "PDMS":
                self.M.nCoating = np.polyval(self.M.PDMSfit,t)
            else:
                print("filename needs to be Air or PDMS")


            self.M.coreN = np.polyval(self.M.SilicaFIT,t)
            self.M.cladN = self.M.coreN - 0.005

            self.M.BuildAndSolveNEFF()

            self.neff =  np.append(self.neff,self.M.neff)



        ax.plot(self.temps,self.neff,linestyle='--',marker='o',linewidth=3,markersize=12)
        

        ax.set_ylim(1.4419,1.4426)
        ax.set_ylabel("Effective Refractive Index",fontsize=16)
        ax.set_xlabel("Temp / C",fontsize=16)
        ax.ticklabel_format(style='sci',scilimits=(-1,5),axis='both',useOffset=False)
        ax.grid(b=True, which='major', color='grey', linestyle='-',alpha=0.4)
        ax.grid(b=True, which='minor', color='grey', linestyle='--',alpha=0.4)
        ax.minorticks_on()  


if __name__ ==  '__main__':

    CW = CWsolve()


    import sys

    print ('Argument List:', str(sys.argv))

    args = sys.argv

    try:
        CW.M.workingDir   = str(sys.argv[1])

    except:
        print("That didn't work")


    CW.run()