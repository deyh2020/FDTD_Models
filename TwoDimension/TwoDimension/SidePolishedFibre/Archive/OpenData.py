import numpy as np 
import pickle
import csv
import matplotlib.pyplot as plt




wd = "data/2022-01-26/Benchmarks/"

filenames = [wd+"Bench.pkl"]


with open(filenames[0],'rb') as file:
    data = pickle.load(file)

for k,v in data.items():
    print(k)

wl = []
Rs = []
Ts = []
for i in range(0,len(data['flux_freqs'])):
    wl = np.append(wl, 1000/data['flux_freqs'][i])
    Ts = np.append(Ts,data['tran_flux'][i]/data['norm_tran'][i])

fig,ax = plt.subplots(dpi=150)

ax.plot(wl,Ts)

plt.savefig(wd+"Transmission.pdf")



"""
with open(wd+'PDMS.csv', 'w', newline='') as csvfile:
    fieldnames = ['Wavelength / um', 'Transmission @ 40C','Transmission @ 65C','Transmission @ 80C']
    writer = csv.writer(csvfile)

    writer.writerow(fieldnames)
    for i in range(0,len(wl)):
        print(i)
        list01 = [wl[i],Ts40[i],Ts65[i],Ts80[i]]
        print(list01)

        writer.writerow( list01 )

"""


