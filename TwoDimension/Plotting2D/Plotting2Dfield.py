import numpy as np
import matplotlib.pyplot as plt 
import pickle


filename = "../data/EasterTime/LaptopDebug/WGMdft.pkl"

with (open(filename, "rb")) as openfile:
        matrix = pickle.load(openfile)


plt.figure(figsize=(16,10))
plt.imshow(np.abs(matrix),aspect=100, interpolation="none")
plt.show()