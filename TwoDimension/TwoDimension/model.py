import meep as mp
import numpy as np
import pickle,json, os
import time
import matplotlib.pyplot as plt

import LoadedCapillaries.structure as LoadedCaps
import SidePolishedFibre.structure as SidePolish


class Model:

    def LoadedCap(self):
        #init constants
        self.structure = LoadedCaps.structure()
        self.ModelType = "LoadedCap"

    def SidePolish(self):
        #init constants
        self.structure = SidePolish.structure()
        self.ModelType = "SidePolish"
        
    def RunTRspectrum(self):

        #Sort out if there's been a previous run and make directories.
        self.Variables = self.structure.Variables
        self.SimRanBefore()
         
        #normalisation run
        self.normRun()

        #Actual run
        print("Polished Variable")
        print(self.Variables['Polished'])

        if self.Variables['Polished'] == False:
            self.structure.buildUnpolishedStructure()
        else:
            self.structure.buildStructure()  

        self.structure.sources()
        self.structure.fluxDetectors()
        self.Buildsim(NormRun=False,Plot=True) 

        self.AutoRun()
        self.sim.print_times()

    def PlotStructure(self):	
        self.Variables = self.structure.Variables
        if self.Variables['Polished'] == False:
            self.structure.buildUnpolishedStructure()
        else:
            self.structure.buildStructure()  
        self.structure.sources()
        self.structure.fluxDetectors()
        self.Buildsim(NormRun=False,Plot=True) 
        plt.show()

    
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
            


    def Buildsim(self,Plot=False,NormRun=False):   # builds sim and plots structure to file 

        self.sim = mp.Simulation(
            cell_size=self.structure.cell_size,
            geometry=self.structure.Objlist,
            sources=self.structure.src,
            resolution=self.Variables['res'],
            force_complex_fields=False,
            eps_averaging=True,
            boundary_layers=self.structure.pml_layers,
            progress_interval=30,
            Courant=self.Variables['Courant']

            )
        self.sim.use_output_directory(self.Variables["workingDir"])

        # add flux detectors
        self.detectors = {}
        if NormRun:
            self.detectors['Transmission'] = self.sim.add_flux(self.Variables['fcen'], self.Variables['df'], self.Variables['nfreq'],self.structure.detectors['Transmission'])
        else:
            for name,detector in self.structure.detectors.items():
                self.detectors[name] = self.sim.add_flux(self.Variables['fcen'], self.Variables['df'], self.Variables['nfreq'], detector)


        fig,ax = plt.subplots(dpi=150)
        if NormRun:
            self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'})
            plt.savefig(self.Variables["workingDir"]+"NormalModel.pdf")
        else:
            self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'})
            plt.savefig(self.Variables["workingDir"]+"Model.pdf")
        


    def normRun(self):
        #If there hasn't been a previous run and the user want to normalise data, build and run norm.
        if self.Variables["normal"] == True and self.Variables["prevRun"] == False:
            self.structure.buildNorm()  
            self.structure.sources()
            self.structure.fluxDetectors()
            self.Buildsim(NormRun=True,Plot=True) 

            #Run normal model
            print("")
            print("")
            print("Normalisation Run")
            print("")
            print("")


            self.sim.run(
                until_after_sources=self.Variables['sx']*self.Variables['nCore']
                )

            self.norm_tran = mp.get_fluxes(self.detectors['Transmission'])

            #Reset sources
            self.sim.reset_meep()


        elif self.Variables["prevRun"] == True:
            #if there has been a previous sim, then load the norm data
            with open(self.Variables["workingDir"] + "Data.pkl","rb") as file:
                data = pickle.load(file)
            self.norm_tran = data['norm_tran']
            print("Loaded up pickles")
        else:
            "not normaling anyways rip"


    
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
        

