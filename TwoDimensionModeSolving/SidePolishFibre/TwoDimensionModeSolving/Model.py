import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt,os
from datetime import date
import pickle,json, os
import time



class Model:

	def __init__(self):

		#init constants
		self.TicToc = self.TicTocGenerator() # create an instance of the TicTocGen generator

		##Material N
		self.nCoating  = 1.41
		self.coreN     = 1.445
		self.cladN     = 1.440

		##Fibre Dimentions
		self.R1     = 4.1
		self.R2     = 62.5
		self.CladLeft = 1

		##Resonator Dimentions
		self.angle = 121.4
		self.CladLeft = 0 
		self.Depth  = 40
		self.Width  = 100
		self.EllipseOffset = 0
		self.GAP    = 0
		self.Pad    = 50
		self.BubblesNum = 2 
		self.BubblesType = 'sqr'
		self.FibreType = 'polished'

		##Src properties
		self.fcen   = 1/1.55
		self.df     = 0.8e-2
		self.nfreq  = 1000

		##MEEP properties
		self.dpml   = 10
		self.res    = 10
		self.DecayF = 1e-2
		self.WallT  = 0
		self.SimT   = 1e6
		self.today  = str(date.today())
		self.workingDir= ''
		self.filename = 'test'
		self.Datafile = 'test'
		self.sim    = None
		self.Objlist = []
		self.Notes   = ''
		self.NormComplete = False
		self.SingleNorm = False
		self.Courant = 0.5


		#init Data arrays
		self.srcE  = np.array([])
		self.tranE = np.array([])

		self.PDMSindex()
		self.Silicaindex()


	def PlotStructure(self):	

		self.Objlist = []	
		self.buildPolished()  						#builds base polished fibre structure list
		self.ADDtrapazoidBubbles()
		self.BuildModel(NormRun=False,Plot=True) 
		plt.show()

		

	def mkALLDIRS(self):
		
		self.workingDir = '../data/'+self.today+'/'+self.filename+'/'

		print('WD:',self.workingDir)

		try:
			os.makedirs(self.workingDir)
		except:
			print('AlreadyDir')

		self.sim.use_output_directory(self.workingDir)


	def buildPolished(self):

		self.sx = self.GAP + 2*self.Width + 2*self.dpml + self.Pad
		self.sy = 150 + 2*self.dpml

		
		self.cell_size = mp.Vector3(self.sx,self.sy,0)

		self.pml_layers = [mp.PML(thickness=self.dpml)]

		self.Coating = mp.Block(
			center=mp.Vector3(0,0,0),
			size=mp.Vector3(mp.inf,mp.inf,mp.inf),
			material=mp.Medium(index=self.nCoating)
			)

		self.Clad = mp.Block(
			center=mp.Vector3(x=0,  y=(-self.R2/2 + self.CladLeft/2 + self.R1/2)  ,z=0),
			size=mp.Vector3(x=mp.inf,  y= self.R2 + self.R1 + self.CladLeft   ,z=mp.inf),
			material=mp.Medium(index=self.cladN)
			)

		self.Core = mp.Block(
			center=mp.Vector3(0,0,0),
			size=mp.Vector3(mp.inf,2*self.R1,mp.inf),
			material=mp.Medium(index=self.coreN)
			)

		self.Objlist.extend([self.Coating,self.Clad,self.Core])



	def ADDtrapazoidBubbles(self):

		Center = 0
		TL    = self.Width
		D     = self.Depth
		angle = self.angle
		
		BL    = TL - 2*(D/np.tan((180-angle)*(np.pi/180)))
				
		verts = [
	            
				mp.Vector3(x=-TL/2,		y=D 	,z=0),
	            mp.Vector3(x=TL/2 ,		y=D 	,z=0),
	            mp.Vector3(x=BL/2 ,		y=0 	,z=0),
	            mp.Vector3(x=-BL/2,		y=0 	,z=0)
	        
	            ]


		self.LH = mp.Prism(center=mp.Vector3(x=-self.GAP/2 + Center,y=-D/2+self.R1+self.CladLeft,z=0),
	                     vertices = verts,
	                     material=mp.Medium(index=self.nCoating),
	                     height=1
	                     )

		self.RH = mp.Prism(center=mp.Vector3(x=self.GAP/2 + Center,y=-D/2+self.R1+self.CladLeft,z=0),
	                     vertices = verts,
	                     material=mp.Medium(index=self.nCoating),
	                     height=1
	                     )

		self.Objlist.extend([self.LH,self.RH])


	def BuildModel(self,Plot=False,NormRun=False):   # builds sim and plots structure to file 
		
		self.fcen   = 1/1.5071358
		self.df     = 0.1*self.fcen
		self.kpoint = mp.Vector3(x=0,y=0,z=self.fcen*self.coreN)
		
		self.src = [
				mp.EigenModeSource(
					src=mp.ContinuousSource(
						self.fcen
						),
				    center=mp.Vector3(x=-(self.sx/2)+2*self.dpml,y=0),
				    size=mp.Vector3(y=40),
				    direction=mp.X,
				    eig_kpoint=self.kpoint,
				    eig_band=1,
				    eig_parity=mp.EVEN_Y,
				    eig_match_freq=True,
					eig_resolution=1
				)
			]

		
		self.sim = mp.Simulation(
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			force_complex_fields=True,
			eps_averaging=False,
			boundary_layers=self.pml_layers,
			#progress_interval=30,
			#Courant=self.Courant,
			ensure_periodicity=False
			#geometry_center=mp.Vector3(x=0,y=-25,z=0)
			#k_point=mp.Vector3(mp.X)
			)


		self.mkALLDIRS()

		fig,ax = plt.subplots(dpi=150)
		if NormRun:
			self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
			plt.savefig(self.workingDir+"NormModel_" + str(self.Datafile) +".pdf")
		else:
			self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
			plt.savefig(self.workingDir+"Model_" + str(self.Datafile) +".pdf")


	def Run(self):
		
		print("")
		print("")
		print("Running")
		print("")
		print("")

		self.buildPolished()
		self.ADDtrapazoidBubbles()
		self.BuildModel()

		#self.myRunFunction(self.monitorPts)
		#self.sim.solve_cw(L=2)
		self.sim.run(
			mp.at_beginning(mp.output_epsilon),
			mp.at_every(1000,mp.output_efield_z),
			until=10*self.sx*self.coreN
			)
		mp.output_efield_z(self.sim)
	


	def TimestepFields(self):
		
		fig,axes = plt.subplots(1, 1,dpi=200)

		self.sim.run(
			until=self.SimT
			)
		
		#self.sim.plot2D(fields=mp.Ez,plot_sources_flag=True,plot_monitors_flag=True)
		self.sim.plot2D(
			ax = axes,
			#output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
			fields=mp.Ez,
			plot_sources_flag=True,
			plot_monitors_flag=True,
			plot_eps_flag=True,
			eps_parameters={'alpha':0.8, 'interpolation':'none','cmap':'binary','contour':True}
			)
		plt.show()


	def SaveMeta(self):
		
		metadata = {
		"Runtime":self.Runtime,
		"Chunks":self.sim.num_chunks,
		##Material N
		"nCoating": self.nCoating,
		"CoreN":self.coreN,
		"CladN":self.cladN,
		##Fibre Dimentions
		"R1":self.R1,
		"R2":self.R2,
		"CladLeft":self.CladLeft,
		##Resonator Dimentions
		"Depth":self.Depth,
		"Width":self.Width,
		"GAP":self.GAP,
		"Rw":self.Rw,
		##Src properties
		"fcen":self.fcen,
		"df":self.df, 
		"nfreq":self.nfreq,

		##MEEP properties
		"dpml":self.dpml,
		"resolution":self.res,
		"DecayF":self.DecayF,
		"WallT":self.WallT,
		"SimT":self.SimT,
		"today":self.today,
		"WorkingDir":self.workingDir,
		"filename":self.filename,
		"notes":self.Notes,

		"sx":self.sx,
		"sy":self.sy
        }

		
		with open(self.workingDir + str(self.sim.num_chunks) + '_metadata.json', 'w') as file:
			json.dump(metadata, file)




	def dumpData2File(self):
    
		# initialise main data dictionary
		Data = {}
		
		
		Data['Src']['lambda'] = 1/np.array(mp.get_flux_freqs(self.srcE))
		Data['Src']['flux'] = np.array(mp.get_fluxes(self.srcE))
		
		Data['Out']['lambda'] = 1/np.array(mp.get_flux_freqs(self.tranE))
		Data['Out']['flux'] = np.array(mp.get_fluxes(self.tranE))
		

		metadata = {
			"date": str(self.today),
			"Data": self.workingDir+"Data.pk1"
		}

		metadata = {**metadata,**self.meta}
		
		Data = {}
		Data['Src'] = {}       # sensor just after source.
		Data['Out'] = {}       # sensor at the end of the WG (for transmission)

		with open(metadata['Data'], 'wb') as file:
			pickle.dump(Data,file)


		with open(self.workingDir + 'metadata.json', 'w') as file:
			json.dump(metadata, file)


	def pltModel(self,Plt):
		plt.figure(dpi=200)
		self.sim.plot2D(eps_parameters={'alpha':0.8, 'interpolation':'none'})
		if Plt:
			plt.show()
		plt.savefig(self.workingDir+"Model.pdf")


	def TicTocGenerator(self):
		# Generator that returns time differences
		ti = 0           # initial time
		tf = time.time() # final time
		while True:
			ti = tf
			tf = time.time()
			yield tf-ti # returns the time difference


	# This will be the main function through which we define both tic() and toc()
	def toc(self,tempBool=True):
		# Prints the time difference yielded by generator instance TicToc
		self.Runtime = next(self.TicToc)
		print("Whole Sim Walltime: "+ str(self.Runtime) + " s")
		 

	def tic(self):
		self.Runtime = 0
		# Records a time in TicToc, marks the beginning of a time interval
		self.toc(False)

	def PDMSindex(self):

		self.PDMStemp = np.array([27.04200613, 30.04708872, 40.09978324, 50.0485836, 60.10202556, 70.05194708, 80.00074744])
		self.nPDMS    = np.array([1.410413147,1.409271947,1.405629718,1.4019877,1.398453453,1.394973372,1.391331424])
		self.PDMSfit = np.polyfit(self.PDMStemp,self.nPDMS,deg=1)




	def Silicaindex(self):
		
		self.Silicatemp = np.array([22.83686643,40.36719542,70.32692845,103.3346833])
		self.nSilica    = np.array([1.445300107,1.44555516,1.445847903,1.445958546])
		self.SilicaFIT = np.polyfit(self.Silicatemp,self.nSilica,deg=1)



	def addtriBubbles(self):

		RW = self.Rw
		TL = self.Width

		verts = [
	            
	            mp.Vector3(x=-(RW/2+TL/2) ,y=self.R2 ,z=0)   ,
	            mp.Vector3(x=(RW/2+TL/2)  ,y=self.R2 ,z=0)  ,
	            mp.Vector3(x=(RW/2)       ,y=self.R2-self.Depth ,z=0)   ,
	             mp.Vector3(x=-(RW/2)     ,y=self.R2-self.Depth ,z=0)
	        
	            ]


		self.LH = mp.Prism(center=mp.Vector3(x=-self.GAP/2,y=0,z=0),
	                     vertices = verts,
	                     material=mp.Medium(index=self.PDMSn),
	                     height=1
	                     )

		self.RH = mp.Prism(center=mp.Vector3(x=self.GAP/2,y=0,z=0),
	                     vertices = verts,
	                     material=mp.Medium(index=self.PDMSn),
	                     height=1
	                     )

		self.Objlist.extend([self.LH,self.RH])
		