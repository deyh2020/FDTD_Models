import meep as mp
import numpy as np
from datetime import date


class structure:
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
			"nPerovskite":2.5,
			#Device Dimentions
			"taperD":1.000,
			"capD":63,          #updated from microscope measurements
			"WallThick":9.000,  #updated from microscope measurements
			"GAP":0.667,        #from previous simulation experiments, probably needs optimised.
			#Simulation area Properties
			"PAD":2.000,
			"res":10.000/1.0,    # would usually be 10px per wl but our smallest waveguide is 1um thick
			"dpml":1.55,
			#Simulation source Properties
			"StartWL":1.520,
			"EndWL":1.580,
			"WLres":0.001/1000, #res in um so picometer resolution
			"Courant":1.000/np.sqrt(2.000),
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

        

        #make objects


    def buildNorm(self):
        #Build a structure that represents a system without the device, i.e here i've just built a waveguide 
        #without a WGM.
        self.Objlist = []
        
        self.Variables["sx"] = self.Variables['capD']+2*self.Variables['PAD']+2*self.Variables['dpml']
        self.Variables["sy"] = self.Variables['PAD']+2*self.Variables['dpml']+self.Variables['taperD']+self.Variables['GAP']+5

		
        self.cell_size = mp.Vector3(self.Variables["sx"],self.Variables["sy"],0)

        self.pml_layers = [mp.PML(thickness=self.Variables["dpml"])]

        self.taperYpos = 0

        Taper = mp.Block(
            center=mp.Vector3(0,0,0),
            size=mp.Vector3(mp.inf,self.Variables["taperD"],mp.inf),
            material=mp.Medium(index=self.Variables['nClad'])
            )

        self.Objlist.extend([Taper])


    def buildStructure(self):
        #Build the whole device, I've set it up so the objects are added to a list, note the order in the list
        #corrisponds to the layer they're inserted, this equates to the last item in the list being ontop.
        self.Objlist = []

        self.Variables["sx"] = self.Variables['capD']+2*self.Variables['PAD']+2*self.Variables['dpml']
        self.Variables["sy"] = self.Variables['capD']+2*self.Variables['PAD']+2*self.Variables['dpml']+self.Variables['taperD']+self.Variables['GAP']+5


        self.cell_size = mp.Vector3(self.Variables["sx"],self.Variables["sy"],0)

        self.pml_layers = [mp.PML(thickness=self.Variables["dpml"])]


        OD = mp.Cylinder(
            radius=self.Variables["capD"]/2,
            height=mp.inf,
            axis=mp.Vector3(0,0,1),
            material=mp.Medium(index=self.Variables['nClad'])
            )

        ID = mp.Cylinder(
            radius=(self.Variables["capD"] - (self.Variables['WallThick']*2))/2,
            height=mp.inf,
            axis=mp.Vector3(0,0,1),
            material=mp.Medium(index=self.Variables['nPerovskite'])
            )

        self.taperYpos = -(self.Variables["capD"]/2.0 + self.Variables["GAP"] + self.Variables["taperD"]/2)

        Taper = mp.Block(
            center=mp.Vector3(0,self.taperYpos,0),
            size=mp.Vector3(mp.inf,self.Variables["taperD"],mp.inf),
            material=mp.Medium(index=self.Variables['nClad'])
            )

        self.Objlist.extend([OD,ID,Taper])

    def sources(self):
        #calculate fcen df and nfreq add sources to a list
        self.Variables['fcen'] = 1.0/((self.Variables['EndWL'] + self.Variables['StartWL'])/2.0)
        self.Variables['df']   = ((1/self.Variables['StartWL']) - (1/self.Variables['EndWL']))
        self.Variables['nfreq']= int((self.Variables['EndWL']-self.Variables['StartWL'])/self.Variables['WLres'])

        kx = 0.4
        kpoint = mp.Vector3(kx)

        self.src = [
                mp.EigenModeSource(src=mp.GaussianSource(
                    self.Variables['fcen'],
                    fwidth=self.Variables['df']
                    ),
                center=mp.Vector3(x=-(self.Variables['sx']/2)+2*self.Variables['dpml'],y=self.taperYpos),
                size=mp.Vector3(y=5),
                direction=mp.X,
                eig_kpoint=kpoint,
                eig_band=1,
                eig_parity=mp.EVEN_Y,
                eig_match_freq=True
                )
            ]

    def fluxDetectors(self):
        self.detector = mp.FluxRegion(center=mp.Vector3((self.Variables['sx']/2) - 2*self.Variables['dpml'] ,self.taperYpos,0), size=mp.Vector3(0,5,0))
            
            
        