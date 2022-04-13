import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.signal import find_peaks



ExpData   = "/home/chriscrossing/Nextcloud/Documents/Work/PhD/GIT_Repos/FDTD_Models/TwoDimension/data/2022-04-12/ExperimentalDimentions/test.pkl"
SolidCore = "/home/chriscrossing/Nextcloud/Documents/Work/PhD/GIT_Repos/FDTD_Models/TwoDimension/data/2022-04-12/SolidCore/test.pkl"
ThreeumWall   = "/home/chriscrossing/Nextcloud/Documents/Work/PhD/GIT_Repos/FDTD_Models/TwoDimension/data/2022-04-12/3umThick/test.pkl"

objects = []


def openSimData(filename):

    with (open(filename, "rb")) as openfile:
        data = pickle.load(openfile)
    wl = (1/np.array(data['flux_freqs']))*1e3
    pwr = np.array(data['tran_flux'])/np.array(data['norm_tran']) 
    
    findPeaksPWR = (-pwr) + 1
       
    peaks, _ = find_peaks(findPeaksPWR, height=0.2)
       
    return wl, pwr, peaks




wl,pwrExp,peaks          = openData(ExpData)
wl,pwrSolid,peaks        = openData(SolidCore)
wl,pwrThreeumWall,peaks  = openData(ThreeumWall)

print(wl[peaks])

plt.plot(wl,pwrExp,label="Experimental Dimentions")
plt.plot(wl,pwrSolid,label="Solid fibre cylinder")
plt.plot(wl,pwrThreeumWall,label="3um Capillary Wall")
plt.legend()
plt.xlabel("Wavelength / nm",fontsize=16)
plt.ylabel("Normalised Power",fontsize=16)
plt.show()