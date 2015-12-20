######################################################
  ######### Aaron J. Juarez, Dec 2 2015 ###########
######################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
font = {'family':'serif', 'size':12}
plt.rc('font', **font)

#### Read in data file and write out to new file
filename='small.in'
newf = open('small-ed.in','w')
with open(filename, 'r') as f:
    content = f.readlines()
    for i in range(5):newf.write(content[i])
    count=0
    for i in range(5,len(content)):
        line = content[i].strip().split()
        if count==0: newf.write(line[0]+'\n'); count+=1
        elif count==1:
            a,e,incl = line[0],line[1],line[2]
            newf.write('%f %s %s\n'%(float(a)*2,e,incl))
            count+=1
        elif count==2:
            g,n,M = line[0],line[1],line[2]
            newf.write('%s %s %s\n'%(g,n,M))
            count+=1
        elif count==3:
            newf.write('0. 0. 0.\n')
            count=0
newf.close()
