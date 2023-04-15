import numpy as np

import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')  #to catch FutureWarnings
    import tensorflow as tf
    from tensorflow.keras import Input
    from tensorflow.keras.layers import Dense
    from tensorflow.keras.models import Sequential
    from tensorflow.keras import backend as K

from custom_model_elements import my_r_square_metric
from custom_model_elements import my_mean_squared_error_weighted_genexp
from custom_model_elements import my_csi20_metric
from custom_model_elements import my_csi35_metric
from custom_model_elements import my_csi50_metric
from custom_model_elements import my_bias20_metric
from custom_model_elements import my_bias35_metric
from custom_model_elements import my_bias50_metric

from read_inputs import read_inputs_2d

#####

data_file = 'gremlin_conus2_inputs_2d_nogamma.bin'
data = read_inputs_2d(data_file)
ninputs = data['ninputs']
datasets = ['test','train']

model_file = 'model_tune34_epochs100_batchsize10000_layers3_units64.h5'
epochs = 100
batch_size = 10000
layers = 3
units = 64

#####

K.clear_session()

activation = 'relu'
output_dim = 1
optimizer = 'adam'
loss_weight = (1.0, 4.0, 4.0)
loss = my_mean_squared_error_weighted_genexp(weight=loss_weight)
metrics = []
metrics.append(my_r_square_metric)
metrics.append(my_csi20_metric)
metrics.append(my_csi35_metric)
metrics.append(my_csi50_metric)
metrics.append(my_bias20_metric)
metrics.append(my_bias35_metric)
metrics.append(my_bias50_metric)

model = Sequential()
model.add( Input(shape=(ninputs,)) )
for ilayer in range(layers):
    model.add( Dense(units, activation=activation) )
model.add( Dense(output_dim,activation=activation) )

model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

model.load_weights(model_file)

#####

for ads in datasets:

    print('ads =',ads,flush=True)

    nsamp = data['nsamp_'+ads]
    ny = data['ny']
    nx = data['nx']
    print('nsamp,ny,nx,ninputs =',nsamp,ny,nx,ninputs)

    preds = 60.*np.squeeze( model.predict(data['Xdata_'+ads].reshape((nsamp*ny*nx,ninputs))) ).reshape((nsamp,ny,nx))
    preds[preds<0] = 0.
    preds[~np.isfinite(preds)] = -1.E30
    print('preds shape =',preds.shape)
    print('preds dtype =',preds.dtype)

    out_file = 'predictions_dense_'+ads+'_2d.bin'
    print('writing ',out_file,flush=True)
    f = open(out_file,'wb')
    np.array([nsamp],dtype=np.int32).tofile(f)
    np.array([ny],dtype=np.int32).tofile(f)
    np.array([nx],dtype=np.int32).tofile(f)
    preds.tofile(f)
    f.close()
