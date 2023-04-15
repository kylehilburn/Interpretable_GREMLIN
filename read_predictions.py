import numpy as np

def read_predictions(filename):

    f = open(filename,'rb')

    dtype = np.int32
    nsamp = np.fromfile(f,dtype=dtype,count=1)[0]
    ny = np.fromfile(f,dtype=dtype,count=1)[0]
    nx = np.fromfile(f,dtype=dtype,count=1)[0]

    dtype = np.float32
    predictions = np.fromfile(f,dtype=dtype,count=nsamp*ny*nx).reshape((nsamp,ny,nx))

    f.close()

    return predictions
