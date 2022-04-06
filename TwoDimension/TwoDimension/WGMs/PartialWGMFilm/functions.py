import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np 
import sys, os, glob
import time
import sys, os
#sys.path.insert(2,"C:\\Program Files\\Lumerical\\v202\\api\\python\\") 
#import lumapi
def fig_format(ax1,Title,Xlabel,Ylabel,legtitle):
    ax1.set_title(Title,fontsize=18)
    ax1.set_xlabel(Xlabel,fontsize=16)
    ax1.set_ylabel(Ylabel,fontsize=16)
    ax1.grid(b=True, which='major', color='grey', linestyle='-',alpha=0.4)
    ax1.grid(b=True, which='minor', color='grey', linestyle='--',alpha=0.4)
    ax1.minorticks_on()  
    ax1.legend(title=legtitle)
    ax1.ticklabel_format(style='sci',scilimits=(-1,5),axis='both',useOffset=False)
    
def getVal(fdtd,obj,val):
    fdtd.select(obj)
    return fdtd.get(val)

def getFDTD(fdtd):
    shutoff = getVal(fdtd,'FDTD','autoshutoff level')
    return shutoff

def getCirc(fdtd):
    x = getVal(fdtd,'circle','x')
    y = getVal(fdtd,'circle','y')
    rad = getVal(fdtd,'circle','radius')
    return x,y,rad

def getFilm(fdtd):
    x = getVal(fdtd,'ThinFilm1','x')
    y = getVal(fdtd,'ThinFilm1','y')
    xSpan = getVal(fdtd,'ThinFilm1','x span')
    ySpan = getVal(fdtd,'ThinFilm1','y span')
    return x,y,xSpan,ySpan

def setCirc(fdtd,x,y,rad):
    fdtd.switchtolayout()
    fdtd.select('circle')
    fdtd.set('x',x)
    fdtd.set('y',y)
    fdtd.set('radius',rad)
    
def setWG(fdtd,rad):
    fdtd.switchtolayout()
    fdtd.select('rectangle')
    fdtd.set('base width',rad*2.0)
    
def upWGmonitor(fdtd):
    WG = getWG(fdtd)
    width = WG[3]
    fdtd.select('WGfield')
    fdtd.set('y span',width+(width*0.3))
    fdtd.select('source')
    fdtd.set('y span',width+(width*0.3))
    
def upWGMmonitor(fdtd):
    C = getCirc(fdtd)
    y = C[1] + C[2]
    fdtd.select('source_1')
    fdtd.set('y',-y)
    fdtd.select('Stored')
    fdtd.set('y',y)
    fdtd.select('WGMfield')
    fdtd.set('y',y)
    fdtd.set('bend radius',C[2])
    

def getWG(fdtd):
    x = getVal(fdtd,'rectangle','x')
    y = getVal(fdtd,'rectangle','y')
    width = getVal(fdtd,'rectangle','y span') 
    return x,y,width

def getAspect(fdtd):
    x = getVal(fdtd,'Coupling Field','x span')*0.5e6
    y = getVal(fdtd,'Coupling Field','y span')*0.5e6
    return x,y

def getGap(fdtd):
    C = getCirc(fdtd)
    WG = getWG(fdtd)
    return (C[1]-C[2])-(WG[1]+WG[2]/2)

def setGap(fdtd,gap):
    pos = -40.5e-6-gap
    fdtd.switchtolayout()
    fdtd.select("rectangle")
    fdtd.set('y',pos)
    fdtd.select("FDTD::ports::Input_Mode")
    fdtd.set('y',pos)
    fdtd.select("FDTD::ports::WG_Trans_Mode")
    fdtd.set('y',pos)
    fdtd.select("ThinFilm1")
    fdtd.set('y',pos+0.5e-6+0.025e-6)
    fdtd.select("ThinFilm2")
    fdtd.set('y',pos-0.5e-6-0.025e-6)
    
def setSrc(fdtd,x):
    fdtd.switchtolayout()
    fdtd.select("FDTD::ports::Input_Mode")
    fdtd.set("x",x)
    
def getMesh(fdtd):
    WGdx = getVal(fdtd,'meshWG','dx')
    WGdy = getVal(fdtd,'meshWG','dy')
    Cdx = getVal(fdtd,'meshCirc','dx')
    Cdy = getVal(fdtd,'meshCirc','dy')
    return WGdx,WGdy,Cdx,Cdy

def getTimeMesh(fdtd):
    SimT = getVal(fdtd,'FDTD','simulation time')
    WGdy = getVal(fdtd,'FDTD','dt stability factor')
    return SimT,WGdy
    
def setWGMesh(fdtd,mesh):
    mesh = mesh*1e-6
    fdtd.switchtolayout()
    fdtd.select('meshWG')
    fdtd.set('dx',mesh)
    fdtd.set('dy',mesh)
    
def setCircMesh(fdtd,mesh):
    mesh = mesh*1e-6
    fdtd.switchtolayout()
    fdtd.select('meshCirc')
    fdtd.set('dx',mesh)
    fdtd.set('dy',mesh)
    
def setSimTime(fdtd,T): #input in femptoseconds
    T = T*1e-15
    fdtd.switchtolayout()
    fdtd.select('FDTD')
    fdtd.set('simulation time',T)
    
    
def saveData(fdtd,datafile):
    np.savez(datafile + ".npz",
         #x = fdtd.getresult('Coupling Field','x'),
         #y = fdtd.getresult('Coupling Field','y'),
         #P = fdtd.getresult('Coupling Field','P'),
         #E = fdtd.getresult('Coupling Field','E'),
         #H = fdtd.getresult('Coupling Field','H'),
         #Ez = fdtd.getresult('Coupling Field','Ez'),
         #aspect = getAspect(fdtd),
         gap = str(np.round(getGap(fdtd)*1e6,decimals=2)),
         C = getCirc(fdtd),
         WG = getWG(fdtd),
         T = fdtd.getresult('Transmission','T'),
         SpaceMesh = getMesh(fdtd),
         TimeMesh = getTimeMesh(fdtd)
         )
def saveData2(fdtd,datafile):
    np.savez(datafile + ".npz",
         #x = fdtd.getresult('Coupling Field','x'),
         #y = fdtd.getresult('Coupling Field','y'),
         #P = fdtd.getresult('Coupling Field','P'),
         #E = fdtd.getresult('Coupling Field','E'),
         #H = fdtd.getresult('Coupling Field','H'),
         #Ez = fdtd.getresult('Coupling Field','Ez'),
         #aspect = getAspect(fdtd),
         gap = str(np.round(getGap(fdtd)*1e6,decimals=2)),
         C = getCirc(fdtd),
         WG = getWG(fdtd),
         T = fdtd.getresult('Transmission','T'),
         SpaceMesh = getMesh(fdtd),
         TimeMesh = getTimeMesh(fdtd),
         WGfield = fdtd.getresult('WGfield','neff'),
         WGMfield = fdtd.getresult('WGMfield','neff')
         )
          
def saveData3(fdtd,datafile):
    np.savez(datafile + ".npz",
         #x = fdtd.getresult('Coupling Field','x'),
         #y = fdtd.getresult('Coupling Field','y'),
         #P = fdtd.getresult('Coupling Field','P'),
         #E = fdtd.getresult('Coupling Field','E'),
         #H = fdtd.getresult('Coupling Field','H'),
         #Ez = fdtd.getresult('Coupling Field','Ez'),
         #aspect = getAspect(fdtd),
         #gap = str(np.round(getGap(fdtd)*1e6,decimals=2)),
         #C = getCirc(fdtd),
         WG = getWG(fdtd),
         #T = fdtd.getresult('Transmission','T'),
         #SpaceMesh = getMesh(fdtd),
         TimeMesh = getTimeMesh(fdtd),
         #WGfield = fdtd.getresult('WGfield','neff'),
         WGMfield = fdtd.getresult('WGMfield','neff')
         )
        
def printSettings(datafile):
    data = np.load(datafile,allow_pickle=True)
    for i in data:
        print(i)
    
def plotTransmission(datafile,ax):
    data = np.load(datafile,allow_pickle=True)
    T = data['T']
    lam = T.item().get('lambda')
    P = T.item().get('T')
    string = str(os.path.basename(datafile)).strip(".npz") 
    print(len(P))
    ax.plot(lam*1e6,P,label=string)
    
def returnminTransmission(datafile):
    data = np.load(datafile,allow_pickle=True)
    T = data['T']
    P = T.item().get('T')
    return np.min(P)

def returnNEFF(datafile,field):
    data = np.load(datafile,allow_pickle=True)
    WGM = data[str(field)]
    Wl = WGM.item().get('lambda')
    Neff = WGM.item().get('neff')
    return Wl, Neff

    
def plotField(ax,datafile):
    data = np.load(datafile,allow_pickle=True)
    x = data['x']
    y = data['y']
    Field = data['Field']
    C = data['C']
    aspect = data['aspect']
    WG = data['WG']
    gap = data['gap']
    
    Circle1 = plt.Circle((C[0],C[1]),C[2],color='r',fill=False)
    Circle2 = plt.Circle((C[0],C[1]),C[2],color='r',fill=False)

   
    x1 = WG[0] - WG[2]/2
    y1 = WG[1] - WG[3]/2
    WG1 = patches.Rectangle((x1,y1),WG[2],WG[3],linewidth=1,edgecolor='r',facecolor='none')
    WG2 = patches.Rectangle((x1,y1),WG[2],WG[3],linewidth=1,edgecolor='r',facecolor='none')

    Ez = Field[:,:,0,0]

    #ax.contourf(x[:,0],y[:,0],np.transpose(Ez),contours)
    ex = np.array([min(x)[0],max(x)[0],min(y)[0],max(y)[0]])
    #print(ex)
    ax.imshow(np.flip(np.transpose(np.real(Ez)),axis=0),extent=ex)
    ax.add_artist(Circle1)
    ax.autoscale(False)
    ax.add_patch(WG1)
    string = "Gap: " + str(data['gap']) + "um "
    ax.set_title(string,fontsize=20)


