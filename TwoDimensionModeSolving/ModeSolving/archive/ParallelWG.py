import meep as mp
import numpy as np
import matplotlib.pyplot as plt

resolution = 40   # pixels/μm
    
Si = mp.Medium(index=3.45)

dpml = 1.0
pml_layers = [mp.PML(dpml)]
    
sx = 5
sy = 3
cell = mp.Vector3(sx+2*dpml,sy+2*dpml,0)

a = 1.0     # waveguide width/height

k_point = mp.Vector3(z=0.5)

def parallel_waveguide(s,xodd):
    geometry = [mp.Block(center=mp.Vector3(-0.5*(s+a)),
                         size=mp.Vector3(a,a,mp.inf),
                         material=Si),
                mp.Block(center=mp.Vector3(0.5*(s+a)),
                         size=mp.Vector3(a,a,mp.inf),
                         material=Si)]

    symmetries = [mp.Mirror(mp.X, phase=-1 if xodd else 1),
                  mp.Mirror(mp.Y, phase=-1)]

    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell,
                        geometry=geometry,
                        boundary_layers=pml_layers,
                        symmetries=symmetries,
                        k_point=k_point)

    sim.init_sim()
    EigenmodeData = sim.get_eigenmode(0.22,
                                      mp.Z,
                                      mp.Volume(center=mp.Vector3(), size=mp.Vector3(sx,sy)),
                                      2 if xodd else 1,
                                      k_point,
                                      match_frequency=False,
                                      parity=mp.ODD_Y)

    fcen = EigenmodeData.freq
    print("freq:, {}, {}, {}".format("xodd" if xodd else "xeven", s, fcen))

    sim.reset_meep()

    eig_sources = [mp.EigenModeSource(src=mp.GaussianSource(fcen, fwidth=0.1*fcen),
                                      size=mp.Vector3(sx,sy),
                                      center=mp.Vector3(),
                                      eig_band=2 if xodd else 1,
                                      eig_kpoint=k_point,
                                      eig_match_freq=False,
                                      eig_parity=mp.ODD_Y)]

    sim.change_sources(eig_sources)


    sim.run(until=100)

    plt.figure(dpi=200)
    sim.plot2D(
        #output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(self.SimSize,self.SimSize)),
        fields=mp.Ey,
        plot_sources_flag=False,
        plot_monitors_flag=False
        )
		#plt.savefig(self.workingDir+"FieldsAtEnd.pdf")
		

    sim.reset_meep()




s = 0.1
parallel_waveguide(s,True)
parallel_waveguide(s,False)
plt.show()