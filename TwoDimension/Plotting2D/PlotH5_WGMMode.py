import h5py
import numpy as np
import matplotlib.pyplot as plt

filename = "../data/EasterTime/LaptopDebug/WGMdft.h5"

with h5py.File(filename,'r') as f:    
    for k,v in f.items():
        print(k,v)
   
   
   
