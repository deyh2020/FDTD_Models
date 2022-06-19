import numpy as np
import matplotlib.pyplot as plt
import h5py


wD = "../data/2022-06-13/test_ModeSolving/"


#f = h5py.File(wD + "CWsolve-Air.h5",'r')

fig,axes = plt.subplots(1,2,dpi=200)

eps    = ['NaseemFibre-eps-000000.00.h5']
fields = ['NaseemFibre-ey-000000.00.h5']


for i in [0]:

    epsf = np.flip( np.transpose( np.array( h5py.File(wD + eps[i],'r')['eps'] ) ),0 )
    epsf = (epsf - 1.00)**15

    #fields =  np.array(h5py.File(wD + fields[i],'r')['ey.r'])
    fields = h5py.File(wD + fields[i],'r')['ey.r']
    print(fields)    
    #axes[i].imshow(epsf,cmap="binary",interpolation="none",vmin=0.00,vmax=np.max(epsf))
    axes[i].imshow(fields,interpolation="none")


plt.show()


""" 


workingDir = "data/2022-01-24/ModelTrio/"

filename = ['AirCoatedYfield.png','PDMSCoatedYfield.png']


epsimage =   plt.imread(workingDir+"EPS.png")
fieldimage = plt.imread(workingDir+filename[0])

axes[0].imshow(fieldimage,extent=(-10,10,-10,10))
axes[0].imshow(epsimage,alpha=0.5,extent=(-10,10,-10,10))

axes[0].set_xlabel("X / um")
axes[0].set_ylabel("")


epsimage =   plt.imread(workingDir+"EPS.png")
fieldimage = plt.imread(workingDir+filename[1])

axes[1].imshow(fieldimage,extent=(-10,10,-10,10))
axes[1].imshow(epsimage,alpha=0.35,extent=(-10,10,-10,10))

axes[1].set_xlabel("X / um")
axes[1].set_ylabel("")
#axes[0].set_title("a)")
#axes[1].set_title("b)")


fig.text(0.03, 0.5, 'Y / um', va='center', rotation='vertical')
fig.text(0.145, 0.7, 'a)', va='center', rotation='horizontal')
fig.text(0.57, 0.7, 'b)', va='center', rotation='horizontal')

axes[1].set_yticks([])

plt.savefig(workingDir+"ModeProfiles" +".pdf")
#plt.show() """