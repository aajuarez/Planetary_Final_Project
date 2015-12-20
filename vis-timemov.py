##########################################################
########### Aaron J. Juarez, Dec 06--09, 2015 ############
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

#nom=findfiles('BODY*.aei', project) #list of paths to disk particle files
nom=findfiles('*.aei', project) #list of paths to *.aei files
#nomsel = np.random.choice(nom,70) #randomly choose N bodies
#nom=findfiles('_*', project) #choose only big bodies b and c
#for i in range(len(nomsel)):nom.append(nomsel[i])
tnom = [cz.magma, cz.viridis]
colnom=tnom[0]

##################################################################
### MOVIE IMAGES :: t,x,y,z ;; WARNING: this can be very slow

data=np.genfromtxt(nom[0],dtype=None,skiprows=4,names=namez,unpack=1)
t0=data['t']
t0=np.linspace(0,1000,11)
tcol = np.linspace(0,1,len(t0)); print 'time stamps:', len(t0)
#    if j<=1: colnom = tnom[j]; sz=3
#    else: colnom = cm.binary_r; sz=1
for k in range(len(t0)):
    print k
    fig = plt.figure(figsize=(8,8))
    ptrack=fig.gca(projection='3d')
    #plt.gca().patch.set_facecolor('white')
    bk=0.7
    ptrack.w_xaxis.set_pane_color((bk, bk, bk, 1.0))
    ptrack.w_yaxis.set_pane_color((bk, bk, bk, 1.0))
    ptrack.w_zaxis.set_pane_color((bk, bk, bk, 1.0))
#    ptrack.set_xlim([-0.02,0.02])
#    ptrack.set_ylim([-0.02,0.02])
#    ptrack.set_zlim([-0.02,0.02])
    ptrack.set_xlim([-12,12])
    ptrack.set_ylim([-12,12])
    ptrack.set_zlim([-0.7,0.7])
    sz=9; lw=1
    ptrack.text2D(0.05, 0.95, r'$t=%d\ \rm years$'%round(t0[k]),
                  transform=ptrack.transAxes)
    for j in range(len(nom)):
#        if project=='GalileanSatellites_output':
        with open(nom[j], 'r') as f: content = f.readlines()
        if len(content)==5: continue
        elif project[0:10]=='PlanetDisk':
            if nom[j]==project+'/JUPITER.aei' or\
                nom[j]==project+'/JUPx10.aei' or\
                nom[j]==project+'/SatJx10.aei':
                    sz=120; colnom=cz.viridis
            else: sz=7; colnom=cz.inferno
        data=np.genfromtxt(nom[j],dtype=None,skiprows=4,names=namez,unpack=1)
        t=data['t']; x=data['x']; y=data['y']; z=data['z']
        t_ind=np.where(t==t0[k])[0]
#        print t0[k], t_ind
        ptrack.scatter(x[t_ind],y[t_ind],z[t_ind],c=colnom(tcol[5]),lw=0,s=sz)
#        ptrack.plot([x[t_ind],x[t_ind+1]],[y[t_ind],y[t_ind+1]],
#                    [z[t_ind],z[t_ind+1]],'ko-',
#                    c=colnom(tcol[k]),lw=0.8,mew=0,ms=sz)
    ptrack.view_init(elev=12., azim=40)
    plt.tight_layout()
#    plt.savefig("movie-SolSys-%i"%(t0[k])
    plt.savefig("movie-PlanetDisk-%i"%(round(t0[k]))
                    +".png",transparent=0,frameon=0,dpi=200)
    plt.close()

'''
for iview in xrange(0,360,15):
        print iview
        ptrack.view_init(elev=15., azim=iview)
        plt.tight_layout()
        plt.savefig("movie-GalSat-%i"%(iview)
                        +".png",transparent=0,frameon=0,dpi=200)
exit()
#'''
