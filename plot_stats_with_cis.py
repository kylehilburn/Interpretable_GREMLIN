import numpy as np
from matplotlib import pyplot as plt

from get_statistics import refthrs

# Paul Tol's high contrast color scheme
c_gremlin= '#004488'  #blue
c_dense = '#bb5566'  #red
c_linear = '#ddaa33'  #yellow

#####

dss = ['gremlin','dense','linear']
pdata = {}
for ads in dss:
    pdata[ads] = {}
    f = open('stats_'+ads+'.txt','r')
    for aline in f:
        items = [anitem.strip() for anitem in aline.split('=')]
        if items[0] != 'catstats': 
            akey = items[0]
            pdata[ads][akey] = float(items[1])
        else:
            aref,apod,afar,acsi,abias = [float(anitem.strip()) for anitem in items[1].split()]
            pdata[ads]['pod_'+str(int(aref))] = apod
            pdata[ads]['far_'+str(int(aref))] = afar
            pdata[ads]['csi_'+str(int(aref))] = acsi
            pdata[ads]['bias_'+str(int(aref))] = abias
    f.close()

#####

dss = ['gremlin','dense','linear']
cdata = {}
for ads in dss:
    cdata[ads] = {}
    f = open('cis_'+ads+'_10000.txt','r')
    for aline in f:
        items = [anitem.strip() for anitem in aline.split('=')]
        if items[0] != 'catstats':
            akey = items[0]
            lower,upper = [float(anitem) for anitem in items[1].split()]
            cdata[ads][akey] = (lower,upper)
        else:
            aref,pod_lower,pod_upper,far_lower,far_upper,csi_lower,csi_upper,bias_lower,bias_upper = [float(anitem) for anitem in items[1].split()]
            cdata[ads]['pod_'+str(int(aref))] = (pod_lower, pod_upper)
            cdata[ads]['far_'+str(int(aref))] = (far_lower, far_upper)
            cdata[ads]['csi_'+str(int(aref))] = (csi_lower, csi_upper)
            cdata[ads]['bias_'+str(int(aref))] = (bias_lower, bias_upper)
    f.close()

#####

fig = plt.figure(figsize=(6.5,4.5))
fig.subplots_adjust(left=0.10,right=0.96,bottom=0.10,top=0.92,wspace=0.3,hspace=0.4)

plt.subplot(2,2,1)

aval = pdata['gremlin']['pearson_rsq']
alo,ahi = cdata['gremlin']['pearson_rsq']

bval = pdata['dense']['pearson_rsq']
blo,bhi = cdata['dense']['pearson_rsq']

cval = pdata['linear']['pearson_rsq']
clo,chi = cdata['linear']['pearson_rsq']

plt.plot([1,1],[alo,ahi],linestyle='solid',color=c_gremlin)
plt.plot([2,2],[blo,bhi],linestyle='solid',color=c_dense)
plt.plot([3,3],[clo,chi],linestyle='solid',color=c_linear)

plt.plot([1],[aval],marker='o',color=c_gremlin)
plt.plot([2],[bval],marker='o',color=c_dense)
plt.plot([3],[cval],marker='o',color=c_linear)

plt.xticks([1,2,3],['CNN','DENSE','LINEAR'])
plt.ylim([0.72,0.78])

plt.grid()
plt.title('(A) R$^2$')

plt.subplot(2,2,2)

aval = pdata['gremlin']['rmsd']
alo,ahi = cdata['gremlin']['rmsd']

bval = pdata['dense']['rmsd']
blo,bhi = cdata['dense']['rmsd']

cval = pdata['linear']['rmsd']
clo,chi = cdata['linear']['rmsd']

plt.plot([1,1],[alo,ahi],linestyle='solid',color=c_gremlin)
plt.plot([2,2],[blo,bhi],linestyle='solid',color=c_dense)
plt.plot([3,3],[clo,chi],linestyle='solid',color=c_linear)

plt.plot([1],[aval],marker='o',color=c_gremlin)
plt.plot([2],[bval],marker='o',color=c_dense)
plt.plot([3],[cval],marker='o',color=c_linear)

plt.xticks([1,2,3],['CNN','DENSE','LINEAR'])
plt.ylim([5.2,6.2])

plt.grid()
plt.title('(B) RMSD')

plt.subplot(2,2,3)
akey = 'csi'

for aref in refthrs:

    aval = pdata['gremlin'][akey+'_'+str(int(aref))]
    alo,ahi = cdata['gremlin'][akey+'_'+str(int(aref))]

    bval = pdata['dense'][akey+'_'+str(int(aref))]
    blo,bhi = cdata['dense'][akey+'_'+str(int(aref))]

    cval = pdata['linear'][akey+'_'+str(int(aref))]
    clo,chi = cdata['linear'][akey+'_'+str(int(aref))]

    plt.plot([aref-1,aref-1],[alo,ahi],linestyle='solid',color=c_gremlin)
    plt.plot([aref+0,aref+0],[blo,bhi],linestyle='solid',color=c_dense)
    plt.plot([aref+1,aref+1],[clo,chi],linestyle='solid',color=c_linear)

    plt.axvspan(aref-2,aref+2,alpha=0.25,color='gray')

plt.xlabel('Reflectivity (dBZ)')
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55])
plt.ylim([0.0,0.8])
plt.grid()
plt.title('(C) CSI')

plt.subplot(2,2,4)
akey = 'bias'

for aref in refthrs:

    aval = pdata['gremlin'][akey+'_'+str(int(aref))]
    alo,ahi = cdata['gremlin'][akey+'_'+str(int(aref))]

    bval = pdata['dense'][akey+'_'+str(int(aref))]
    blo,bhi = cdata['dense'][akey+'_'+str(int(aref))]

    cval = pdata['linear'][akey+'_'+str(int(aref))]
    clo,chi = cdata['linear'][akey+'_'+str(int(aref))]

    plt.plot([aref-1,aref-1],[alo,ahi],linestyle='solid',color=c_gremlin)
    plt.plot([aref+0,aref+0],[blo,bhi],linestyle='solid',color=c_dense)
    plt.plot([aref+1,aref+1],[clo,chi],linestyle='solid',color=c_linear)

    plt.axvspan(aref-2,aref+2,alpha=0.25,color='gray')

plt.xlabel('Reflectivity (dBZ)')
plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55])
plt.ylim([0.75, 1.33])
plt.yticks([0.75, 0.87, 1, 1.15, 1.33])
plt.grid()
plt.title('(D) BIAS')

figname = 'figure4_stats_with_cis.png'
fig.savefig(figname,dpi=300)
plt.clf()
