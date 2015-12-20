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

#project=['GalileanSatellites_output']
#namez=['t','a','e','incl','peri','node','M','mass']
#project='SolarSystem_output'
#namez=['t','long','M','a','e','incl','peri','node','mass']
#project='ChaoticResonance_out_xyz'
#namez=['t','x','y','z']
#project='ChaoticResonance_out_0'
#project='ChaoticResonance_out_1'
#project='PlanetDisk_out_0'
project='PlanetDisk_out_1'
namez=['t','a','e','incl','M','f','peri','node','mass','x','y','z']
#project='PlanetDisk_out_4'
#namez=['t','e','incl','M','f','peri','node','mass','x','y','z']

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

#nom=findfiles('*.aei', project) #list of paths to *.aei files
nom=findfiles('BODY*.aei', project) #list of paths to disk particle files
nomsel = np.random.choice(nom,70) #randomly choose N bodies
#nom=findfiles('_*', project) #disk/planets: choose only big bodies b and c
nom=findfiles('JUP*.aei', project) #disk/planets: choose only Jupiter body
#nom=findfiles('Sat*.aei', project)
#lam_b,varpi_b=param_prime(nom[0])
#lam_c,varpi_c=param_prime(nom[1])
for i in range(len(nomsel)):nom.append(nomsel[i])
tnom = [cz.magma, cz.viridis]

##################################################################
#'''
fig = plt.figure(figsize=(16,9)) #3x2
f=fig.add_subplot(321,axisbg='0.57')
g=fig.add_subplot(323,axisbg='0.57')
h=fig.add_subplot(325,axisbg='0.57')
f1=fig.add_subplot(322,axisbg='0.57')
g1=fig.add_subplot(324,axisbg='0.57')
h1=fig.add_subplot(326,axisbg='0.57')
time,xarr,yarr,zarr=[],[],[],[]
col=np.linspace(0,1,len(nom))
for j in range(len(nom)):
        with open(nom[j], 'r') as f_: content = f_.readlines()
        if len(content)==5: continue
        print j, nom[j]
        data=np.genfromtxt(nom[j],dtype=None,skiprows=4,names=namez,unpack=1,)
#                           usecols=[0,2,3,4,5,6,7,8,9,10,11])
###!!! missing values won't work here, maybe pandas would work better!
        t=data['t']
        colnom = tnom[0]; sz=0.8; lw=0.4
#        lam_x = lam_b; varpi_x = varpi_b
######## Switch for 2 planets and disk parameters
#        if j<=1:
#            colnom = tnom[j]; sz=2.5; lw=1.5
#            if j==0:   lam_x = lam_c; varpi_x = varpi_c
#            elif j==1: lam_x = lam_b; varpi_x = varpi_b
#        else: colnom = cz.plasma; sz=0.8; lw=0.4
######## Switch for planet and disk parameters
        if nom[j]==project+'/JUPITER.aei' or\
            nom[j]==project+'/SatJx10.aei': colnom=cz.viridis; sz=2.5; lw=4
        else: colnom = cz.magma; sz=0.8; lw=0.4
######## Params for asteroidal / cometary
        a=data['a']
        mass = data['mass']; mass -= mass[0]
        e = data['e']; incl=data['incl']
        M=data['M']; peri=data['peri'];node=data['node']
        f_ta=data['f']
#        varpi = peri+node
#        lam = M + varpi
#        phi = 2*lam_x - lam - varpi
#        psi = 2*lam_x - lam - varpi_x
#        corr = 0>phi; print len(corr1)
#        phi[corr]+= 360*3
#        corr = phi>360; print len(corr1)
#        phi[corr]-= 360
#        corr = 0>psi
#        psi[corr]+=360

        l__=f.plot(t,a,'k-',c=colnom(col[j]),mew=0,lw=lw)
#        l__=f.plot(t,f_ta,'k-',c=colnom(col[j]),mew=0,lw=lw)
        l__[0].set_clip_on(False)
        l__=g.plot(t,e,'k-',c=colnom(col[j]),mew=0,lw=lw)
        l__[0].set_clip_on(False)
        l__=h.plot(t,incl,'k-',c=colnom(col[j]),mew=0,lw=lw)
        l__[0].set_clip_on(False)

#        l__=f1.plot(t,M,'k-',c=colnom(col[j]),mew=0,lw=lw)
#        l__=f1.plot(t,M,'ko',c=colnom(col[j]),mew=0,ms=sz)
#        l__=f1.plot(t,phi,'ko',c=colnom(col[j]),mew=0,ms=sz)
        l__=f1.plot(t,f_ta,'k-',c=colnom(col[j]),mew=0,lw=lw)
        l__[0].set_clip_on(False)
        l__=g1.plot(t,node,'k-',c=colnom(col[j]),mew=0,lw=lw)
#       l__=g1.plot(t,f_ta,'ko',c=colnom(col[j]),mew=0,ms=sz)
#        l__=g1.plot(t,psi,'ko',c=colnom(col[j]),mew=0,ms=sz)
        l__[0].set_clip_on(False)
        l__=h1.plot(t,peri,'k-',c=colnom(col[j]),mew=0,lw=lw)
#        l__=h1.plot(t,peri,'ko',c=colnom(col[j]),mew=0,ms=sz)
        l__[0].set_clip_on(False)

h.set_xlabel(r'$t\ [\rm years]$',size=16)
f.set_ylabel(r'$a\ [\rm AU]$',size=16)
#f.set_ylabel(r'$m\ [M_\odot]$',size=16)
#f.set_ylabel(r'$f\ [\rm deg]$',size=16)
g.set_ylabel(r'$e$',size=16)
h.set_ylabel(r'$i\ [\rm deg]$',size=16)
h1.set_xlabel(r'$t\ [\rm years]$',size=16)
#f1.set_ylabel(r'$M\ [\rm deg]$',size=16)
#f1.set_ylabel(r'$\phi\ [\rm deg]$',size=16)
f1.set_ylabel(r'$f\ [\rm deg]$',size=16)
g1.set_ylabel(r'$\Omega\ [\rm deg]$',size=16)
#g1.set_ylabel(r'$f\ [\rm deg]$',size=16)
#g1.set_ylabel(r'$\psi\ [\rm deg]$',size=16)
h1.set_ylabel(r'$\omega\ [\rm deg]$',size=16)
for i in [f1,g1,h1]: #for parameters w/ 360 deg range
    i.set_yticks(np.arange(0,360+60,60))
    i.set_ylim([0,360])

plt.tight_layout()
#plt.savefig('new.pdf')
plt.savefig('orbels.png',dpi=300)
#'''
#print time[0],'year integration'
#plt.show()#WARNING: use for small data sets, huge data -> super slow
