import numpy as np
from netCDF4 import Dataset
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys

from radar_reflec_cmap import cmap, norm, bounds, ticklabels
from get_statistics import get_refc_stats
from read_datetimes import read_datetimes
from read_predictions import read_predictions

from matplotlib.patheffects import withStroke
embossed = [withStroke(linewidth=1,foreground='white')]

###

isamp = 68

###

pred_file = {}
pred_file['(B)'] = 'predictions_gremlin_test_2d.bin'
pred_file['(C)'] = 'predictions_dense_test_2d.bin'
pred_file['(D)'] = 'predictions_linear_test_2d.bin'

titles= {}
titles['(A)'] = '(A) MRMS'
titles['(B)'] = '(B) GREMLIN'
titles['(C)'] = '(C) DENSE'
titles['(D)'] = '(D) LINEAR'

###

datetimes = read_datetimes('sample_datetimes.txt')

data_file = 'gremlin_conus2_dataset.nc'
nsamp_train = 1798
ds = Dataset(data_file,'r')
mrms = ds.variables['MRMS_REFC'][isamp+nsamp_train, :, :]
lat = ds.variables['latitude'][isamp+nsamp_train, :, :]
lon = ds.variables['longitude'][isamp+nsamp_train, :, :]
ds.close()

no_mrms = mrms < -99
mrms[mrms<0] = 0.
mrms = np.ma.masked_where(no_mrms,mrms)

preds = {}
for apred in ['(B)','(C)','(D)']:
    preds[apred] = read_predictions(pred_file[apred])
    preds[apred] = np.ma.masked_where(preds[apred]<=-1.E30, preds[apred])

###

fig = plt.figure(figsize=(16,12))
plt.subplots_adjust(left=0.02,right=1.00,bottom=0.02,top=0.94,hspace=0.2,wspace=0.0)

nrow = 2
ncol = 2

fs = 'large'
fst = 'large'

datestring = datetimes['TEST'][isamp].strftime('%Y%m%d%H%MZ')

basemap = {}
basemap['projection'] = 'cyl'
basemap['resolution'] = 'l'
basemap['llcrnrlon'] = np.min(lon)
basemap['urcrnrlon'] = np.max(lon)
basemap['llcrnrlat'] = np.min(lat)
basemap['urcrnrlat'] = np.max(lat)
basemap['fix_aspect'] = False
basemap = Basemap(**basemap)
xb,yb = basemap(lon,lat)

xak,yak = basemap(-81.518, 41.073)

plt.subplot(nrow,ncol,1)
zz = mrms
pcm = basemap.pcolormesh(xb,yb,zz,cmap=cmap,norm=norm)
basemap.drawcoastlines()
basemap.drawcountries()
basemap.drawstates()
basemap.drawcounties()
smax = '{0:2.0f}'.format(np.max(zz))
plt.title(titles['(A)'] + ' (Max = '+smax+' dBZ)',fontsize=fst,fontweight='bold')

plt.text(xak,yak,'A', color='black', fontsize='xx-large',fontweight='bold', ha='center',va='center', path_effects=embossed)

cb = plt.colorbar(pcm,orientation='vertical',ticks=bounds)
cb.set_label('Composite Reflectivity (dBZ)',fontsize=fs)
cb.ax.tick_params(labelsize=fs)
cb.ax.set_xticklabels(ticklabels)

for apanel,ipanel in zip(['(B)','(C)','(D)'],[2,3,4]):
    print(apanel)
    plt.subplot(nrow,ncol,ipanel)
    zz = preds[apanel][isamp,:,:]
    zz[   0:30 ,    :   ] = np.nan
    zz[ 226:256,    :   ] = np.nan
    zz[    :   ,   0:30 ] = np.nan
    zz[    :   , 226:256] = np.nan
    bad = no_mrms | ~np.isfinite(zz)
    zz = np.ma.masked_where(bad,zz)
    pcm = basemap.pcolormesh(xb,yb,zz,cmap=cmap,norm=norm)
    basemap.drawcoastlines()
    basemap.drawcountries()
    basemap.drawstates()
    basemap.drawcounties()
    stats = get_refc_stats(zz,mrms,~bad,[35])

    plt.text(xak,yak,'A', color='black', fontsize='xx-large',fontweight='bold', ha='center',va='center', path_effects=embossed)

    items1 = []
    items1.append('RMSD={0:3.1f}'.format(stats['rmsd']))
    items1.append('RSQ={0:3.2f}'.format(stats['pearson_rsq']))
    items1.append('MAX={0:2.0f}'.format(np.max(zz)))

    items2 = []
    items2.append('CSI35={0:3.2f}'.format(stats['csi'][35]))
    items2.append('POD35={0:3.2f}'.format(stats['pod'][35]))
    items2.append('FAR35={0:3.2f}'.format(stats['far'][35]))

    stat_string1 = ', '.join(items1)
    stat_string2 = ', '.join(items2)
    plt.title(titles[apanel] + '\n\n', fontsize=fst,fontweight='bold')
    plt.text(0.5,1.01,stat_string1 + '\n' + stat_string2, fontsize=fst, ha='center',va='bottom',\
        transform=plt.gca().transAxes)

    cb = plt.colorbar(pcm,orientation='vertical',ticks=bounds)
    cb.set_label('Composite Reflectivity (dBZ)',fontsize=fs)
    cb.ax.tick_params(labelsize=fs)
    cb.ax.set_xticklabels(ticklabels)

figname = 'figure5_compare_prediction_maps_'+str(isamp).zfill(3)+'_'+datestring+'.png'
fig.savefig(figname,dpi=300)
print(figname)
fig.clf()
