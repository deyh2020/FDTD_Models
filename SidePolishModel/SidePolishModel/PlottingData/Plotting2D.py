import numpy as np
import matplotlib.pyplot as plt
import csv, pickle



def plotEXP(self):
    filename = "../data/Experimental/FPRS without PDMS coated/0_5.csv"
    wlLine = 14
    pwrLine = 15

    

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        line = 0
        for row in spamreader:
            #print(line)
            if line == wlLine:
                wl = np.array(row,dtype=float)

            if line == pwrLine:
                Ts = np.array(row,dtype=float)  
                
                            
            line += 1 
    
    
    ax2 = self.M.axes.twinx()
    
    color = 'tab:red'
    ax2.plot(wl,Ts,color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylabel('db', color=color)

def myFFT(t,v):
    N = len(t) # samples

    T = t[-1]/N # sample spacing

    xf = np.fft.fftfreq(N, T)[:N//2]
    yf = 2.0/N * np.abs( np.fft.fft(v)[0:N//2] )

    return 1/xf,yf


"""
Open Data
"""

oneDdata = "../../data/2022-03-16/Mode2Exp_1Dmodel/All.pkl"

twoD2mm   = "../../data/2022-03-14/2mm_SquareDips/data.pkl"
twoD1mm   = "../../data/2022-03-14/1mm_SquareDips/data.pkl"
twoD500um  = "../../data/2022-03-14/500um_SquareDips/data.pkl"


with open(oneDdata, 'rb') as file:
    data = pickle.load(file)


for k,v in data.items():
    print(k)


flux_freqs = np.array(data['flux_freqs'])
refl_flux  = np.array(data['refl_flux'])
norm_tran  = np.array(data['norm_tran'])
tran_flux  = np.array(data['tran_flux'])

nfreq = len(flux_freqs)



wl = []
Rs = []
Ts = []
for i in range(nfreq):
    wl = np.append(wl, 1/flux_freqs[i])
    Rs = np.append(Rs,-refl_flux[i]/norm_tran[i])
    Ts = np.append(Ts,tran_flux[i]/norm_tran[i])



wl = wl*1000

z = np.polyfit(wl,Ts,3)
TsFIT = 0#np.polyval(z,wl)

xf,yf = myFFT(wl,Ts-TsFIT)

plt.figure()
#plt.plot(wl,Rs,'--',label='reflectance')
plt.plot(wl,Ts,label='transmittance')
#plt.plot(wl,TsFIT)
#plt.plot(wl,1-Rs-Ts,label='loss')
#plt.axis([5.0, 10.0, 0, 1])
plt.xlabel("wavelength (μm)")


plt.figure()
plt.plot(xf,yf)
plt.xlim(0,25)


plt.show()

