import meep as mp
import numpy as np
from datetime import date
import pickle,json, os

def dumpData2File(meta,today,workingDir,sim,src,tran,sphereMode,nfreq):
    
    # initialise main data dictionary
    Data = {}
    Data['WGM_mode'] = {}  # FT sensor in the sphere. 
    Data['Src'] = {}       # sensor just after source.
    Data['Out'] = {}       # sensor at the end of the WG (for transmission)
    
    # array of y-position values measured (y-axis sensor at x=0)
    Data['WGM_mode']['yPos'] = sim.get_array_metadata(center=mp.Vector3(0,36,0), size=mp.Vector3(0,10,0))[1]
    # array of wavelengths measured if ft.
    Data['WGM_mode']['lambda'] = 1/np.array(mp.get_flux_freqs(sphereMode))

    nfreq = len(Data['WGM_mode']['lambda'])


    # initialize wl vs y-pos matrix.
    matrix = np.zeros([len(sim.get_dft_array(sphereMode,mp.Ez,0)),nfreq],dtype=np.complex128)
    
    # fill matrix
    for i in range(0,nfreq):
        matrix[:,i] = sim.get_dft_array(sphereMode,mp.Ez,i)

    #drop patrix into dictionary    
    Data['WGM_mode']['matrix'] = matrix

    
    Data['Src']['lambda'] = 1/np.array(mp.get_flux_freqs(src))
    Data['Src']['flux'] = np.array(mp.get_fluxes(src))
    
    Data['Out']['lambda'] = 1/np.array(mp.get_flux_freqs(tran))
    Data['Out']['flux'] = np.array(mp.get_fluxes(tran))
    




    metadata = {
        "date": str(today),
        "Data": workingDir+"Data.pk1"
    }

    metadata = {**metadata,**meta}
    

    with open(metadata['Data'], 'wb') as file:
        pickle.dump(Data,file)


    with open(workingDir + 'metadata.json', 'w') as file:
        json.dump(metadata, file)

    

def buildWGMmodel(WGMr,WGr,Gap,fsrc,df,resolution,nfreq):


    fsrc = 1/1.5475 # frequency of eigenmode or constant-amplitude source
    df = 16e-3

    nfreq = 1000

    resolution = 20 #pixels per distance unit, so 10 px/um rn. (ideal)


    WGMr = 40
    WGr = 0.5
    Fthick = 0.05

    cell = mp.Vector3(100,100,0) # in microns

    wgYpos = -WGMr-Gap-WGr

    WaveGuide = mp.Block(mp.Vector3(88,WGr*2,mp.inf),
            center=mp.Vector3(y=wgYpos),
            material=mp.Medium(index=1.440))

    Circle = mp.Cylinder(radius=WGMr, material=mp.Medium(index=1.440))

    WGFilm1 = mp.Block(mp.Vector3(10,0.05,mp.inf),
                        center=mp.Vector3(y=wgYpos+0.5+0.025),
                        material=mp.Medium(index=2.5))

    WGFilm2 = mp.Block(mp.Vector3(10,0.05,mp.inf),
                        center=mp.Vector3(y=wgYpos-0.50-0.025),
                        material=mp.Medium(index=2.5))



    geometry = [WaveGuide,Circle,WGFilm1,WGFilm2]


    kx = 0.4    # initial guess for wavevector in x-direction of eigenmode
    kpoint = mp.Vector3(kx)
    bnum = 1    # band number of eigenmode

    sources = [mp.EigenModeSource(src=mp.GaussianSource(fsrc,fwidth=df),
            center=mp.Vector3(x=-40,y=wgYpos),
            size=mp.Vector3(y=5),
            direction=mp.NO_DIRECTION,
            eig_kpoint=kpoint,
            eig_band=bnum,
            eig_parity=mp.EVEN_Y+mp.ODD_Z,
            eig_match_freq=True)
            ]


    pml_layers = [mp.PML(thickness=5.0)]

    sim = mp.Simulation(cell_size=cell,
            boundary_layers=pml_layers,
            eps_averaging=True,
            geometry=geometry,
            sources=sources,
            resolution=resolution,
            progress_interval=30,
            split_chunks_evenly=False
            )


    # src flux
    src_fr = mp.FluxRegion(center=mp.Vector3(-35,wgYpos,0), size=mp.Vector3(0,3,0))                            
    src = sim.add_flux(fsrc, 8e-3, nfreq, src_fr)



    # transmitted flux
    tran_fr = mp.FluxRegion(center=mp.Vector3(40,wgYpos,0), size=mp.Vector3(0,3,0))
    tran = sim.add_flux(fsrc, 8e-3, nfreq, tran_fr)

    # Sphere flux

    sphere_fr = mp.FluxRegion(center=mp.Vector3(0,36,0), size=mp.Vector3(0,10,0))
    sphereMode = sim.add_flux(fsrc, 8e-3, nfreq, sphere_fr)


    return sim,src,tran,sphereMode




import time

def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        return tempTimeInterval

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)