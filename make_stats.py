from netCDF4 import Dataset
import numpy as np
import sys

from get_statistics import get_refc_stats, refthrs
from read_predictions import read_predictions

ads = sys.argv[1]

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

good = (Ydata >= 0) & (preds >= 0)
Ydata = Ydata[good]
preds = preds[good]
stats = get_refc_stats(preds,Ydata)

keys = []
keys.append('mean(goes-mrms)')
keys.append('std(goes-mrms)')
keys.append('rmsd')
keys.append('pearson_rsq')
keys.append('r_square')

#print(predfile)

for akey in keys:
    print(akey+'=','{0:7.4f}'.format(stats[akey]))

for aref in refthrs:
    print('catstats=',aref, \
        '{0:7.4f}'.format(stats['pod_'+str(aref)]), \
        '{0:7.4f}'.format(stats['far_'+str(aref)]), \
        '{0:7.4f}'.format(stats['csi_'+str(aref)]), \
        '{0:7.4f}'.format(stats['bias_'+str(aref)]) )
