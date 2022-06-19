 
import meep as mp
import numpy as np
import pickle,json, os
import time
import matplotlib.pyplot as plt
import h5py

class Model:

    """
    Because I want to have this as a somewhat modular bit of code, I'd like to have submodules for each structure type while maintaining a main model class with all the functions used for all models.

    init imports the variables 
    """

    def __init__(self,structure):
        self.structure = structure
        self.Variables = self.structure.Variables



    '''
    BuildAndSolve builds the model and solves the fundamental mode + plots.
    '''

    def BuildAndSolve(self,axes=None):
        self.Variables = self.structure.Variables
        self.structure.buildStructure()

        self.structure.BuildModel_CW()    
        
        self.structure.sim.init_sim()
        mp.output_epsilon(self.structure.sim)
        self.structure.sim.solve_cw()
        mp.output_efield_y(self.structure.sim)
        self.saveMetaData()
        self.PlotMode()

        

    
    '''
    BuildAndSolveNEFF builds and solves for effective index. (takes longer than BuildAndSolve)
    '''

    def BuildAndSolveNEFF(self):
        self.Variables = self.structure.Variables
        
        self.structure.buildStructure()
        self.structure.BuildModel_CW() 

        self.structure.RunMPB()

        print("NEFF: ", self.structure.neff)

        self.structure.sim.reset_meep()



    """
    PlotStructure is used to just build the structure given and plot, very useful when making a new device.
    """


    def PlotStructure(self):	
        self.Variables = self.structure.Variables
        self.structure.buildStructure()  
        self.structure.BuildModel_CW() 
        plt.show()


    """
    PlotMode is used to plot the mode profiles from file and save them.
    """

    def PlotMode(self):

        epsFile = self.Variables['workingDir'] + self.Variables['MPsimname'] + "-eps-000000.00.h5"
        eyFile      = self.Variables['workingDir'] + self.Variables['MPsimname'] + "-ey-000000.00.h5"

        epsf = np.flip( np.transpose( np.array( h5py.File(epsFile,'r')['eps'] ) ),0 )
        epsfmod = (epsf - 1.00)**15 # manipulating eps to create more contrast for plotting

        fields = np.flip( np.transpose( h5py.File(eyFile,'r')['ey.r']))

        midpoint = int(len(epsf[:,0])/2)
        ext = self.Variables['SimSize']/2

        vertical_eps    = np.sqrt(np.flip(epsf[:,midpoint]))
        vertical_field  = np.flip(fields[:,midpoint]/max(fields[:,midpoint]))

        horisontal_eps   = np.sqrt(epsf[midpoint,:])
        horisontal_field = fields[midpoint,:]/max(fields[midpoint,:])

        from mpl_toolkits.axes_grid1 import make_axes_locatable
        
        fig, main_ax = plt.subplots(figsize=(10, 10))
        divider = make_axes_locatable(main_ax)
        
        top_ax = divider.append_axes("top", 2.0, pad=0.5,sharex=main_ax)
        right_ax = divider.append_axes("right", 2.0, pad=0.5, sharey=main_ax)

        # make some labels invisible
        top_ax.xaxis.set_tick_params(labelbottom=False)
        right_ax.yaxis.set_tick_params(labelleft=False)

        #disable autoscale
        main_ax.autoscale(enable=True)
        right_ax.autoscale(enable=False)
        top_ax.autoscale(enable=False)

        #labelling
        main_ax.set_xlabel('xpos / um')
        main_ax.set_ylabel('ypos / um')
        top_ax.set_ylabel('Normalised Fields and N')
        right_ax.set_xlabel('Normalised Fields and N')

        #plotting 
        main_ax.imshow(fields,interpolation="none",extent=(-ext,ext,-ext,ext))

        
        top_ax.plot(np.linspace(-ext,ext,len(horisontal_field)),horisontal_field,label='ey')
        top_ax_twin = top_ax.twinx()
        top_ax_twin.plot(np.linspace(-ext,ext,len(horisontal_eps)),horisontal_eps,color='r',label="n")
        top_ax_twin.set_xlabel("n")

        right_ax.plot(vertical_field,np.linspace(-ext,ext,len(vertical_field)),label='ey')
        
        right_ax_twin = right_ax.twiny()
        right_ax_twin.plot(vertical_eps,np.linspace(-ext,ext,len(vertical_eps)),color='r',label="n")
        right_ax_twin.set_ylabel("n")

        top_ax.legend()
        right_ax.legend()
        
        plt.show()



    """
    saveMetaData saves all the variables to a json file
    """

    def saveMetaData(self):
        with open(self.Variables['workingDir'] + 'metadata.json', 'w') as file:
            json.dump(self.Variables, file)

    """
    Below are older conviluted functions that need simplified and implimented later.
    """

    
    def SimRanBefore(self):
        #check whether fields file exists, then loads the variables dictionary 
        #from file.
        WD = self.Variables['workingDir']
        
        if os.path.exists(WD + "fields.h5"):
            print("Path exists, trying to open previous vars")
            try:
                #try to reload variables
                with open(self.Variables['workingDir'] + "metadata.json") as json_file:
                    self.Variables = json.load(json_file)
            except:
                print("Failed to load old vars from .json")
                
            #overwrite these variables
            self.Variables["prevRun"] = True 
            self.Variables['workingDir'] = WD
            print("Variables loaded")
            


    
    
    def AutoRun(self):

        if self.Variables["prevRun"] == True:
            #If we're reloading variables then we must reload the FT detectors with data from 
            #last time
            print("")
            print("")
            print("")
            print("Reloading Sim")
            print("")
            print("")
            print("")
            
            self.sim.load(self.Variables['workingDir'])  # loads structure and fields
            for name,detector in self.detectors.items(): # loads detector data from files
                self.sim.load_flux(name,detector)
        else:
            print("")
            print("")
            print("Actual Run")
            print("")
            print("")

        
        if self.Variables['savefields'] == True:
            self.sim.run(
                mp.at_beginning(mp.output_epsilon),
                mp.at_every(200,mp.output_efield_z),
                until_after_sources=self.Variables['SimTime'] + self.Variables['nClad']* (self.Variables['sx']/2 + np.pi*self.Variables['capD']*self.Variables['roundTrips'])
                
                )
        else:
            if self.ModelType == "SidePolish":
                self.sim.run(	
                    mp.at_beginning(mp.output_epsilon),
                    until_after_sources=self.Variables['SimTime'] + self.Variables['nClad']* (self.Variables['sx'] + self.Variables['GAP']*self.Variables['roundTrips'])
                    
                    )
            elif self.ModelType == "LoadedCap":
                self.sim.run(	
                    mp.at_beginning(mp.output_epsilon),
                    until_after_sources=self.Variables['SimTime'] + self.Variables['nClad']* (self.Variables['sx']/2 + np.pi*self.Variables['capD']*self.Variables['roundTrips'])
                    
                    )

        print("SimTime = " + str(self.sim.round_time() ))

        
        """
        Dumping fields and fluxes
        """
        
        self.sim.dump(self.Variables['workingDir'])   # dumps fields and structure
         
        for name,detector in self.detectors.items():  # dump all the Fourier Transform detectors
            self.sim.save_flux(name,detector) 
            #self.sim.output_dft(detector, self.Variables['workingDir'] + name+"_dft")
            self.dumpWGMfields(detector,name)
            
        self.Variables['SimTime'] = self.sim.round_time()
        
        
        """
        Dumping fields and fluxes
        """


        flux_freqs = mp.get_flux_freqs(self.detectors['Transmission'])
        tran_flux = mp.get_fluxes(self.detectors['Transmission'])

        Data = {}
        Data['flux_freqs'] = flux_freqs
        Data['tran_flux'] = tran_flux

        if self.Variables["normal"] == True:
            Data['norm_tran'] = self.norm_tran

        with open(self.Variables['workingDir'] + "Data.pkl", 'wb') as file:
            pickle.dump(Data,file)

        self.Variables['CPUS'] = str(self.sim.num_chunks)

        with open(self.Variables['workingDir'] + 'metadata.json', 'w') as file:
            json.dump(self.Variables, file)


        wl = []
        Ts = []
        for i in range(self.Variables['nfreq']):
            wl = np.append(wl, 1/flux_freqs[i])
            
            if self.Variables["normal"] == True:
                Ts = np.append(Ts,tran_flux[i]/self.norm_tran[i])
            elif self.Variables["normal"] == False:
                Ts = np.append(Ts,tran_flux[i])

        plt.figure(dpi=1000)
        plt.plot(wl,Ts,label='transmittance')
        plt.xlabel("wavelength (um)")
        plt.savefig(self.Variables['workingDir']+"TransRef_" + str(int(self.Variables['SimTime'])) + ".pdf")


    def dumpWGMfields(self,detector,name):        
        
        
        # initialize wl vs y-pos matrix.
        matrix = np.zeros([len(self.sim.get_dft_array(detector,mp.Ez,0)),self.Variables['nfreq']],dtype=np.complex128)

        for i in range(0,self.Variables['nfreq']):
            matrix[:,i] = self.sim.get_dft_array(detector,mp.Ez,i)
        
        data = {}
        #Wavelength vs position vs Ez
        data['matrix'] = np.fliplr(np.flipud(matrix))
        
        #wavelengths measured over
        data['WL'] = 1/np.flip(detector.args[0])

        #positional data
        cen = self.structure.detectors[name].center
        size = self.structure.detectors[name].size
        data['Location'] = self.sim.get_array_metadata(center=cen, size=size)
        
        #refractiveindex underneath monitor
        data['RefractiveIndex'] = np.sqrt(self.sim.get_array(component=mp.Dielectric,center=cen,size=size))
        
        #dump data to file
        with open(self.Variables['workingDir'] + name +"_dft.pkl", 'wb') as file:
            pickle.dump(data,file)
        

