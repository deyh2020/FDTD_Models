import numpy as np 
import pickle
import csv


wd = "data/2022-01-25/1D_PDMS/"

filenames = [wd+"40.pkl",wd+"65.pkl",wd+"80.pkl"]


with open(filenames[0],'rb') as file:
    data = pickle.load(file)


wl = []
Rs = []
Ts40 = []
for i in range(0,len(data['flux_freqs'])):
    wl = np.append(wl, 1000/data['flux_freqs'][i])
    Ts40 = np.append(Ts40,data['tran_flux'][i]/data['norm_tran'][i])

with open(filenames[1],'rb') as file:
    data = pickle.load(file)

wl = []
Rs = []
Ts65 = []
for i in range(0,len(data['flux_freqs'])):
    wl = np.append(wl, 1000/data['flux_freqs'][i])
    Ts65 = np.append(Ts65,data['tran_flux'][i]/data['norm_tran'][i])

with open(filenames[2],'rb') as file:
    data = pickle.load(file)

wl = []
Rs = []
Ts80 = []
for i in range(0,len(data['flux_freqs'])):
    wl = np.append(wl, 1000/data['flux_freqs'][i])
    Ts80 = np.append(Ts80,data['tran_flux'][i]/data['norm_tran'][i])


print(Ts40)

with open(wd+'PDMS.csv', 'w', newline='') as csvfile:
    fieldnames = ['Wavelength / um', 'Transmission @ 40C','Transmission @ 65C','Transmission @ 80C']
    writer = csv.writer(csvfile)

    writer.writerow(fieldnames)
    for i in range(0,len(wl)):
        print(i)
        list01 = [wl[i],Ts40[i],Ts65[i],Ts80[i]]
        print(list01)

        writer.writerow( list01 )


