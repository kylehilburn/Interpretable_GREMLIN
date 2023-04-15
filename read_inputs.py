import numpy as np

def read_inputs_1d(filename):

    data = {}

    f = open(filename,'rb')

    dtype = np.int64
    nsamp_train = np.fromfile(f,dtype=dtype,count=1)[0]
    nsamp_test = np.fromfile(f,dtype=dtype,count=1)[0]
    ninputs = np.fromfile(f,dtype=dtype,count=1)[0]
    data['nsamp_train'] = nsamp_train
    data['nsamp_test'] = nsamp_test
    data['ninputs'] = ninputs

    dtype = np.float32
    data['Xdata_train'] = np.fromfile(f,dtype=dtype,count=nsamp_train*ninputs).reshape((nsamp_train,ninputs))
    data['Xdata_test'] = np.fromfile(f,dtype=dtype,count=nsamp_test*ninputs).reshape((nsamp_test,ninputs))
    data['Ydata_train'] = np.fromfile(f,dtype=dtype,count=nsamp_train)
    data['Ydata_test'] = np.fromfile(f,dtype=dtype,count=nsamp_test)

    f.close()

    return data

def read_inputs_2d(filename):

    data = {}

    f = open(filename,'rb')

    dtype = np.int64
    nsamp_train = np.fromfile(f,dtype=dtype,count=1)[0]
    nsamp_test = np.fromfile(f,dtype=dtype,count=1)[0]
    ny = np.fromfile(f,dtype=dtype,count=1)[0]
    nx = np.fromfile(f,dtype=dtype,count=1)[0]
    ninputs = np.fromfile(f,dtype=dtype,count=1)[0]

    data['nsamp_train'] = nsamp_train
    data['nsamp_test'] = nsamp_test
    data['ny'] = ny
    data['nx'] = nx
    data['ninputs'] = ninputs

    dtype = np.float32
    data['Xdata_train'] = np.fromfile(f,dtype=dtype,count=nsamp_train*ny*nx*ninputs).reshape((nsamp_train,ny,nx,ninputs))
    data['Xdata_test'] = np.fromfile(f,dtype=dtype,count=nsamp_test*ny*nx*ninputs).reshape((nsamp_test,ny,nx,ninputs))
    data['Ydata_train'] = np.fromfile(f,dtype=dtype,count=nsamp_train*ny*nx).reshape((nsamp_train,ny,nx))
    data['Ydata_test'] = np.fromfile(f,dtype=dtype,count=nsamp_test*ny*nx).reshape((nsamp_test,ny,nx))

    f.close()

    return data
