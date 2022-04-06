import TwoDimensionTR.Model as M
import matplotlib.pyplot as plt
import csv
import numpy as np



class TwoDsolve: 

    def __init__(self):

        self.M = M.Model()

    def run(self):

        #self.mode_1()
        #self.mode_2(    
        #self.plotEXP()
        self.M.RunTRspectrum()

    def debug(self):
        self.M.RunTRspectrum()



    def sqrBubbles(self):
        self.M.angle = 90
        self.M.AutoRun()


    
    def pltStructure(self):
        self.M.PlotStructure()


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