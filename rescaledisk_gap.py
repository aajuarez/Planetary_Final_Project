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
a_, e_, incl_, g_, n_, M_ = [],[],[],[],[],[]
with open(filename, 'r') as f:
    content = f.readlines()
    count=0
    for i in range(5,len(content)):
        line = content[i].strip().split()
        if count==0: count+=1
        elif count==1:
            a,e,incl = line[0],line[1],line[2]
            a_.append(a)
            e_.append(e)
            incl_.append(incl)
            count+=1
        elif count==2:
            g,n,M = line[0],line[1],line[2]
            g_.append(g)
            n_.append(n)
            M_.append(M)
            count+=1
        elif count==3: count=0

indz = np.argsort(a_) #smallest to largest
a=np.array(a_)[indz]
e=np.array(e_)[indz]
incl=np.array(incl_)[indz]
g=np.array(g_)[indz]
n=np.array(n_)[indz]
M=np.array(M_)[indz]

#Rgap_in, Rgap_out = 1.8, 2.2 #chaotic res
Rgap_in, Rgap_out = 4.9, 5.5 #planet/disk, test 2
a_, e_, incl_, g_, n_, M_ = [],[],[],[],[],[]
for i in range(len(a)):
    if float(a[i]) < Rgap_in:
        a_.append(a[i])
        e_.append(e[i])
        incl_.append(incl[i])
        g_.append(g[i])
        n_.append(n[i])
        M_.append(M[i])
    elif float(a[i]) > Rgap_out:
        a_.append(a[i])
        e_.append(e[i])
        incl_.append(incl[i])
        g_.append(g[i])
        n_.append(n[i])
        M_.append(M[i])
print len(a_)
#print a_

newf = open('small-ed.in','w')
for i in range(5):newf.write(content[i])
count=0
for i in range(len(a_)):
    newf.write('BODY'+str(i)+'\n'); count+=1
    newf.write('%s %s %s\n'%(a_[i],e_[i],incl_[i]))
    newf.write('%s %s %s\n'%(g_[i],n_[i],M_[i]))
    newf.write('0. 0. 0.\n')
newf.close()
