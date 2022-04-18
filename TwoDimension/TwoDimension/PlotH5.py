import h5py
import numpy as np
import matplotlib.pyplot as plt

filename = "../data/2022-04-14/SidePolish_Angled500um/SidePolishedFibre-eps-000000.00.h5"

with h5py.File(filename,'r') as f:    
    eps = np.flipud(np.array(f['eps']).transpose())



plt.imshow(eps)
plt.show()