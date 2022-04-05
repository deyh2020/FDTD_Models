from locale import RADIXCHAR
import numpy as np
import matplotlib.pyplot as plt
import pickle



def openData(filename,experiments):

    with open(filename,'r') as file:
        data = np.genfromtxt(file,delimiter=',',skip_header=14)


    #experiments = 3     # add this to the saving function
    
    dataDict = {}



    for i in range(0,experiments):
        wl = np.array(data[:,2*i + 1])
        pwr = np.array(data[:,2*(i+1)])

        wl = wl[~np.isnan(pwr)]
        pwr = pwr[~np.isnan(pwr)]

        dataDict['exp_'+str(i+1)] = np.array([wl,pwr])
        
        #print(dataDict['exp_'+str(i)])

    return dataDict




def Normalise(WL,PWR):

    filename = "../../../TunableLaserGUI/data/Christian/2022-03-18/Best1.csv"
    data = openData(filename,1)['exp_1']
    
    normPWR = np.interp(WL,data[0],data[1])

    return normPWR/PWR






plt.figure(figsize=(16,10))

"""Simulaiton Data"""

simdatafile = "../data/2022-03-31/DesktopBench/test.pkl"
with open(simdatafile,"rb") as file:
    data = pickle.load(file)


flux_freqs = data['flux_freqs']
tran_flux  = data['tran_flux']
norm_tran = data['norm_tran']

wl = []
Ts = []
for i in range(len(flux_freqs)):
    
    wl = np.append(wl, 1/flux_freqs[i])
    Ts = np.append(Ts,tran_flux[i]/norm_tran[i])

wl = wl*1000

plt.plot(wl,Ts,label='SimulatonData')
#plt.plot(wl,Ts,'x')


"""Experimental Data"""
experimentalData = "../../../TunableLaserGUI/data/Christian/2022-03-18/Best1.csv"
dataDict = openData(experimentalData,5)
WL  = dataDict['exp_'+str(5)][0]
PWR = dataDict['exp_'+str(5)][1]
normPWR = Normalise(WL,PWR)




plt.plot(WL,normPWR,label='Experimental Data 1, 0.01nm res')



experimentalData = "../../../TunableLaserGUI/data/Christian/2022-03-18/Best2.csv"
dataDict = openData(experimentalData,3)
WL  = dataDict['exp_'+str(2)][0]
PWR = dataDict['exp_'+str(2)][1]
normPWR = Normalise(WL,PWR)




plt.plot(WL,normPWR,label='Experimental Data 2, 1pm res')

experimentalData = "../../../TunableLaserGUI/data/Christian/2022-03-18/Best3.csv"
dataDict = openData(experimentalData,2)
WL  = dataDict['exp_'+str(2)][0]
PWR = dataDict['exp_'+str(2)][1]
normPWR = Normalise(WL,PWR)




plt.plot(WL,normPWR,label='Experimental Data 3, 1pm res')


plt.xlabel("Wavelength / nm",fontsize=16)
plt.ylabel("Normalised Power",fontsize=16)


#print("Simulation Datapoints: "+ str(len(flux_freqs)))
#print("Experimental Datapoints: "+ str(len(WL)))
#print("Simulation DPP1nm: "+ str(len(flux_freqs)/(max(wl)-min(wl))))
#print("Experimental DPP1nm: "+ str(len(WL)/(max(WL)-min(WL))))

#print("dlam: " + str(max(wl)-min(wl)))

plt.savefig("expvssim.pdf")
plt.legend()
plt.show()


"""
filename = "../../../TunableLaserGUI/data/Christian/2022-03-18/Best5.csv"
dataDict = openData(filename,7)


plt.figure(figsize=(16,10))

for i in range(0,7):
    WL  = dataDict['exp_'+str(i+1)][0]
    PWR = dataDict['exp_'+str(i+1)][1]


    normPWR = Normalise(WL,PWR)




    plt.plot(WL,normPWR)

"""


