from cgitb import reset
from curses.ascii import STX
from tkinter import Variable
from xml.etree.ElementPath import get_parent_map
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

		#Huge Dictionary of variables

		self.Variables = {
			#programming vars 
			"debug":False,
			"prevRun":False,
			"SimTime":0.0,
			#refractive indexes
			"nAir": 1.000,
			"nCore":1.445,
			"nClad":1.440,
			"nPDMS":1.410,
			#Device Dimentions
			"taperD":1.000,
			"capD":80,
			"WallThick":10.000,
			"GAP":0.667,
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
			"workingDir":'',
			"filename":'test',
			"dataFile":'test',
			"roundTrips":1.00,    #relates to how long the sim will run relative to orbits of the WGM
			#Flags
			"normal":True,
			"savefields":False
		}


		self.sim = None
		self.PDMSindex()
		self.Silicaindex()
		self.Objlist = []

	

	def RunTRspectrum(self):

		#if self.Variables['debug'] == True:
		self.Variables["workingDir"] = '../data/'+self.Variables["today"]+'/'+self.Variables['filename']+'/'
		self.mkALLDIRS()
				
		#check whether fields file exists.
		if os.path.exists(self.Variables["workingDir"] + "fields.h5"):
			try:
				#try to reload variables
				with open(self.Variables['workingDir'] + "metadata.json") as json_file:
					self.Variables = json.load(json_file)
			except:
				print("Tried to load old vars from .json")
			print("settign var true")
			self.Variables["prevRun"] = True 

		
		self.tic()
		self.Objlist = []					#Reset Model and build structure

		if self.Variables["normal"] == True and self.Variables["prevRun"] == False:
			self.buildNorm()  						#builds base polished fibre structure list		
			self.BuildModel(NormRun=True,Plot=True) 

			#Run normal model
			self.NormRun()

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
			

		self.Objlist = []
		
		self.buildFilledCapillary()  						#builds base polished fibre structure list
		self.BuildModel(NormRun=False,Plot=True) 


		self.AutoRun()
		self.toc()
		self.sim.print_times()

		self.SaveMeta()


	def PlotStructure(self):	

		self.Objlist = []	
		self.buildFilledCapillary()  						#builds base polished fibre structure list
		#self.buildNorm()
		self.BuildModel(NormRun=False,Plot=True) 
		plt.show()

	def buildNorm(self):

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



	def buildFilledCapillary(self):



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
			material=mp.Medium(index=self.Variables['nPDMS'])
			)

		self.taperYpos = -(self.Variables["capD"]/2.0 + self.Variables["GAP"] + self.Variables["taperD"]/2)

		Taper = mp.Block(
			center=mp.Vector3(0,self.taperYpos,0),
			size=mp.Vector3(mp.inf,self.Variables["taperD"],mp.inf),
			material=mp.Medium(index=self.Variables['nClad'])
			)

		self.Objlist.extend([OD,ID,Taper])


	def BuildModel(self,Plot=False,NormRun=False):   # builds sim and plots structure to file 
		
		kx = 0.4
		kpoint = mp.Vector3(kx)

		fcen  = 1.0/((self.Variables['EndWL'] + self.Variables['StartWL'])/2.0)
		df    = ((1/self.Variables['StartWL']) - (1/self.Variables['EndWL']))
		nfreq = int((self.Variables['EndWL']-self.Variables['StartWL'])/self.Variables['WLres'])

		print("")
		print("")
		print("")
		print("Datapoints:-   " + str(nfreq))
		print("")
		print("")
		print("")
		


		self.Variables['fcen'] = fcen
		self.Variables['df'] = df
		self.Variables['nfreq'] = nfreq
		
		sx   = self.Variables['sx']
		sy   = self.Variables['sy']
		dpml = self.Variables['dpml']
		res     = self.Variables['res']
		Courant = self.Variables['Courant']
		
		PAD     = self.Variables['PAD']
		GAP		= self.Variables['GAP']
		workingDir = self.Variables['workingDir']
		dataFile   = self.Variables['dataFile']


		self.src = [
				mp.EigenModeSource(src=mp.GaussianSource(
					fcen,
					fwidth=df
					),
				center=mp.Vector3(x=-(sx/2)+2*dpml,y=self.taperYpos),
				size=mp.Vector3(y=5),
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
			resolution=res,
			force_complex_fields=False,
			eps_averaging=True,
			boundary_layers=self.pml_layers,
			progress_interval=30,
			Courant=Courant
			#geometry_center=mp.Vector3(x=0,y=-25,z=0)
			#k_point=mp.Vector3(mp.X)
			)
		self.sim.use_output_directory(self.Variables["workingDir"])


		


		print(fcen)
		print(df)
		print(nfreq)

		# transmitted flux
		tran_fr = mp.FluxRegion(center=mp.Vector3((sx/2) - 2*dpml ,self.taperYpos,0), size=mp.Vector3(0,5,0))
		
		self.tranE = self.sim.add_flux(fcen, df, nfreq, tran_fr)


		"""
		if self.FluxRegion == True:
			print("Adding flux") 
			self.dft_fields = self.sim.add_dft_fields([mp.Dz,mp.Ez],
                                fcen,0,1,
                                center=mp.Vector3(-PAD/2,-self.Depth/2,0),
                                size=mp.Vector3(1.2*self.GAP+self.Width,1.2*self.Depth,0),
                                yee_grid=True)
		"""
		
		fig,ax = plt.subplots(dpi=150)
		if NormRun:
			self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
			plt.savefig(workingDir+"NormModel_" + str(dataFile) +".pdf")
		else:
			self.sim.plot2D(ax=ax,eps_parameters={'alpha':0.8, 'interpolation':'none'},frequency=0)
			plt.savefig(workingDir+"Model_" + str(dataFile) +".pdf")

		

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
			until_after_sources=self.Variables['sx']*self.Variables['nClad']
			)

		

		
		# for normalization run, save flux fields data for reflection plane
		#self.norm_refl = self.sim.get_flux_data(self.refl)
		# save incident power for transmission plane
		self.norm_tran = mp.get_fluxes(self.tranE)



	def AutoRun(self):

		print("prevRun"+str(self.Variables["prevRun"]))
		#self.myRunFunction(self.monitorPts)
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
		
		print("")
		print("")
		print("Actual Run")
		print("")
		print("")

		print("Previous SimTime = " + str(self.Variables['SimTime']))

		

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

		
		#if self.FluxRegion == True:
		#	with open(self.workingDir + "ResonantFlux.pkl", 'wb') as file:
		#		pickle.dump(Data,file)




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
		

	def mkALLDIRS(self):
		

		print('WD:',self.Variables["workingDir"])

		try:
			os.makedirs(self.Variables["workingDir"])
		except:
			print('AlreadyDir')

		


	def SaveMeta(self):

		self.Variables['CPUS'] = str(self.sim.num_chunks)
		
		with open(self.Variables['workingDir'] + 'metadata.json', 'w') as file:
			json.dump(self.Variables, file)



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
		self.Variables['WallT'] = next(self.TicToc)
		print("Whole Sim Walltime: "+ str(self.Variables['WallT']) + " s")
		 

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