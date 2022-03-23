import h5py
import numpy as np 
import matplotlib.pyplot as plt


wD = '../data/2022-03-22/test/'

epsf = 'twoDsolve-eps-000000.00.h5'
fieldf = 'twoDsolve-ez-000799.88.h5'


eps = np.flipud(np.transpose(h5py.File(wD + epsf, 'r')['eps']))
field = np.flipud(np.transpose(h5py.File(wD + fieldf, 'r')['ez']))


plt.figure()

plt.imshow(eps,cmap="binary",interpolation="none",vmin=0.00,vmax=np.max(eps))
plt.imshow(field,cmap="bwr",vmin=-np.max(field),vmax=np.max(field),alpha=0.8)

plt.show()