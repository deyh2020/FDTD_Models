import meep as mp
import numpy as np
from datetime import date


class structure:


    '''
    initialise structure class with a variable dictionary:
    '''

    def __init__(self):
        self.Variables = {
			#programming vars 
			"debug":False,
			"prevRun":False,
            "SimTime":0.0,
			
            #refractive indexes
			"nAir": 1.000,
			"nCore":1.445,
			"nClad":1.440,
			"nCoating":1.410, #PDMS
			
            #Device Dimentions
			"R1":4.1,
            "R2":62.5,
            "CladLeft":1.0,
            "Polished":True,
			
            #Simulation area Properties
			'PAD':1000,
			"res":10.000/1.0,    # would usually be 10px per wl but our smallest waveguide is 1um thick
			"dpml":1.55,
			
            #Simulation source Properties
			"wl":1.550,
            "modeOrder":1,
			"Courant":1.000,
			
            #Simulation Properties
			"today":str(date.today()),
			"WallT":0,
			"workingDir":'../data/',
			"roundTrips":1.00,    #relates to how long the sim will run relative to orbits of the WGM
			"SaveFieldsatEnd":True,
            
            #Flags
			"normal":True,
			"savefields":False
		}

        #self.PDMSindex()
        #self.Silicaindex()

        
        

        #make objects


    def buildFibre(self):
        
        self.Objlist = []

        if self.Variables['FibreType']   == "Standard":
            self.buildUnpolishedFibre()
        elif self.Variables['FibreType'] == "Polished":
            self.buildPolishedFibre()
        else:
            print("Fibre Type not selected")



    '''
    buildUnpolishedFibre is used to add an unpolished fibre structure to the Objlist global list.
    '''
    
    def buildUnpolishedFibre(self):

        self.SrcSize = self.Variables['SimSize'] - 2*self.Variables['PMLThick']
        self.cell_size = mp.Vector3(self.Variables['SimSize'], self.Variables['SimSize'], 0)

        self.pml_layers = [
            mp.PML(thickness=self.Variables['PMLThick'], direction=mp.X),
            mp.PML(thickness=self.Variables['PMLThick'], direction=mp.Y)
            ]

        Core = mp.Cylinder(
            radius=self.Variables['R1'],
            height=mp.inf,
            axis=mp.Vector3(0,0,1),
            material=mp.Medium(index=self.Variables['nCore'])
            )

        Clad = mp.Cylinder(
            radius=self.Variables['R2'],
            height=mp.inf,
            axis=mp.Vector3(0,0,1),
            material=mp.Medium(index=self.Variables['nClad'])
            )

        self.Objlist.extend([Clad,Core])

    '''
    buildPolishedFibre is used to add an polished fibre structure to the Objlist global list.
    '''

    def buildPolishedFibre(self,WPDMS=False):

        self.SrcSize = self.Variables['SimSize'] - 2*self.Variables['PMLThick']
        self.cell_size = mp.Vector3(self.Variables['SimSize'], self.Variables['SimSize'], 0)

        self.pml_layers = [
            mp.PML(thickness=self.Variables['PMLThick'], direction=mp.X),
            mp.PML(thickness=self.Variables['PMLThick'], direction=mp.Y)
            ]

        PolishedZone = mp.Block(
            center=mp.Vector3(y=self.Variables['R2']/2+self.Variables['R1']+self.Variables['Pad']),
            size=mp.Vector3(250,62.5,mp.inf), 
            material=mp.Medium(index=self.Variables['nCoating']))


        Core = mp.Cylinder(
            radius=self.Variables['R1'],
            height=mp.inf,
            axis=mp.Vector3(0,0,1),
            material=mp.Medium(index=self.Variables['nCore'])
            )

        Clad = mp.Cylinder(
            radius=self.Variables['R2'],
            height=mp.inf,
            axis=mp.Vector3(0,0,1),
            material=mp.Medium(index=self.Variables['nClad'])
            )

        self.Objlist.extend([Clad,Core,PolishedZone])

    
    '''
    BuildModel_CW is used to build the MEEP simulation object with a source.
    '''

    def BuildModel_CW(self, Plot=False, axes=None):   # builds sim and plots structure to file

        self.fcen = 1/self.Variables['wl']
        self.df = 0.1*self.fcen
        self.kpoint = mp.Vector3(x=0, y=0, z=self.fcen*self.Variables['nCore'])

        self.src = [
                mp.EigenModeSource(
                    src=mp.ContinuousSource(
                        self.fcen
                    ),
                    center=mp.Vector3(0, 0, 0),
                    size=mp.Vector3(self.SrcSize, self.SrcSize, 0),
                    direction=mp.Z,
                    eig_kpoint=self.kpoint,
                    eig_band=self.Variables['modeOrder'],
                    eig_parity=mp.ODD_Y,
                    eig_match_freq=True,
                    eig_resolution=1
                )
            ]

        self.sim = mp.Simulation(
                cell_size=self.cell_size,
                geometry=self.Objlist,
                sources=self.src,
                resolution=self.Variables['res'],
                symmetries=[mp.Mirror(mp.X)],
                force_complex_fields=True,
                eps_averaging=True,
                boundary_layers=self.pml_layers,
                k_point=self.kpoint,
                ensure_periodicity=False
            )

        
        
        if Plot:
            if axes == None:
                    ax = plt.axes()
            else:
                ax = axes,
            self.sim.plot2D(
                ax=ax,
                #output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
                #fields=mp.Ez,
                plot_sources_flag=False,
                plot_monitors_flag=False,
                plot_eps_flag=True,
                eps_parameters={'alpha': 0.8, 'interpolation': 'none'}
            )
            plt.savefig(self.workingDir+"EPS_" + str(self.Datafile) + ".pdf")


    """
    RunMPB solves for k, group velocity and neff. 
    """

    def RunMPB(self):

        self.sim.init_sim()

        self.EigenmodeData = self.sim.get_eigenmode(
                self.fcen,
                mp.Z,
                        mp.Volume(center=mp.Vector3(), size=mp.Vector3(
                            self.SrcSize, self.SrcSize, 0)),
                band_num=1,
                kpoint=self.kpoint,
                match_frequency=True,
                resolution=self.res
            )

        self.k = self.EigenmodeData.k
        self.vg = self.EigenmodeData.group_velocity
        self.neff = self.k.norm() * self.wl

            
    def PDMSindex(self):

        self.PDMStemp = np.array([27.04200613, 30.04708872, 40.09978324, 50.0485836, 60.10202556, 70.05194708, 80.00074744])
        self.nPDMS    = np.array([1.410413147,1.409271947,1.405629718,1.4019877,1.398453453,1.394973372,1.391331424])
        self.PDMSfit = np.polyfit(self.PDMStemp,self.nPDMS,deg=1)




    def Silicaindex(self):

        self.Silicatemp = np.array([22.83686643,40.36719542,70.32692845,103.3346833])
        self.nSilica    = np.array([1.445300107,1.44555516,1.445847903,1.445958546])
        self.SilicaFIT = np.polyfit(self.Silicatemp,self.nSilica,deg=1)
            
        
