from copy import deepcopy
from scipy import signal
from skimage.measure import block_reduce
import numpy as np
import sys

#####

try:
    atype = sys.argv[1]
except:
    sys.exit("Error, you must supply '1d' or '2d' argument")

try:
    nogamma = '_'+sys.argv[2]
except:
    nogamma = ''

in_file = 'gremlin_conus2.npz'
out_file = 'gremlin_conus2_inputs_'+atype+nogamma+'.bin'

#####

print('reading',in_file)
ldata = np.load(in_file)
data = {}
data['Xdata_train'] = deepcopy( ldata['Xdata_train'] )
data['Xdata_test'] = deepcopy( ldata['Xdata_test'] )
data['Ydata_train'] = deepcopy( ldata['Ydata_train'] )
data['Ydata_test'] = deepcopy( ldata['Ydata_test'] )

bad = {}

bad['train'] = \
    ( data['Xdata_train'][:,:,:,0] == 0 ) & \
    ( data['Xdata_train'][:,:,:,1] == 0 ) & \
    ( data['Xdata_train'][:,:,:,2] == 0 ) & \
    ( data['Xdata_train'][:,:,:,3] == 0 ) & \
    ( data['Ydata_train'][:,:,:] == 0 )

bad['test'] = \
    ( data['Xdata_test'][:,:,:,0] == 0 ) & \
    ( data['Xdata_test'][:,:,:,1] == 0 ) & \
    ( data['Xdata_test'][:,:,:,2] == 0 ) & \
    ( data['Xdata_test'][:,:,:,3] == 0 ) & \
    ( data['Ydata_test'][:,:,:] == 0 )

print('nbad train,test =',np.sum(bad['train']),np.sum(bad['test']))

if nogamma == '':
    G = {0:1.210, 1:1.044, 2:1.820, 3:0.102}
    for i in [0,1,2,3]:
        data['Xdata_train'][:,:,:,i] **= G[i]
        data['Xdata_test'][:,:,:,i] **= G[i]

nt = {'test':448, 'train':1798}
ny = 256
nx = 256
ncin = 4
ncout = 1

for ic in range(ncin):
    data['Xdata_train'][:,:,:,ic][bad['train']] = np.nan
    data['Xdata_test'][:,:,:,ic][bad['test']] = np.nan
data['Ydata_train'][bad['train']] = np.nan
data['Ydata_test'][bad['test']] = np.nan

#####

nlev = 4

kerns = []
kerns.append( np.array( [[ 0.,  0.,  0.],[ 0.,  1.,  0.],[ 0.,  0.,  0.]] ) )       # Identity
kerns.append( np.array( [[ 1.,  0., -1.],[ 2.,  0., -2.],[ 1.,  0., -1.]] ) / 4. )  # Sobel DX
kerns.append( np.array( [[ 1.,  2.,  1.],[ 0.,  0.,  0.],[-1., -2., -1.]] ) / 4. )  # Sobel DY
kerns.append( np.array( [[ 1.,  1.,  1.],[ 1., -8.,  1.],[ 1.,  1.,  1.]] ) / 8. )  # Laplacian

gausblur_kern = np.array( [[ 1.,  2.,  1.],[ 2.,  4.,  2.],[ 1.,  2.,  1.]] ) / 16.

nkern = len(kerns)

ninputs = ncin * nlev * nkern
print('ninputs =',ninputs)

#####

Xdata = {}
Ydata = {}

for ads in ['test','train']:

    print('ads =',ads)

    if atype == '1d':
        Xdata[ads] = np.zeros((nt[ads]*ny*nx,ninputs),dtype=np.float32)
    else:
        Xdata[ads] = np.zeros((nt[ads],ny,nx,ninputs),dtype=np.float32)

    for ilev in range(nlev):

        xx = deepcopy(data['Xdata_'+ads])

        if (ilev==0):
            for it,ic in np.ndindex((nt[ads],ncin)):
                xx[it,:,:,ic] = signal.convolve2d( \
                    xx[it,:,:,ic], gausblur_kern, fillvalue=np.nan, mode='same')
        for klev in range(ilev):
            for it,ic in np.ndindex((nnt,nnc)):
                xx[it,:,:,ic] = signal.convolve2d( \
                    xx[it,:,:,ic], gausblur_kern, fillvalue=np.nan, mode='same')
            xx = block_reduce(xx,(1,2,2,1),np.max)

        nnt,nny,nnx,nnc = xx.shape
        if nnt != nt[ads]: sys.exit('nnt error')
        if nnc != ncin: sys.exit('nnc error')
        print('ilev,nny,nnx =',ilev,nny,nnx)

        fxx = np.zeros((nnt,nny,nnx,nnc*nkern),dtype=np.float32)

        for icin in range(ncin):
            for ikern,akern in enumerate(kerns):
                kinput = icin*nkern + ikern
                for it in range(nt[ads]):
                    fxx[it,:,:,kinput] = signal.convolve2d( \
                        xx[it,:,:,icin], akern, fillvalue=np.nan, mode='same' )

        for klev in range(ilev):
            fxx = np.repeat(fxx,2,axis=1).repeat(2,axis=2)
            for it,ic in np.ndindex((nnt,nnc*nkern)):
                fxx[it,:,:,ic] = signal.convolve2d( \
                    fxx[it,:,:,ic], gausblur_kern, fillvalue=np.nan, mode='same')

        for icin in range(ncin):
            for ikern in range(nkern):
                iinput = ilev*(nkern*ncin) + icin*nkern + ikern
                kinput = icin*nkern + ikern
                if atype == '1d':
                    Xdata[ads][:,iinput] = fxx[:,:,:,kinput].flatten()
                else:
                    Xdata[ads][:,:,:,iinput] = fxx[:,:,:,kinput]

    if atype == '1d':
        Ydata[ads] = np.array(data['Ydata_'+ads].flatten(),dtype=np.float32)
    else:
        Ydata[ads] = np.array(data['Ydata_'+ads],dtype=np.float32)

    if atype == '1d':
        good = np.isfinite(np.amax(Xdata[ads],axis=1))
        print('good shape, ngood =',good.shape,np.sum(good))
        Xdata[ads] = Xdata[ads][good,:]
        Ydata[ads] = Ydata[ads][good]

    print('ads,nsamp =',ads,Xdata[ads].shape[0])

#####

print('writing',out_file)

if atype == '1d':
    nsamp_train,ninput = Xdata['train'].shape
    nsamp_test,ninput = Xdata['test'].shape
else:
    nsamp_train,ny,nx,ninput = Xdata['train'].shape
    nsamp_test,ny,nx,ninput = Xdata['test'].shape

print('nsamp_train, nsamp_test, ninput =',nsamp_train,nsamp_test,ninput)

f = open(out_file,'wb')
if atype == '1d':
    np.array([nsamp_train],dtype=np.int64).tofile(f)
    np.array([nsamp_test],dtype=np.int64).tofile(f)
    np.array([ninput],dtype=np.int64).tofile(f)
else:
    np.array([nsamp_train],dtype=np.int64).tofile(f)
    np.array([nsamp_test],dtype=np.int64).tofile(f)
    np.array([ny],dtype=np.int64).tofile(f)
    np.array([nx],dtype=np.int64).tofile(f)
    np.array([ninput],dtype=np.int64).tofile(f)
Xdata['train'].tofile(f)
Xdata['test'].tofile(f)
Ydata['train'].tofile(f)
Ydata['test'].tofile(f)
f.close()
