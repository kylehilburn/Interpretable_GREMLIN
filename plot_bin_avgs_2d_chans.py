import numpy as np
from matplotlib import pyplot as plt
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

bins_dict = {}
bins_dict['C13'] = [100 + 300 - 100.*0.02*i for i in range(101)]
bins_dict['C09']  = [50 + 250 - 50.*0.02*i for i in range(101)]
bins_dict['C07'] = [100 + 300 - 100.*0.02*i for i in range(101)]
bins_dict['GED'] = [-50. + 50.*0.02*i for i in range(101)]

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

fig = plt.figure(figsize=(24,15))
fig.subplots_adjust(left=0.05,right=0.95,bottom=0.15,top=0.95,wspace=0.3,hspace=0.3)
fs = 'x-large'

alev = 'L0'

#chancombos = [('C07','C09'),('C07','C13'),('C09','C13'),('C07','GED'),('C09','GED'),('C13','GED')]
chancombos = [('C07','C13'),('C09','C13'),('C13','GED')]

units = {'C07':'K', 'C09':'K', 'C13':'K', 'GED':'Groups/5-min/km$^2$'}

akern = 'I'

iplot = 0

for bchan,achan in chancombos:

    for ads in datasets:

        k1 = (alev,achan,akern)
        k2 = (alev,bchan,akern)

        ii = indices[k1]
        jj = indices[k2]

        img = scldbz * tots[ads][:,:,jj,ii] / cnts[ads][:,:,jj,ii]

        img = np.ma.masked_invalid(img)

        iplot += 1
        plt.subplot(3,4,iplot)

        #pcm = plt.pcolormesh(bins,bins,img,cmap=cmap,norm=norm)
        pcm = plt.pcolormesh(bins_dict[achan],bins_dict[bchan],img,cmap=cmap,norm=norm)

        plt.grid()
        plt.xlabel(achan+' ('+units[achan]+')',fontsize=fs)
        plt.ylabel(bchan+' ('+units[bchan]+')',fontsize=fs)

        if achan.startswith('C'):
            plt.xlim([200,300])
        else:
            plt.xlim([0,50])
        plt.xticks(fontsize=fs)

        if bchan.startswith('C'):
            plt.ylim([200,300])
        else:
            plt.ylim([0,50])
        plt.yticks(fontsize=fs)

        if achan.startswith('C') and bchan.startswith('C'):
            plt.plot([200,300],[200,300],color='black',linestyle='dashed')

        plt.title('Model='+model_names[ads])

        plabel = '(' + ascii_lowercase[iplot-1] + ')'
        plt.text(0.025,0.925,plabel,color='black',fontsize='xx-large',fontweight='bold',transform=plt.gca().transAxes)

cax = fig.add_axes([0.25, 0.06, 0.50, 0.02])
cb = plt.colorbar(pcm,orientation='horizontal',ticks=bounds,cax=cax)
cb.set_label('Composite Reflectivity (dBZ)',fontsize=fs)
cb.ax.set_xticklabels(ticklabels,fontsize=fs)

plt.text(0.125+0.0175,0.975,'DATA',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')
plt.text(0.375+0.0080,0.975,'CNN',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')
plt.text(0.625-0.0060,0.975,'DENSE',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')
plt.text(0.875-0.0150,0.975,'LINEAR',fontsize=24,fontweight='bold',transform=fig.transFigure,ha='center')

plt.text(0.965,0.835,'SW vs LW',fontsize=24,fontweight='bold',transform=fig.transFigure,rotation=90,va='center')
plt.text(0.965,0.550,'WV vs LW',fontsize=24,fontweight='bold',transform=fig.transFigure,rotation=90,va='center')
plt.text(0.965,0.275,'LW vs GED',fontsize=24,fontweight='bold',transform=fig.transFigure,rotation=90,va='center')

figname = 'figure9_bin_avgs_2d_chans_'+alev+'_'+akern+'.png'
fig.savefig(figname)
print(figname)
plt.clf()

#####

