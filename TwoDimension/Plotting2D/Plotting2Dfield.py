import numpy as np
import matplotlib.pyplot as plt 
import pickle

WD = "../data/2022-04-19/SidePolish_Square500um/"
fieldFname = WD + "Transmissiondft.pkl"
#filename = "../data/2022-04-20/6umThick/Transmission_dft.pkl"
transFname = WD + "Data.pkl"

with (open(fieldFname, "rb")) as openfile:
        field = pickle.load(openfile)

with (open(transFname, "rb")) as openfile:
        Transmission = pickle.load(openfile)





fig,ax = plt.subplots(2,1,figsize=(20,10))

wl = 1/np.array(Transmission['flux_freqs'])



tran_flux = np.array(Transmission['tran_flux'])
norm_tran = np.array(Transmission['norm_tran'])

pwr = tran_flux/norm_tran

ax[0].plot(wl*1000,pwr)

ax[0].set_title("3um Thick Walls",fontsize=16)

ax[0].set_ylabel("Un-normalised PWR",fontsize=16)

WL = 1000*field['WL']
(x,y,z,w)=field['Location']
n = field['RefractiveIndex']

ax[0].set_xlim(min(WL),max(WL))


n = (n - 1.0)**7

nMatrix = np.zeros(shape=(len(n),len(WL)))
for i in range(0,len(WL)):
        nMatrix[:,i] = n


ax[1].set_ylabel("Monitor Position Y / um",fontsize=16)
ax[1].set_xlabel("Wavelength / nm",fontsize=16)


ax[1].imshow(
        np.flipud(nMatrix),
        aspect=0.3, 
        #interpolation="none",
        extent=(WL[0],WL[-1],y[0],y[-1]),
        cmap="Greys",
        alpha=1)

ax[1].imshow(
        np.abs(field['matrix']),
        aspect=0.3, 
        interpolation="none",
        extent=(WL[0],WL[-1],y[0],y[-1]),
        cmap="Reds",
        alpha=0.7)





plt.savefig(WD+"Fields.pdf",dpi=400)
plt.show()