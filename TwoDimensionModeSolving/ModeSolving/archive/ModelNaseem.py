import meep as mp
from meep.visualization import plot2D
import numpy as np
import matplotlib.pyplot as plt
import sys, getopt,os
from datetime import date
import pickle,json, os
import time



class Model:

	def __init__(self):

		self.TicToc = self.TicTocGenerator() # create an instance of the TicTocGen generator
		
		##Material N
		self.Coating = 'Air'
		self.nCoating = 1.41
		self.coreN  = 1.445
		self.cladN  = 1.440

		##Fibre Dimentions
		self.R1     = 4.1
		self.R2     = 62.5
		self.Pad    = 0
		self.height = 40

		##Src properties / c=1
		self.wl     = 1.55
		self.fcen   = 1/self.wl
		self.df     = 2e-2
		self.nfreq  = 1000

		##MEEP properties
		self.res    = 12
		self.DecayF = 1e-8
		self.WallT  = 0
		self.SimT   = 10
		self.today  = str(date.today())
		self.filename= 'test'
		self.Datafile = 'Default'
		self.sim    = None
		self.Objlist = []
		self.Notes   = ''
		self.SimSize = 40
		self.PMLThick = 2
		self.SrcSize  = self.SimSize - 2*self.PMLThick
		self.kpoint = mp.Vector3(x=0,y=0,z=self.fcen*self.coreN)
		self.FibreType = ''

		#LoadTempDependanceData
		self.PDMSindex()
		self.Silicaindex()

		#init Data arrays
		self.srcE  = np.array([])
		self.tranE = np.array([])



	def buildFibre(self):

		self.SrcSize  = self.SimSize - 2*self.PMLThick
		self.cell_size = mp.Vector3(self.SimSize,self.SimSize,0)

		self.pml_layers = [
			mp.PML(thickness=self.PMLThick,direction=mp.X),
			mp.PML(thickness=self.PMLThick,direction=mp.Y)
			]

		self.Core = mp.Cylinder(
			radius=self.R1,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.coreN)
			)

		self.Clad = mp.Cylinder(
			radius=self.R2,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.cladN)
			)

		self.Objlist.extend([self.Clad,self.Core])

	def buildPolishedFibre(self,WPDMS=False):

		self.SrcSize  = self.SimSize - 2*self.PMLThick
		self.cell_size = mp.Vector3(self.SimSize,self.SimSize,0)

		self.pml_layers = [
			mp.PML(thickness=self.PMLThick,direction=mp.X),
			mp.PML(thickness=self.PMLThick,direction=mp.Y)
			]

		self.PolishedZone = mp.Block(
			center=mp.Vector3(y=self.R2/2+self.R1+self.Pad), 
			size=mp.Vector3(250,62.5,mp.inf), 
			material=mp.Medium(index=self.nCoating))
		

		self.Core = mp.Cylinder(
			radius=self.R1,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.coreN)
			)

		self.Clad = mp.Cylinder(
			radius=self.R2,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.cladN)
			)

		self.Objlist.extend([self.Clad,self.Core,self.PolishedZone])
		print(self.Objlist)

	def buildParallelBlocks(self):

		self.SrcSize  = self.SimSize - 2*self.PMLThick
		self.cell_size = mp.Vector3(self.SimSize,self.SimSize,0)

		self.pml_layers = [
			mp.PML(thickness=self.PMLThick,direction=mp.X),
			mp.PML(thickness=self.PMLThick,direction=mp.Y)
			]

		self.Coating = mp.Block(
			center=mp.Vector3(),
			size=mp.Vector3(x=mp.inf,y=mp.inf),
			material=mp.Medium(index=self.nCoating)
			)

		self.Clad = mp.Block(
			center=mp.Vector3(),
			size=mp.Vector3(x=mp.inf,y=self.height),
			material=mp.Medium(index=self.cladN)
			)

		self.Objlist.extend([self.Coating,self.Clad])




	def BuildModel(self,Plot=False,axes=None):   # builds sim and plots structure to file 

		
		self.fcen   = 1/self.wl
		self.df     = 0.1*self.fcen
		self.kpoint = mp.Vector3(x=0,y=0,z=self.fcen*self.coreN)


		self.src = [
				mp.EigenModeSource(
					src=mp.GaussianSource(
						self.fcen,
						fwidth=self.df
						),
				    center=mp.Vector3(0,0,0),
				    size=mp.Vector3(self.SrcSize,self.SrcSize,0),
				    direction=mp.Z,
				    eig_kpoint=self.kpoint,
				    eig_band=1,
				    eig_parity=mp.ODD_Y,
				    eig_match_freq=True,
					eig_resolution=1
				)
			]

		

		
		self.sim = mp.Simulation(
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			symmetries=[mp.Mirror(mp.X)],
			force_complex_fields=True,
			eps_averaging=True,
			boundary_layers=self.pml_layers,
			k_point=self.kpoint,   
			ensure_periodicity=False
			)

		self.mkALLDIRS()

		if Plot:
			if axes == None:
					ax = plt.axes()
			else:
				ax = axes,
			self.sim.plot2D(
				ax = ax,
				#output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
				#fields=mp.Ez,
				plot_sources_flag=False,
				plot_monitors_flag=False,
				plot_eps_flag=True,
				eps_parameters={'alpha':0.8, 'interpolation':'none'}
			)

	def BuildModel_CW(self,Plot=False,axes=None):   # builds sim and plots structure to file 

		
		self.fcen   = 1/self.wl
		self.df     = 0.1*self.fcen
		self.kpoint = mp.Vector3(x=0,y=0,z=self.fcen*self.coreN)


		self.src = [
				mp.EigenModeSource(
					src=mp.ContinuousSource(
						self.fcen
						),
				    center=mp.Vector3(0,0,0),
				    size=mp.Vector3(self.SrcSize,self.SrcSize,0),
				    direction=mp.Z,
				    eig_kpoint=self.kpoint,
				    eig_band=1,
				    eig_parity=mp.ODD_Y,
				    eig_match_freq=True,
					eig_resolution=1
				)
			]

		

		
		self.sim = mp.Simulation(
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			symmetries=[mp.Mirror(mp.X)],
			force_complex_fields=True,
			eps_averaging=True,
			boundary_layers=self.pml_layers,
			k_point=self.kpoint,   
			ensure_periodicity=False
			)

		self.mkALLDIRS()

		if Plot:
			if axes == None:
					ax = plt.axes()
			else:
				ax = axes,
			self.sim.plot2D(
				ax = ax,
				#output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
				#fields=mp.Ez,
				plot_sources_flag=False,
				plot_monitors_flag=False,
				plot_eps_flag=True,
				eps_parameters={'alpha':0.8, 'interpolation':'none'}
			)
			plt.savefig(self.workingDir+"EPS_"+ str(self.Datafile) +".pdf")
			


	def RunAndPlotF(self,axes=None):

		t = (1e-6/3e8)
		tFactor = 1e-15/t # converts femptoseconds into unitless MEEP

		print("Actual Simtime:", self.SimT*t)

		self.sim.run(
			mp.at_beginning(mp.output_epsilon),
			mp.at_end(mp.output_efield_z),
			until_after_sources=self.SimT
			)

		if axes == None:
			fig,axes = plt.subplots(dpi=200)

		self.sim.plot2D(
			ax = axes,
			#output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
			fields=mp.Ey,
			plot_sources_flag=False,
			plot_monitors_flag=False,
			eps_parameters={'alpha':0.8, 'interpolation':'none','cmap':'binary','contour':True},
			field_parameters={'alpha':0.7,'cmap':'Greys'}
			)
		plt.savefig(self.workingDir+"FieldsAtEnd_"+ str(self.Datafile) +".pdf")
		plt.show()
		

	def BuildAndSolveNEFF(self):

		self.Objlist = []

		if self.FibreType == "Standard":
			self.buildFibre()
		elif self.FibreType == "Polished":
			self.buildPolishedFibre()
		else:
			print("Fibre Type not selected")

		self.BuildModel_CW(Plot=False)
		self.RunMPB()
		self.sim.reset_meep()


	def BuildAndSolve(self,axes=None):

		self.Objlist = []

		if self.FibreType == "Standard":
			self.buildFibre()
		elif self.FibreType == "Polished":
			self.buildPolishedFibre()
		else:
			print("Fibre Type not selected")

		self.BuildModel_CW(Plot=True)
		#self.RunAndPlotF_FDS(axes=axes)

		print(self.workingDir)
		
		if os.path.isfile(self.workingDir + "runner-ey-000000.00.h5"): #Check if the sim has already ran before?			
			print("AlreadyRan")
		else:
			print("FirstRun")
			self.sim.init_sim()
			mp.output_epsilon(self.sim)
			self.sim.solve_cw()
			mp.output_efield_y(self.sim)


	def RunAndPlotF_FDS(self,axes=None):

		t = (1e-6/3e8)
		tFactor = 1e-15/t # converts femptoseconds into unitless MEEP

		self.sim.init_sim()
		mp.output_epsilon(self.sim)
		self.sim.solve_cw()
		mp.output_efield_y(self.sim)



		if axes == None:
			fig,axes = plt.subplots(dpi=200)

		self.sim.plot2D(
			ax = axes,
			#output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
			fields=mp.Ey,
			plot_sources_flag=False,
			plot_monitors_flag=False,
			plot_boundaries_flag=False,
			plot_eps_flag=True,
			eps_parameters={'alpha':1, 'interpolation':'none','cmap':'binary','contour':False},
			field_parameters={'alpha':0.8,'cmap':'gnuplot'}
			)


	def RunMPB(self):

		self.sim.init_sim()

		self.EigenmodeData = self.sim.get_eigenmode(
			self.fcen,
			mp.Z,
			mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SrcSize,self.SrcSize,0)),
			band_num=1,
			kpoint=self.kpoint,
			match_frequency=True,
			resolution=self.res
			)

		self.k = self.EigenmodeData.k
		self.vg = self.EigenmodeData.group_velocity
		self.neff = self.k.norm() * self.wl

		

	def mkALLDIRS(self):
		
		self.workingDir = '../data/'+self.today+'/'+self.filename+'_ModeSolving/'

		print('WD:',self.workingDir)

		try:
			os.makedirs(self.workingDir)
		except:
			print('AlreadyDir')

		self.sim.use_output_directory(self.workingDir)

	def dumpData2File(self):
    
		# initialise main data dictionary
		Data = {}
		Data['Src'] = {}       # sensor just after source.
		Data['Out'] = {}       # sensor at the end of the WG (for transmission)
		
		
		Data['Src']['lambda'] = 1/np.array(mp.get_flux_freqs(self.srcE))
		Data['Src']['flux'] = np.array(mp.get_fluxes(self.srcE))
		
		Data['Out']['lambda'] = 1/np.array(mp.get_flux_freqs(self.tranE))
		Data['Out']['flux'] = np.array(mp.get_fluxes(self.tranE))
		

		metadata = {
			"date": str(self.today),
			"Data": self.workingDir+"Data.pk1"
		}

		metadata = {**metadata,**self.meta}
		

		with open(metadata['Data'], 'wb') as file:
			pickle.dump(Data,file)


		with open(self.workingDir + 'metadata.json', 'w') as file:
			json.dump(metadata, file)


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
		tempTimeInterval = next(self.TicToc)
		if tempBool:
			print( "Elapsed time: %f seconds.\n" %tempTimeInterval )

	def tic(self):
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


	def AirN(self,T):
		p = 1013.25
		e = 20
		N = (77.6/T)*(p + 4810*(e/T))
		n = (N/1e6) + 1
		return n
	
	def SaveMeta(self):
		
		self.metadata = {
		##Material N
		"nCoating": self.nCoating,
		"CoreN":self.coreN,
		"CladN":self.cladN,
		
		##Fibre Dimentions
		"R1":self.R1,
		"R2":self.R2,
		"CladLeft":self.Pad,

		##Src properties
		"fcen":self.fcen,
		"df":self.df, 
		"nfreq":self.nfreq,

		##MEEP properties
		#"dpml":self.dpml,
		"resolution":self.res,
		"DecayF":self.DecayF,
		"WallT":self.WallT,
		"SimT":self.SimT,
		"today":self.today,
		"filename":self.filename,
		"notes":self.Notes,

		"neff":self.neff,

        }

		
		with open(self.workingDir + 'metadata' + str(self.Datafile) + '.json' , 'w') as file:
			json.dump(self.metadata, file)
	