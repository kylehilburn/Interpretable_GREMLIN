from netCDF4 import Dataset
import numpy as np
from sklearn.utils import resample
import sys

from get_statistics import get_refc_stats, refthrs, stat_names
from read_predictions import read_predictions

#####

ads = sys.argv[1]

nresamp = int(sys.argv[2])

#####

nstats = len(stat_names)

def bootstrap_resample(data,nresamp):
    bs_stats = np.zeros((nresamp,nstats))
    for isamp in range(nresamp):
        asamp = resample(data)  # note: resampling is performed on the level of samples (images)
        good = (asamp[:,:,:,0] >=0) & (asamp[:,:,:,1] >= 0)
        stats = get_refc_stats(asamp[:,:,:,0][good], asamp[:,:,:,1][good])
        for istat,astat in enumerate(stat_names):
            bs_stats[isamp,istat] = stats[astat]
    return bs_stats
    
def get_95_cis(stats):
    cis = {}
    for istat,astat in enumerate(stat_names):
        sd = np.std(stats[:,istat])
        mn = np.mean(stats[:,istat])
        cis[astat] = (mn-1.96*sd, mn+1.96*sd)
    return cis

#####

datafile = 'gremlin_conus2_dataset.nc'
ds = Dataset(datafile,'r')
nbatches = {'train':1798, 'test':448}
i0 = nbatches['train']
i1 = nbatches['train'] + nbatches['test']
Ydata = ds.variables['MRMS_REFC'][i0:i1, :, :]
ds.close()
ybad = Ydata <= -999.
Ydata[Ydata<0] = 0.  #suppress sub-zero variability (non-meteorological echoes)
Ydata[ybad] = -999.

#####

predfile = 'predictions_'+ads+'_test_2d.bin'
preds = read_predictions(predfile)
pbad = preds <= -1.E30
preds[preds<0] = 0.  #suppress sub-zero variability (non-meteorological echoes)
preds[pbad] = -999.

#####

# remove pixels lacking full spatial context
preds[:,   0:30 ,    :   ] = -999.
preds[:, 226:256,    :   ] = -999.
preds[:,    :   ,   0:30 ] = -999.
preds[:,    :   , 226:256] = -999.

#####

nsamp,ny,nx = preds.shape
data = np.zeros((nsamp,ny,nx,2))
data[:,:,:,0] = preds
data[:,:,:,1] = Ydata

bs_stats = bootstrap_resample(data,nresamp)

outfile = 'bootstrap_stats_'+ads+'_'+str(nresamp)+'.bin'
f = open(outfile,'wb')
np.array([nresamp],dtype=np.int32).tofile(f)
np.array([nstats],dtype=np.int32).tofile(f)
bs_stats.tofile(f)
f.close()

cis = get_95_cis(bs_stats, clevel)

keys = []
keys.append('mean(goes-mrms)')
keys.append('std(goes-mrms)')
keys.append('rmsd')
keys.append('pearson_rsq')
keys.append('r_square')

for akey in keys:
    print(akey+'=','{0:7.4f} {1:7.4f}'.format(cis[akey][0],cis[akey][1]))

for aref in refthrs:
    print('catstats=',aref, \
        '{0:7.4f} {1:7.4f}'.format(cis['pod_'+str(aref)][0],cis['pod_'+str(aref)][1]), \
        '{0:7.4f} {1:7.4f}'.format(cis['far_'+str(aref)][0],cis['far_'+str(aref)][1]), \
        '{0:7.4f} {1:7.4f}'.format(cis['csi_'+str(aref)][0],cis['csi_'+str(aref)][1]), \
        '{0:7.4f} {1:7.4f}'.format(cis['bias_'+str(aref)][0],cis['bias_'+str(aref)][1]) )
