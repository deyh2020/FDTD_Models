import numpy as np
import matplotlib.pyplot as plt 
import pickle

WD = "../data/2022-04-20/6umThick/"
fieldFname = WD + "WGM_dft.pkl"
spectrumFname = WD + "Data.pkl"
#filename = "../data/2022-04-20/9umThick/Transmission_dft.pkl"

"""
Transmission spectrum data manipulation
"""
        
with open(spectrumFname, "rb") as openfile:
    spectrum = pickle.load(openfile)

for k,v in spectrum.items():
    print(k)

wl = []
Ts = []

wl = 1/np.array(spectrum['flux_freqs'])
norm = np.array(spectrum['norm_tran'])
pwr = np.array(spectrum['tran_flux'])

print(len(wl))
print(len(pwr))
   

"""
Field Data manipulation
"""
with (open(fieldFname, "rb")) as openfile:
        field = pickle.load(openfile)

WL = 1000*field['WL']
(x,y,z,w)=field['Location']
n = field['RefractiveIndex']

n = (n - 1.0)**7

nMatrix = np.zeros(shape=(len(n),len(WL)))
for i in range(0,len(WL)):
        nMatrix[:,i] = n


fig, ax = plt.subplots(2,1,figsize=(20,10))


#ax[0].plot(wl,pwr)
ax[0].plot(wl*1000,pwr/norm)


ax[1].imshow(
        np.flipud(nMatrix),
        aspect=0.1, 
        #interpolation="none",
        extent=(WL[0],WL[-1],y[0],y[-1]),
        cmap="Greys",
        alpha=1)

ax[1].imshow(
        np.abs(field['matrix']),
        aspect=0.1, 
        interpolation="none",
        extent=(WL[0],WL[-1],y[0],y[-1]),
        cmap="binary",
        alpha=0.7)

ax[0].set_title("6um Wall Thickness: Transmission Spectrum",fontsize=16)
ax[1].set_title("WGM mode monitor",fontsize=16)


ax[0].set_xlim(1530,1536)
ax[1].set_xlim(1530,1536)


plt.savefig(WD+"Fields.pdf",dpi=400)
plt.show()