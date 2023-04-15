import numpy as np
from matplotlib import pyplot as plt
from string import ascii_lowercase

from read_bin_avgs import read_bin_avgs

#####

thelev = 'L0'
datasets = ['data','gremlin','dense','linear']
colors = {'data':'black', 'gremlin':'#004488', 'dense':'#bb5566', 'linear':'#ddaa33'}
lw = {'data':2, 'gremlin':1, 'dense':1, 'linear':1}

#####

cnt_data = {}
tot_data = {}

for ads in datasets:

    data = read_bin_avgs('bin_avgs_'+ads+'.bin')

    xbins = data['xbins']
    cnt_data[ads] = data['cnt1d']
    tot_data[ads] = data['tot1d']

#####

levs = ['L0','L1','L2','L3']
chans = ['C07','C09','C13','GED']
kerns = ['I','DX','DY','LAP']

index_dict = {}
iinput = -1
for alev in levs:
    for achan in chans:
        for akern in kerns:
            iinput += 1
            index_dict[(alev,achan,akern)] = iinput

#####


fig = plt.figure(figsize=(24,20))
plt.subplots_adjust(left=0.05,right=0.95,bottom=0.05,top=0.95,wspace=0.3,hspace=0.3)
fs = 'xx-large'

#####

iplot = 0

for achan in chans:
    for akern in kerns:

        iplot += 1
        plt.subplot(4,4,iplot)

        for ads in datasets:

            iinput = index_dict[(thelev,achan,akern)]

            z = tot_data[ads][:,iinput] / cnt_data[ads][:,iinput]

            bad = cnt_data[ads][:,iinput] <= 10
            z[bad] = np.nan

            plt.plot(xbins,z,color=colors[ads],linewidth=lw[ads])

        plt.grid()
        plt.xlabel('Input',fontsize=fs)
        plt.ylabel('Mean Output',fontsize=fs)
        if akern == 'I':
            plt.xlim([0,1])
            plt.xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0],fontsize=fs)
        else:
            plt.xlim([-1,1])
            plt.xticks([-1.0, -0.5, 0.0, 0.5, 1.0],fontsize=fs)
        plt.ylim([0,1])
        plt.title('Chan='+achan+', Kern='+akern,fontsize=fs)
        plt.yticks(fontsize=fs)

        plabel = '(' + ascii_lowercase[iplot-1] + ')'
        plt.text(0.025,0.925,plabel,color='black',fontsize='xx-large',fontweight='bold',transform=plt.gca().transAxes)

plt.text(0.150,0.975,'Identity Kernels',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')
plt.text(0.625,0.975,'Gradient Kernels',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')
axf = plt.axes([0,0,1,1],facecolor=(1,1,1,0),frame_on=False)
axf.set_xlim([0,1])
axf.set_ylim([0,1])
axf.plot([0.25,0.25],[0.01,0.99],color='black',linewidth=0.5)
plt.text(0.970,0.875-0.010,'Shortwave',fontsize=24,fontweight='bold',transform=fig.transFigure,rotation=90,va='center')
plt.text(0.970,0.625+0.000,'Water Vapor',fontsize=24,fontweight='bold',transform=fig.transFigure,rotation=90,va='center')
plt.text(0.970,0.375+0.010,'Longwave',fontsize=24,fontweight='bold',transform=fig.transFigure,rotation=90,va='center')
plt.text(0.970,0.125+0.025,'Lightning',fontsize=24,fontweight='bold',transform=fig.transFigure,rotation=90,va='center')

figname = 'figure6_bin_avgs_1d.png'
fig.savefig(figname)
print(figname)
plt.clf()

#####

