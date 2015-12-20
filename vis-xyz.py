##########################################################
########### Aaron J. Juarez, Dec 01--05, 2015 ############
##########################################################
import numpy as np
import os, fnmatch
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import colormaps as cz
font = {'family':'serif', 'size':12}
plt.rc('font', **font)

def findfiles(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

#project='GalileanSatellites_output'
#namez=['t','a','e','incl','peri','node','M','mass','x','y','z']
#project='SolarSystem_output'
#namez=['t','long','M','a','e','incl','peri','node','mass','x','y','z']
#project='ChaoticResonance_out_xyz'
#namez=['t','x','y','z']
#project='ChaoticResonance_out_0'
#project='ChaoticResonance_out_1'
#project='ChaoticResonance_out_2'
#project='PlanetDisk_out_0'
project='PlanetDisk_out_1'
#project='PlanetDisk_out_2-0'
#project='PlanetDisk_out_2-1'
#project='PlanetDisk_out_2-2'
#project='PlanetDisk_out_3-100y'
#project='PlanetDisk_out_3-2'
#project='PlanetDisk_out_4'
namez=['t','a','e','incl','M','f','peri','node','mass','x','y','z']

##################################################################
def dxdt(time,param):
    xp = []
    for i in range(len(time)-1):
        xp.append((param[i+1]-param[i])/(time[i+1]-time[i]))
    return np.array(xp)

def param_prime(fname):
    data=np.genfromtxt(fname,dtype=None,skiprows=4,names=namez,unpack=1)
    M=data['M']; f_ta=data['f']; peri=data['peri']; node=data['node']
    varpi = peri+node
    lam = M + varpi
    return lam, varpi

nom=findfiles('BODY*.aei', project) #list of paths to disk particle files
nomsel = np.random.choice(nom,70) #randomly choose N bodies
#nom=findfiles('_*', project) #choose only big bodies b and c
nom=findfiles('JUP*', project) #choose only Jupiter body
for i in range(len(nomsel)):nom.append(nomsel[i])
nom=findfiles('*.aei', project) #list of paths to *.aei files
tnom = [cz.magma, cz.viridis]
colnom=tnom[0]

##################################################################
### SNAP SHOTS :: first, last
#'''
time,xarr,yarr,zarr=[],[],[],[]
col=np.linspace(0,1,len(nom))
for j in range(len(nom)):
#    if project=='GalileanSatellites_output':
    with open(nom[j], 'r') as f: content = f.readlines()
    if len(content)==5: continue
    print j, nom[j]
    data=np.genfromtxt(nom[j],dtype=None,skiprows=4,names=namez,unpack=1)
    t=data['t']; x=data['x']; y=data['y']; z=data['z']
    time.append([t[0],t[-1]])
    xarr.append([x[0],x[-1]])
    yarr.append([y[0],y[-1]])
    zarr.append([z[0],z[-1]])

colnom=tnom[0]
fig = plt.figure(figsize=(8,10))
f=fig.add_subplot(211,axisbg='0.57',aspect=1)
g=fig.add_subplot(212,axisbg='0.57')
for i in range(len(time)):
    if i!=len(time)-1:
        f.plot(xarr[i][0],yarr[i][0],'o',c=cm.binary_r(0.2),mew=0)
        g.plot(xarr[i][0],zarr[i][0],'o',c=cm.binary_r(0.2),mew=0)
    else:
        f.plot(xarr[i][0],yarr[i][0],'o',c=colnom(0.2),mew=0,ms=20)
        g.plot(xarr[i][0],zarr[i][0],'o',c=colnom(0.2),mew=0,ms=20)

f.set_xlabel(r'$X\ [\rm AU]$',size=16)
f.set_ylabel(r'$Y\ [\rm AU]$',size=16)
g.set_xlabel(r'$X\ [\rm AU]$',size=16)
g.set_ylabel(r'$Z\ [\rm AU]$',size=16)
plt.tight_layout()
plt.savefig('xyz-first.png',dpi=300)

fig = plt.figure(figsize=(8,10))
f=fig.add_subplot(211,axisbg='0.57',aspect=1)
g=fig.add_subplot(212,axisbg='0.57')
for i in range(len(time)):
    if i!=len(time)-1:
        f.plot(xarr[i][1],yarr[i][1],'o',c=cm.binary_r(0.2),mew=0)
        g.plot(xarr[i][1],zarr[i][1],'o',c=cm.binary_r(0.2),mew=0)
    else:
        f.plot(xarr[i][1],yarr[i][1],'o',c=colnom(0.2),mew=0,ms=20)
        g.plot(xarr[i][1],zarr[i][1],'o',c=colnom(0.2),mew=0,ms=20)
f.set_xlabel(r'$X\ [\rm AU]$',size=16)
f.set_ylabel(r'$Y\ [\rm AU]$',size=16)
g.set_xlabel(r'$X\ [\rm AU]$',size=16)
g.set_ylabel(r'$Z\ [\rm AU]$',size=16)
plt.tight_layout()
plt.savefig('xyz-last.png',dpi=300)
#exit()
##################################################################
### MOVIE IMAGES :: first, last
fig = plt.figure(figsize=(8,8)); g=fig.gca(projection='3d')
for i in range(len(time)):
    if i!=len(time)-1:
        g.scatter(xarr[i][0],yarr[i][0],zarr[i][0],'o',s=7,
                  c=colnom(0.2),lw=0,alpha=0.64)
    else:
        g.scatter(xarr[i][0],yarr[i][0],zarr[i][0],'o',s=120,
                  c=tnom[1](0.2),lw=0,alpha=1)
g.set_xlabel('$X$',size=16)
g.set_ylabel('$Y$',size=16)
g.set_zlabel('$Z$',size=16)
g.view_init(elev=15., azim=45)
plt.tight_layout()
plt.savefig('pos-first.png',dpi=300)

fig = plt.figure(figsize=(8,8)); h=fig.gca(projection='3d')
for i in range(len(time)):
    if i!=len(time)-1:
        h.scatter(xarr[i][1],yarr[i][1],zarr[i][1],'o',s=7,
                  c=colnom(0.8),lw=0,alpha=0.64)
    else:
        h.scatter(xarr[i][1],yarr[i][1],zarr[i][1],'o',s=120,
                  c=tnom[1](0.8),lw=0,alpha=1)
h.set_xlabel('$X$',size=16)
h.set_ylabel('$Y$',size=16)
h.set_zlabel('$Z$',size=16)
h.view_init(elev=15., azim=45)
plt.tight_layout()
plt.savefig('pos-last.png',dpi=300)
#'''
##################################################################
### MOVIE IMAGES :: t,x,y,z ;; WARNING: this can be very slow
'''
fig = plt.figure(figsize=(8,8))
ptrack=fig.gca(projection='3d')
#plt.gca().patch.set_facecolor('white')
bk=0.7
ptrack.w_xaxis.set_pane_color((bk, bk, bk, 1.0))
ptrack.w_yaxis.set_pane_color((bk, bk, bk, 1.0))
ptrack.w_zaxis.set_pane_color((bk, bk, bk, 1.0))
sz=4; lw=1
for j in range(len(nom)):
#    if project=='GalileanSatellites_output':
    with open(nom[j], 'r') as f: content = f.readlines()
    if len(content)==5: continue
    print j, nom[j]
    data=np.genfromtxt(nom[j],dtype=None,skiprows=4,names=namez,unpack=1)
    t=data['t']; x=data['x']; y=data['y']; z=data['z']
    tcol = np.linspace(0,1,len(x))
#### switch for 2 planets/disk
#    if j<=1: colnom = tnom[j]; sz=3
#    else: colnom = cm.binary_r; sz=1
#### switch for planet/disk
    if j!=0:colnom=cz.viridis;sz=4
    else: colnom=cz.magma;sz=120
    for k in range(len(x)-1):
        ptrack.scatter(x[k],y[k],z[k],c=colnom(tcol[k]),lw=0,s=sz)
#        ptrack.plot([x[k],x[k+1]],[y[k],y[k+1]],[z[k],z[k+1]],
#                    c=colnom(tcol[k]),lw=0.8,mew=0,ms=sz)

for iview in xrange(0,360,15):
        print iview
        ptrack.view_init(elev=15., azim=iview)
        plt.tight_layout()
#        plt.savefig("movie-SolarSys-%i"%(iview)
        plt.savefig("movie-PlanetDisk-%i"%(iview)
                        +".png",transparent=0,frameon=0,dpi=200)
exit()
#'''
##################################################################
#plt.show()#WARNING: use for small data sets, huge data -> super slow
