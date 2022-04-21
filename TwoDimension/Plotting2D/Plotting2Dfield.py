import numpy as np
import matplotlib.pyplot as plt 
import pickle


filename = "../data/2022-04-18/SidePolish_Square2mm/Transmission_dft.pkl"
#filename = "../data/2022-04-20/9umThick/Transmission_dft.pkl"

with (open(filename, "rb")) as openfile:
        data = pickle.load(openfile)


WL = 1000*data['WL']
(x,y,z,w)=data['Location']
n = data['RefractiveIndex']

n = (n - 1.0)**7

print(np.shape(np.abs(data['matrix'])))
print(np.shape(n))

nMatrix = np.zeros(shape=(len(n),len(WL)))
for i in range(0,len(WL)):
        nMatrix[:,i] = n


plt.figure(figsize=(20,10))
plt.imshow(
        np.flipud(nMatrix),
        aspect=0.3, 
        #interpolation="none",
        extent=(WL[0],WL[-1],y[0],y[-1]),
        cmap="Greys",
        alpha=1)

plt.imshow(
        np.abs(data['matrix']),
        aspect=0.3, 
        interpolation="none",
        extent=(WL[0],WL[-1],y[0],y[-1]),
        cmap="Reds",
        alpha=0.7)


plt.show()