import meep as mp
import MyMeepFunctions as myF


Gap = 6.434e-01

fsrc = 1/1.5475 # frequency of eigenmode or constant-amplitude source
df = 16e-3

nfreq = 3000
resolution = 20 #pixels per distance unit, so 10 px/um rn. (ideal)


#flux_freqs = mp.get_flux_freqs(src)

WGMr = 40
WGr = 0.5

sim,src,tran,sphereMode = myF.buildWGMmodel(WGMr,WGr,Gap,fsrc,df,resolution,nfreq)


pt = mp.Vector3(x=0,y=39.5)

sim.run(mp.at_beginning(mp.output_epsilon),
      until_after_sources=mp.stop_when_fields_decayed(750,mp.Ez,pt,0.9))
