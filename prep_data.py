from netCDF4 import Dataset
import numpy as np

###

in_file = 'gremlin_conus2_dataset.nc'
out_file = 'gremlin_conus2.npz'

###

xmin = {'GOES_ABI_C07':200., 'GOES_ABI_C09':200., 'GOES_ABI_C13':200., 'GOES_GLM_GROUP':0.1}
xmax = {'GOES_ABI_C07':300., 'GOES_ABI_C09':250., 'GOES_ABI_C13':300., 'GOES_GLM_GROUP':50.0}

ymin = 0.
ymax = 60.

chans = ['GOES_ABI_C07', 'GOES_ABI_C09', 'GOES_ABI_C13', 'GOES_GLM_GROUP']
nchans = len(chans)

# Samples 0 to 1797 were used for training and samples 1798 to 2245 were used for testing
nbatches = {'train':1798, 'test':448}

fill_value = 0  # for output

Xdata = {}
Ydata = {}
Lat = {}
Lon = {}

print('reading',in_file)

ds = Dataset(in_file,'r')

print(ds)

for ads in ['train','test']:

    print('ads=',ads)

    ny = ds.dimensions['ny'].size
    nx = ds.dimensions['ny'].size

    if ads == 'train':
        i0 = 0
        i1 = nbatches['train']
    else:
        i0 = nbatches['train']
        i1 = nbatches['train'] + nbatches['test']

    Xdata[ads] = np.zeros((nbatches[ads],ny,nx,nchans))
    Ydata[ads] = np.zeros((nbatches[ads],ny,nx))
    Lat[ads] = np.zeros((nbatches[ads],ny,nx))
    Lon[ads] = np.zeros((nbatches[ads],ny,nx))
    badmask = np.zeros((nbatches[ads],ny,nx),np.int32)  #0=good, 1=bad

    for ichan,achan in enumerate(chans):
        print('achan=',achan)
        badmask[ np.ma.getmask(ds.variables[achan][i0:i1, :, :]) ] = 1
        if 'ABI' in achan:
            Xdata[ads][:,:,:,ichan] = (xmax[achan] - ds.variables[achan][i0:i1, :, :]) / (xmax[achan] - xmin[achan])
        else:
            Xdata[ads][:,:,:,ichan] = (ds.variables[achan][i0:i1, :, :] - xmin[achan]) / (xmax[achan] - xmin[achan])

    Xdata[ads][ Xdata[ads] < 0 ] = 0.
    Xdata[ads][ Xdata[ads] > 1 ] = 1.

    badmask[ np.ma.getmask(ds.variables['MRMS_REFC'][i0:i1, :, :]) ] = 1
    Ydata[ads][:,:,:] = (ds.variables['MRMS_REFC'][i0:i1, :, :] - ymin) / (ymax - ymin)

    Ydata[ads][ Ydata[ads] < 0 ] = 0.
    Ydata[ads][ Ydata[ads] > 1 ] = 1.

    Lat[ads][:,:,:] = ds.variables['latitude'][i0:i1, :, :]
    Lon[ads][:,:,:] = ds.variables['longitude'][i0:i1, :, :]

    for ichan in range(nchans):
        Xdata[ads][:,:,:,ichan][badmask==1] = fill_value

    Ydata[ads][:,:,:][badmask==1] = fill_value

ds.close()

print('writing',out_file)
np.savez( out_file, \
    Xdata_train = Xdata['train'], \
    Ydata_train = Ydata['train'], \
    Xdata_test = Xdata['test'], \
    Ydata_test = Ydata['test'], \
    Lat_train = Lat['train'], \
    Lon_train = Lon['train'], \
    Lat_test = Lat['test'], \
    Lon_test = Lon['test'] )
