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
			"nClad":1.3,
			"nPDMS":1.410,
			#Device Dimentions
			"R1":4.1,
            "R2":62.5,
            "CladLeft":1.0,
			##Resonator Dimentions
            'angle':90,#121.4,
            'CladLeft':0 ,
            'Depth':40,
            'Width':100,
            'GAP':50,
            
            'BubblesNum':2 ,
            'BubblesType':'sqr',
            'FibreType':'polished',
			#Simulation area Properties
			'PAD':200,
			"res":10.000/1.0,    # would usually be 10px per wl but our smallest waveguide is 1um thick
			"dpml":1.55,
			#Simulation source Properties
			"StartWL":1.520,
			"EndWL":1.580,
			"WLres":0.1/1000, #res in um so 100pm
			"Courant":1.000/np.sqrt(2.000),
			#Simulation Properties
			"today":str(date.today()),
			"WallT":0,
			"workingDir":'',
			"filename":'test',
			"dataFile":'test',
			"roundTrips":1.00,    #relates to how long the sim will run relative to orbits of the WGM
			#Flags
			"normal":True,
			"savefields":False
		}

        #self.PDMSindex()
        #self.Silicaindex()
        

        #make objects


    def buildNorm(self):
        #Build a structure that represents a system without the device, i.e here i've just built a waveguide 
        #without a WGM.
        self.Objlist = []
        
        self.Variables["sx"] = self.Variables['GAP']+self.Variables['Width']+2*self.Variables['PAD']+2*self.Variables['dpml']
        self.Variables["sy"] = 2.3*self.Variables['R2'] + 2*self.Variables['dpml']
		
        self.cell_size = mp.Vector3(self.Variables["sx"],self.Variables["sy"],0)

        self.pml_layers = [mp.PML(thickness=self.Variables["dpml"])]

        self.Coating = mp.Block(
            center=mp.Vector3(0,0,0),
            size=mp.Vector3(mp.inf,mp.inf,mp.inf),
            material=mp.Medium(index=self.Variables['nAir'])
            )


        self.Clad = mp.Block(
            center=mp.Vector3(x=0,y=0,z=0),
            size=mp.Vector3(x=mp.inf,y=2*self.Variables['R2'],z=mp.inf),
            material=mp.Medium(index=self.Variables['nClad'])
            )

        self.Core = mp.Block(
            center=mp.Vector3(0,0,0),
            size=mp.Vector3(mp.inf,2*self.Variables['R1'],mp.inf),
            material=mp.Medium(index=self.Variables['nCore'])
            )

        self.Objlist.extend([self.Coating,self.Clad,self.Core])


    def buildStructure(self):
        #Build a structure that represents a system without the device, i.e here i've just built a waveguide 
        #without a WGM.
        self.Objlist = []
        
        self.Variables["sx"] = self.Variables['GAP']+self.Variables['Width']+2*self.Variables['PAD']+2*self.Variables['dpml']
        self.Variables["sy"] = 2.3*self.Variables['R2'] + 2*self.Variables['dpml']
		
        self.cell_size = mp.Vector3(self.Variables["sx"],self.Variables["sy"],0)

        self.pml_layers = [mp.PML(thickness=self.Variables["dpml"])]

        self.Coating = mp.Block(
            center=mp.Vector3(0,0,0),
            size=mp.Vector3(mp.inf,mp.inf,mp.inf),
            material=mp.Medium(index=self.Variables['nAir'])
            )


        self.Clad = mp.Block(
            center=mp.Vector3(x=0,y=(-self.Variables['R2']/2 + self.Variables['CladLeft']/2 + self.Variables['R1']/2)),
            size=mp.Vector3(x=mp.inf,y= self.Variables['R2'] + self.Variables['R1'] + self.Variables['CladLeft']   ,z=mp.inf),
            material=mp.Medium(index=self.Variables['nClad'])
            )

        self.Core = mp.Block(
            center=mp.Vector3(0,0,0),
            size=mp.Vector3(mp.inf,2*self.Variables['R1'],mp.inf),
            material=mp.Medium(index=self.Variables['nCore'])
            )


        TL    = self.Variables['Width']
        D     = self.Variables['Depth']
        angle = self.Variables['angle']

        BL    = TL - 2*(D/np.tan((180-angle)*(np.pi/180)))
                
        verts = [
                
                mp.Vector3(x=-TL/2,		y=D 	,z=0),
                mp.Vector3(x=TL/2 ,		y=D 	,z=0),
                mp.Vector3(x=BL/2 ,		y=0 	,z=0),
                mp.Vector3(x=-BL/2,		y=0 	,z=0)
            
                ]


        self.LH = mp.Prism(center=mp.Vector3(x=-self.Variables['GAP']/2 - TL/2,y=-D/2+self.Variables['R1']+self.Variables['CladLeft'],z=0),
                            vertices = verts,
                            material=mp.Medium(index=self.Variables['nAir']),
                            height=1
                            )

        self.RH = mp.Prism(center=mp.Vector3(x=self.Variables['GAP']/2 + TL/2,y=-D/2+self.Variables['R1']+self.Variables['CladLeft'],z=0),
                            vertices = verts,
                            material=mp.Medium(index=self.Variables['nAir']),
                            height=1
                            )

        self.Objlist.extend([self.Coating,self.Clad,self.Core,self.LH,self.RH])


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
                center=mp.Vector3(x=-(self.Variables['sx']/2)+2*self.Variables['dpml'],y=0),
                size=mp.Vector3(y=40),
                direction=mp.X,
                eig_kpoint=kpoint,
                eig_band=1,
                eig_parity=mp.EVEN_Y,
                eig_match_freq=True
                )
            ]

    def fluxDetectors(self):
        self.detector = mp.FluxRegion(center=mp.Vector3((self.Variables['sx']/2) - 2*self.Variables['dpml'] ,0,0), 
                size=mp.Vector3(0,12,0))
            
            
        