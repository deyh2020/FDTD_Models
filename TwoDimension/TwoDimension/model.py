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

    def SidePolish(self):
        #init constants
        self.structure = SidePolish.structure()
        
    def RunTRspectrum(self):

        #Sort out if there's been a previous run and make directories.
        self.Variables = self.structure.Variables
        self.mkALLDIRS()
        self.SimRanBefore()
        
                
        #normalisation run
        self.normRun()

        #Actual run
        self.structure.buildStructure()  
        self.structure.sources()
        self.structure.fluxDetectors()
        self.Buildsim(NormRun=False,Plot=True) 

        self.AutoRun()
        self.sim.print_times()

    def PlotStructure(self):	
        self.Variables = self.structure.Variables
        self.structure.buildStructure()  
        self.structure.sources()
        self.structure.fluxDetectors()
        self.Buildsim(NormRun=False,Plot=True) 
        plt.show()

    
    def SimRanBefore(self):
        #check whether fields file exists.
        WD = self.Variables["workingDir"]
        print("")
        print("")
        print(WD + "fields.h5")
        print("")
        print("")
        
        if os.path.exists(WD + "fields.h5"):
            print("Path exists, trying to open previous vars")
            try:
                #try to reload variables
                with open(self.Variables['workingDir'] + "metadata.json") as json_file:
                    self.Variables = json.load(json_file)
            except:
                print("Failed to load old vars from .json")
            self.Variables["prevRun"] = True 
            self.Variables["workingDir"] = WD
            print("Variables loaded")
            
    def mkALLDIRS(self):
        self.Variables["workingDir"] = '../data/'+self.Variables["today"]+'/'+self.Variables['filename']+'/'
        try:
            os.makedirs(self.Variables["workingDir"])
        except:
            print('AlreadyDir')
    
            
        
        


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

        # transmitted flux
        self.tranE = self.sim.add_flux(self.Variables['fcen'], self.Variables['df'], self.Variables['nfreq'], self.structure.detector)


        fig,ax = plt.subplots(dpi=150)
        if NormRun:
            self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
            plt.savefig(self.Variables["workingDir"]+"NormModel_" + str(self.Variables["dataFile"]) +".pdf")
        else:
            self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
            plt.savefig(self.Variables["workingDir"]+"Model_" + str(self.Variables["dataFile"]) +".pdf")
        


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
                until_after_sources=self.Variables['sx']*self.Variables['nClad']
                )

            self.norm_tran = mp.get_fluxes(self.tranE)

            #Reset sources
            self.sim.reset_meep()


        elif self.Variables["prevRun"] == True:
            #load pickless
            with open(self.Variables["workingDir"] + self.Variables['dataFile'] + ".pkl","rb") as file:
                data = pickle.load(file)
            self.norm_tran = data['norm_tran']
            print("Loaded up pickles")
        else:
            "not normaling anyways rip"


    
    def AutoRun(self):

        if self.Variables["prevRun"] == True:
            print("")
            print("")
            print("")
            print("Reloading Sim")
            print("")
            print("")
            print("")
            self.sim.load(self.Variables['workingDir'])
            self.sim.load_flux("Transmission",self.tranE)
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
            self.sim.run(	
                mp.at_beginning(mp.output_epsilon),
                until_after_sources=self.Variables['SimTime'] + self.Variables['nClad']* (self.Variables['sx']/2 + np.pi*self.Variables['capD']*self.Variables['roundTrips'])
                
                )

        print("SimTime = " + str(self.sim.round_time() ))

        
        """
        Dumping fields and fluxes
        """
        self.sim.dump(self.Variables['workingDir'])
        self.sim.save_flux("Transmission",self.tranE)
        self.Variables['SimTime'] = self.sim.round_time()


        flux_freqs = mp.get_flux_freqs(self.tranE)
        tran_flux = mp.get_fluxes(self.tranE)

        Data = {}
        Data['flux_freqs'] = flux_freqs
        Data['tran_flux'] = tran_flux

        if self.Variables["normal"] == True:
            Data['norm_tran'] = self.norm_tran

        with open(self.Variables['workingDir'] + self.Variables['dataFile'] + ".pkl", 'wb') as file:
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
        plt.xlabel("wavelength (μm)")
        plt.savefig(self.Variables['workingDir']+"TransRef_" + str(int(self.Variables['SimTime'])) + ".pdf")

    def PDMSindex(self):

        self.PDMStemp = np.array([27.04200613, 30.04708872, 40.09978324, 50.0485836, 60.10202556, 70.05194708, 80.00074744])
        self.nPDMS    = np.array([1.410413147,1.409271947,1.405629718,1.4019877,1.398453453,1.394973372,1.391331424])
        self.PDMSfit = np.polyfit(self.PDMStemp,self.nPDMS,deg=1)




    def Silicaindex(self):

        self.Silicatemp = np.array([22.83686643,40.36719542,70.32692845,103.3346833])
        self.nSilica    = np.array([1.445300107,1.44555516,1.445847903,1.445958546])
        self.SilicaFIT = np.polyfit(self.Silicatemp,self.nSilica,deg=1)
