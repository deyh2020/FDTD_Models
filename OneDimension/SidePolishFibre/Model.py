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
		self.BackgroundN  = 1.41
		self.N1 = 1.00
		self.N2 = 1.00

		##Capillary Dimentions
		self.OD     = 62
		self.WallThick  = 8.2

		##Resonator Dimention
		self.Mthick = 5
		self.GAP    = 10
		self.Width  = 10
		self.Pad    = 5

		##Src properties
		self.fcen   = 1/1.55
		self.df     = 0.1e-2 #0.8e-2
		self.nfreq  = 1000

		##MEEP properties
		self.dpml   = 10
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

		self.fig,self.axes = plt.subplots(1,1,dpi=200)

		#Plotting 
		
		

	def mkALLDIRS(self):
		
		self.workingDir = '../data/'+self.today+'/'+self.filename + '_1Dmodel/'  # diffirentiate from other packages
		

		print('WD:',self.workingDir)

		try:
			os.makedirs(self.workingDir)
		except:
			print('AlreadyDir')

		self.sim.use_output_directory(self.workingDir)



	def buildFaboryPeriot(self,NormRun=False):

		self.sx = self.GAP + 2*self.Mthick + 2*self.dpml + 200
		self.sy = 0

		if NormRun:
			N1 = self.BackgroundN
			N2 = self.BackgroundN
		elif NormRun == False:
			N1 = self.N1
			N2 = self.N2

		
		self.cell_size = mp.Vector3(self.sx,self.sy,0)

		self.pml_layers = [mp.PML(thickness=self.dpml,direction=mp.X)]

		Background = mp.Block(
			center=mp.Vector3(0,0,0),
			size=mp.Vector3(mp.inf,mp.inf,mp.inf),
			material=mp.Medium(index=self.BackgroundN)
			)

		M1 = mp.Block(
			center=mp.Vector3(self.GAP/2 + self.Mthick/2,0,0),
			size=mp.Vector3(self.Mthick,mp.inf,mp.inf),
			material=mp.Medium(index=N1)
			)

		M2 = mp.Block(
			center=mp.Vector3(-self.GAP/2 - self.Mthick/2,0,0),
			size=mp.Vector3(self.Mthick,mp.inf,mp.inf),
			material=mp.Medium(index=N2)
			)

		self.Objlist.extend([Background,M1,M2])

	def buildFaboryPeriotSingle(self,NormRun=False):

		self.sx = self.Width + 2*self.Pad + 2*self.dpml
		self.sy = 0

		if NormRun:
			N1 = self.BackgroundN

		elif NormRun == False:
			N1 = self.N1


		
		self.cell_size = mp.Vector3(self.sx,self.sy,0)

		self.pml_layers = [mp.PML(thickness=self.dpml,direction=mp.X)]

		Background = mp.Block(
			center=mp.Vector3(0,0,0),
			size=mp.Vector3(mp.inf,mp.inf,mp.inf),
			material=mp.Medium(index=self.BackgroundN)
			)

		M1 = mp.Block(
			center=mp.Vector3(0,0,0),
			size=mp.Vector3(self.Width,mp.inf,mp.inf),
			material=mp.Medium(index=N1)
			)

		self.Objlist.extend([Background,M1])


	def BuildModel(self,Plot=False,NormRun=False):   # builds sim and plots structure to file 
		
		kx = 0.4
		kpoint = mp.Vector3(kx)

		self.src = [
				mp.Source(mp.GaussianSource(self.fcen,fwidth=self.df),
                     component=mp.Ez,
                     center=mp.Vector3(x=-(self.sx/2)+2*self.dpml),
                     size=mp.Vector3()
					 )
			]

		
		self.sim = mp.Simulation(
			cell_size=self.cell_size,
			geometry=self.Objlist,
			sources=self.src,
			resolution=self.res,
			force_complex_fields=False,
			eps_averaging=False,
			boundary_layers=self.pml_layers,
			progress_interval=30,
			Courant=self.Courant
			)


		self.mkALLDIRS()

		# src flux
		src_fr = mp.FluxRegion(center=mp.Vector3(-(self.sx/2) + 2*self.dpml+5,0,0), size=mp.Vector3())                            
		self.refl = self.sim.add_flux(self.fcen, self.df, self.nfreq, src_fr)

		# transmitted flux
		tran_fr = mp.FluxRegion(center=mp.Vector3((self.sx/2) - 2*self.dpml ,0,0), size=mp.Vector3())
		self.tranE = self.sim.add_flux(self.fcen, self.df, self.nfreq, tran_fr)


		#fig,ax = plt.subplots(dpi=150)
		#if NormRun:
		#	self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
		#	plt.savefig(self.workingDir+"NormModel_" + str(self.Datafile) +".pdf")
		#else:
		#	self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
		#	plt.savefig(self.workingDir+"Model_" + str(self.Datafile) +".pdf")

		

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
			until=5*self.sx*self.BackgroundN
			)
		

		
		# for normalization run, save flux fields data for reflection plane
		self.norm_refl = self.sim.get_flux_data(self.refl)
		# save incident power for transmission plane
		self.norm_tran = mp.get_fluxes(self.tranE)

		print("")
		print("")
		print("Completed")
		print("")
		print("")



	def AutoRun(self):
		
		print("")
		print("")
		print("Actual Run")
		print("")
		print("")

		#self.myRunFunction(self.monitorPts)

		self.sim.run(
		    mp.at_beginning(mp.output_epsilon),
			#mp.at_every(100,mp.output_efield_z),
			until=10*self.sx*self.BackgroundN
			
			)

		#pt = mp.Vector3()

		#self.sim.run(
			#mp.at_beginning(mp.output_epsilon),
			#mp.at_every(500, mp.output_dpwr),
		#	until_after_sources=mp.stop_when_fields_decayed(dt,mp.Ez,pt,self.DecayF)
		#	)
		

		flux_freqs = mp.get_flux_freqs(self.refl)
		refl_flux = mp.get_fluxes(self.refl)
		tran_flux = mp.get_fluxes(self.tranE)

		Data = {}
		Data['flux_freqs'] = flux_freqs
		Data['refl_flux'] = refl_flux
		Data['tran_flux'] = tran_flux
		Data['norm_tran'] = self.norm_tran
		Data['norm_refl'] = self.norm_refl

		with open(self.workingDir + self.Datafile + ".pkl", 'wb') as file:
			pickle.dump(Data,file)




		wl = []
		Rs = []
		Ts = []
		for i in range(self.nfreq):
			wl = np.append(wl, 1000/flux_freqs[i])
			Rs = np.append(Rs,-refl_flux[i]/self.norm_tran[i])
			Ts = np.append(Ts,tran_flux[i]/self.norm_tran[i])




		

		self.axes.plot(wl,Ts,label=self.Datafile + 'C')
		
		from scipy.signal import find_peaks

		peaks, _ = find_peaks(-Ts+1.0, height=0)


		self.axes.plot(wl[peaks],Ts[peaks],'x')

		print(wl[peaks])

		FSR = np.diff(wl[peaks])

		print(FSR)

		print(np.average(FSR))

		plt.legend(loc="upper right")
		#plt.xlim((1530,1570))
		plt.savefig(self.workingDir+"TransRef_" + str(self.Datafile) + "_" + str(self.Mthick) +".pdf")
		#plt.show()


	def RunTRspectrumSingleFP(self):
		
		self.tic()
		self.Objlist = []							#Reset Model and build structure

		self.buildFaboryPeriotSingle(NormRun=True)  						#builds base polished fibre structure list		
		self.BuildModel(NormRun=True,Plot=False) 

		#Run normal model
		self.NormRun()

		#Reset sources
		self.sim.reset_meep()
		

		self.Objlist = []	
		self.buildFaboryPeriotSingle(NormRun=False) 						#builds base polished fibre structure list
		
		


		self.BuildModel(NormRun=False,Plot=True) 

		#load data from the normal run
		self.sim.load_minus_flux_data(self.refl,self.norm_refl)

		self.AutoRun()
		self.toc()
		#self.SaveMeta()

		self.sim = None


	def RunTRspectrumDoubleFP(self):
		
		self.tic()
		self.Objlist = []							#Reset Model and build structure

		self.buildFaboryPeriot(NormRun=True)  						#builds base polished fibre structure list		
		self.BuildModel(NormRun=True,Plot=False) 

		#Run normal model
		self.NormRun()

		#Reset sources
		self.sim.reset_meep()
		

		self.Objlist = []	
		self.buildFaboryPeriot(NormRun=False) 						#builds base polished fibre structure list
		
		


		self.BuildModel(NormRun=False,Plot=True) 

		#load data from the normal run
		self.sim.load_minus_flux_data(self.refl,self.norm_refl)

		self.AutoRun()
		self.toc()
		#self.SaveMeta()

		self.sim = None



		



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
		