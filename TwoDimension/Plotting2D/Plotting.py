import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.signal import find_peaks


SolidCore = "/home/chriscrossing/Nextcloud/Documents/Work/PhD/GIT_Repos/FDTD_Models/TwoDimension/data/2022-04-14/SolidCore/Data.pkl"
ThreeumWall   = "/home/chriscrossing/Nextcloud/Documents/Work/PhD/GIT_Repos/FDTD_Models/TwoDimension/data/2022-04-14/3umThick/Data.pkl"
SixumWall   = "/home/chriscrossing/Nextcloud/Documents/Work/PhD/GIT_Repos/FDTD_Models/TwoDimension/data/2022-04-14/6umThick/Data.pkl"
NineumWall   = "/home/chriscrossing/Nextcloud/Documents/Work/PhD/GIT_Repos/FDTD_Models/TwoDimension/data/2022-04-14/9umThick/Data.pkl"

objects = []


def openSimData(filename):

    with (open(filename, "rb")) as openfile:
        data = pickle.load(openfile)
    wl = (1/np.array(data['flux_freqs']))*1e3
    pwr = np.array(data['tran_flux'])/np.array(data['norm_tran']) 
    
    findPeaksPWR = (-pwr) + 1
       
    peaks, _ = find_peaks(findPeaksPWR, height=0.2)
       
    return wl, pwr, peaks



wl1,pwrSolid, peaks       = openSimData(SolidCore)
#print(wl1[peaks])
wl3,pwr6um,peaks        = openSimData(SixumWall)
#print(wl3[peaks])
wl4,pwr9um,peaks          = openSimData(NineumWall)
#print(wl4[peaks])
wl2,pwr3um, peaks       = openSimData(ThreeumWall)
print(wl2[peaks])



plt.plot(wl1,pwrSolid,label="Solid Core")
##plt.plot(wl1[peaks],pwrSolid[peaks],'x')
plt.plot(wl4,pwr9um,label="9um Wall")
##plt.plot(wl4[peaks],pwr9um[peaks],'x')
plt.plot(wl3,pwr6um,label="6um Wall")
##plt.plot(wl3[peaks],pwr6um[peaks],'x')
plt.plot(wl2,pwr3um,label="3um Wall")
##plt.plot(wl2[peaks],pwr3um[peaks],'x')
plt.xlim(1522,1538)

plt.legend()
plt.xlabel("Wavelength / nm",fontsize=16)
plt.ylabel("Normalised Power",fontsize=16)
plt.show()