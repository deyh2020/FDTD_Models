import numpy as np
import matplotlib.pyplot as plt
import Model as M

Model = M.Model()

PDMSt = Model.PDMStemp
nPDMS = Model.nPDMS

t = Model.Silicatemp
n = Model.nSilica

fit = np.polyfit(t,n,deg=2)
tnew = np.linspace(t.min(),t.max(),100)
nnew = np.polyval(fit,tnew)

fitPDMS = np.polyfit(PDMSt,nPDMS,deg=2)
nPDMSnew = np.polyval(fitPDMS,tnew)

fig,ax = plt.subplots(dpi=150)


#ax.plot(t,n)
#ax.plot(tnew,nnew)
ax.plot(PDMSt,nPDMS)
ax.plot(tnew,nPDMSnew)

plt.show()