import numpy as np

def read_bin_avgs(filename):

    data = {}

    f = open(filename,'rb')

    ninputs = np.fromfile(f,dtype=np.int32,count=1)[0]
    nbinsx = np.fromfile(f,dtype=np.int32,count=1)[0]

    data['ninputs'] = ninputs
    data['nbinsx'] = nbinsx

    data['xbins'] = np.fromfile(f,dtype=np.float32,count=nbinsx)

    data['cnt1d'] = np.fromfile(f,dtype=np.float64,count=nbinsx*ninputs).reshape((nbinsx,ninputs))
    data['tot1d'] = np.fromfile(f,dtype=np.float64,count=nbinsx*ninputs).reshape((nbinsx,ninputs))

    data['cnt2d'] = np.fromfile(f,dtype=np.float64,count=nbinsx*nbinsx*ninputs*ninputs).reshape((nbinsx,nbinsx,ninputs,ninputs))
    data['tot2d'] = np.fromfile(f,dtype=np.float64,count=nbinsx*nbinsx*ninputs*ninputs).reshape((nbinsx,nbinsx,ninputs,ninputs))

    f.close()

    return data
