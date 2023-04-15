from matplotlib import pyplot as plt
import numpy as np
from string import ascii_lowercase

from radar_reflec_cmap import cmap, norm, bounds, ticklabels
from read_bin_avgs import read_bin_avgs

#####

datasets = ['data','gremlin','dense','linear']
model_names = {'data':'DATA', 'gremlin':'CNN', 'dense':'DENSE', 'linear':'LINEAR'}

cnts = {}
tots = {}
for ads in datasets:
    data = read_bin_avgs('bin_avgs_'+ads+'.bin')
    bins = data['xbins']
    cnts[ads] = data['cnt2d']
    tots[ads] = data['tot2d']

#####

levs = ['L0','L1','L2','L3']
chans = ['C07','C09','C13','GED']
kerns = ['I','DX','DY','LAP']

indices = {}
iinput = -1
for alev in levs:
    for achan in chans:
        for akern in kerns:
            iinput += 1
            indices[(alev,achan,akern)] = iinput

#####

scldbz = 60.

fig = plt.figure(figsize=(24,12))
fig.subplots_adjust(left=0.05,right=0.95,bottom=0.15,top=0.93,wspace=0.3,hspace=0.3)
fs = 'xx-large'

iplot = 0

#gb_kernel = np.array( [[ 1.,  2.,  1.],[ 2.,  4.,  2.],[ 1.,  2.,  1.]] ) / 16.

alev = 'L0'
chans = ['C13','GED']

for achan in chans:
    for ads in datasets:

        print(achan,ads)

        k1 = (alev,achan,'DY')
        k2 = (alev,achan,'DX')

        ii = indices[k1]
        jj = indices[k2]
        img = scldbz * tots[ads][:,:,jj,ii] / cnts[ads][:,:,jj,ii]

        img = img.T  #transpose to swap DY and DX
        img = img[::-1, ::-1]  #reverse to put in meteorological sense

        img = np.ma.masked_invalid(img)

        iplot += 1
        plt.subplot(2,4,iplot)

        pcm = plt.pcolormesh(bins,bins,img,cmap=cmap,norm=norm)
        
        #plt.grid()
        plt.plot([0,0],[-1,1],linestyle='solid',linewidth=0.5,color='gray')
        plt.plot([-1,1],[0,0],linestyle='solid',linewidth=0.5,color='gray')
        plt.plot([-1,1],[-1,1],linestyle='solid',linewidth=0.5,color='gray')
        plt.plot([-1,1],[1,-1],linestyle='solid',linewidth=0.5,color='gray')

        plt.xlabel('-DX',fontsize=fs)
        plt.ylabel('-DY',fontsize=fs)

        plt.xlim([-1,1])
        plt.ylim([-1,1])
        plt.xticks([-1,0,1],fontsize=fs)
        plt.yticks([-1,0,1],fontsize=fs)

        plt.title('Model='+model_names[ads]+', Chan='+achan,fontsize=fs)

        plabel = '(' + ascii_lowercase[iplot-1] + ')'
        plt.text(0.025,0.925,plabel,color='black',fontsize='xx-large',fontweight='bold',transform=plt.gca().transAxes)

cax = fig.add_axes([0.25, 0.06, 0.50, 0.02])
cb = plt.colorbar(pcm,orientation='horizontal',ticks=bounds,cax=cax)
cb.set_label('Composite Reflectivity (dBZ)',fontsize=fs)
cb.ax.set_xticklabels(ticklabels,fontsize=fs)

plt.text(0.125+0.0175,0.965,'DATA',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')
plt.text(0.375+0.0080,0.965,'CNN',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')
plt.text(0.625-0.0060,0.965,'DENSE',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')
plt.text(0.875-0.0150,0.965,'LINEAR',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')

plt.text(0.965,0.775,'Longwave',fontsize=24,fontweight='bold',transform=fig.transFigure,rotation=90,va='center')
plt.text(0.965,0.330,'Lightning',fontsize=24,fontweight='bold',transform=fig.transFigure,rotation=90,va='center')

figname = 'figure7_bin_avgs_2d_dxdy.png'

fig.savefig(figname)
print(figname)
plt.clf()

#####

