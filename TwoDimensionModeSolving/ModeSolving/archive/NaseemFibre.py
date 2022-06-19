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
        self.M.res = 10
        self.M.FibreType = "Standard"
        self.M.SimSize = 20

        self.M.coreN = 1.620
        self.M.cladN = 1.440 
        self.M.R1    = 2.5
        self.M.R2    = 72.5
    

    def RUN(self):

        #fig, ax1 = plt.subplots(figsize=[12,9])
    
        

        self.M.BuildAndSolve() #Runs CW sim and saves eps and ey fields. 
        
        #print("NEFF= ",self.M.neff)

        
        

        plt.savefig(self.M.workingDir+"FullFigure"+ self.M.filename +".pdf")
        plt.show()

    
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


if __name__ ==  '__main__':

    CW = CWsolve()


    import sys

    print ('Argument List:', str(sys.argv))

    args = sys.argv

    try:
        CW.M.workingDir   = str(sys.argv[1])

    except:
        print("That didn't work")


    CW.RUN()