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
		self.capN      = 1.440
		self.fillN     = 2.50

		##Capillary Dimentions
		self.OD     = 62
		self.WallThick  = 8.2

		##Resonator Dimention

		##Src properties
		self.fcen   = 1/1.55
		self.df     = 0.1e-2 #0.8e-2
		self.nfreq  = 1000

		##MEEP properties
		self.dpml   = 5
		self.res    = 10/1.55
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
		self.Courant = 1/np.sqrt(2)


		#init Data arrays
		self.srcE  = np.array([])
		self.tranE = np.array([])

		self.PDMSindex()
		self.Silicaindex()


	def TestSpectrum(self):	

		self.Objlist = []	
		self.buildPolished()  						#builds base polished fibre structure list
		self.ADDsqrBubbles()  					#add sqr bubbles to the structure list
		self.ADDsqrEmptyBubbles()
		self.BuildModel(NormRun=False,Plot=True) 

		#load data from the normal run
		
		self.QuickRun()

		

	def mkALLDIRS(self):
		
		self.workingDir = 'data/'+self.today+'/'+self.filename+'/'

		print('WD:',self.workingDir)

		try:
			os.makedirs(self.workingDir)
		except:
			print('AlreadyDir')

		self.sim.use_output_directory(self.workingDir)



	def buildFilledCapillary(self):

		self.sx = self.OD + 10 + 2*self.dpml
		self.sy = self.OD + 10 + 2*self.dpml

		
		self.cell_size = mp.Vector3(self.sx,self.sy,0)

		self.pml_layers = [mp.PML(thickness=self.dpml)]


		OD = mp.Cylinder(
			radius=self.OD/2,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.capN)
			)

		ID = mp.Cylinder(
			radius=(self.OD - (self.WallThick*2))/2,
			height=mp.inf,
			axis=mp.Vector3(0,0,1),
			material=mp.Medium(index=self.fillN)
			)

		self.Objlist.extend([OD,ID])


	def BuildModel(self,Plot=False,NormRun=False):   # builds sim and plots structure to file 
		
		kx = 0.4
		kpoint = mp.Vector3(kx)

		self.src = [
				mp.EigenModeSource(src=mp.GaussianSource(self.fcen,fwidth=self.df),
				center=mp.Vector3(x=0,y=-self.OD/2),
				size=mp.Vector3(y=4),
				direction=mp.X,
				eig_kpoint=kpoint,
				eig_band=1,
				eig_parity=mp.EVEN_Y,
				eig_match_freq=True
				)
			]

		
		self.sim = mp.Simulation(
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			force_complex_fields=False,
			eps_averaging=True,
			boundary_layers=self.pml_layers,
			progress_interval=30,
			Courant=self.Courant
			#k_point=mp.Vector3(mp.X)
			)


		self.mkALLDIRS()

		#Stored_flux = mp.FluxRegion(center=mp.Vector3(0,self.OD/2 - 5,0), size=mp.Vector3(0,12,0))
		#self.Stored = self.sim.add_flux(self.fcen, self.df, self.nfreq, Stored_flux)

		storedFlux = mp.FluxRegion(center=mp.Vector3(0,self.OD/2 - 4,0), size=mp.Vector3(0,12,0))
		self.storedFlux = self.sim.add_flux(self.fcen, self.df, self.nfreq, storedFlux)

		fig,ax = plt.subplots(dpi=150)
		if NormRun:
			self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
			plt.savefig(self.workingDir+"NormModel_" + str(self.Datafile) +".pdf")
		else:
			self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
			plt.savefig(self.workingDir+"Model_" + str(self.Datafile) +".pdf")

		

	def NormRun(self):

		print("")
		print("")
		print("Normalisation Run")
		print("")
		print("")

		#while sum(mp.get_fluxes(self.tranE)) == 0.0:
		#	print(sum(mp.get_fluxes(self.tranE)))
		#	print("looped")
		
		self.sim.run(
		#	#mp.at_beginning(mp.output_epsilon),
			#mp.at_every(100,mp.output_efield_z),
			until=2*self.sx*self.coreN
			
			)
		#

		self.sim.run(
		#	#mp.at_beginning(mp.output_epsilon),
		#	#mp.at_every(250,mp.output_efield_z),
			until=mp.stop_when_fields_decayed(
				500,
				mp.Ez,mp.Vector3(0.5*self.sx - 0.5*self.dpml,0),self.DecayF
				)
		)

		

		
		# for normalization run, save flux fields data for reflection plane
		self.norm_refl = self.sim.get_flux_data(self.refl)
		# save incident power for transmission plane
		self.norm_tran = mp.get_fluxes(self.tranE)



	def AutoRun(self):
		
		print("")
		print("")
		print("Actual Run")
		print("")
		print("")

		#self.myRunFunction(self.monitorPts)
		

		self.sim.run(
			mp.at_beginning(mp.output_epsilon),
			until_after_sources=100
		)

		self.sim.run(
			#mp.at_every(100, mp.output_efield_z), 
			until=self.SimT
		)



		# initialize wl vs y-pos matrix.
		matrix = np.zeros([len(self.sim.get_dft_array(self.storedFlux,mp.Ez,0)),self.nfreq],dtype=np.complex128)
		
		# fill matrix
		for i in range(0,self.nfreq):
			matrix[:,i] = self.sim.get_dft_array(self.storedFlux,mp.Ez,i)


		with open(self.workingDir + self.Datafile + ".pkl", 'wb') as file:
			pickle.dump(matrix,file)


		"""
		wl = []
		Rs = []
		Ts = []
		for i in range(self.nfreq):
			wl = np.append(wl, 1/flux_freqs[i])
			Rs = np.append(Rs,-refl_flux[i]/self.norm_tran[i])
			Ts = np.append(Ts,tran_flux[i]/self.norm_tran[i])

		plt.figure()
		plt.plot(wl,Rs,'--',label='reflectance')
		plt.plot(wl,Ts,label='transmittance')
		plt.plot(wl,1-Rs-Ts,label='loss')
		#plt.axis([5.0, 10.0, 0, 1])
		plt.xlabel("wavelength (μm)")
		plt.legend(loc="upper right")
		plt.savefig(self.workingDir+"TransRef_" + str(self.Datafile) +".pdf")
		#plt.show()
		"""


	def QuickRun(self):
		
		print("")
		print("")
		print("Quick Run")
		print("")
		print("")

		#self.myRunFunction(self.monitorPts)

		self.sim.run(
		#	#mp.at_beginning(mp.output_epsilon),
			#mp.at_every(100,mp.output_efield_z),
			until=2*self.sx*self.coreN
			
			)

		flux_freqs = mp.get_flux_freqs(self.refl)
		refl_flux = mp.get_fluxes(self.refl)
		tran_flux = mp.get_fluxes(self.tranE)
		
		wl = []
		Rs = []
		Ts = []
		for i in range(self.nfreq):
			wl = np.append(wl, 1/flux_freqs[i])
			Rs = np.append(Rs,-refl_flux[i])
			Ts = np.append(Ts,tran_flux[i])

		plt.figure()
		plt.plot(wl,Rs,'--',label='reflectance')
		plt.plot(wl,Ts,label='transmittance')
		plt.plot(wl,1-Rs-Ts,label='loss')
		#plt.axis([5.0, 10.0, 0, 1])
		plt.xlabel("wavelength (μm)")
		plt.legend(loc="upper right")
		plt.savefig(self.workingDir+"TransRef_" + str(self.Datafile) +".pdf")
		#plt.show()


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
		