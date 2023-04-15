import numpy as np

import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore')  #to catch FutureWarnings
    import tensorflow as tf
    from tensorflow.keras import models
    from tensorflow.keras.models import load_model

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

data_file = 'gremlin_conus2.npz'
data = np.load(data_file)
datasets = ['test','train']

model_file = 'model_K12_WTD_ALL_3x3_T_SEQ_blocks_3_epochs_100.h5'
model = load_model(model_file,\
    custom_objects={\
    "my_r_square_metric": my_r_square_metric,\
    "my_mean_squared_error_genexp": my_mean_squared_error_weighted_genexp,\
    "loss": my_mean_squared_error_weighted_genexp(),\
    "my_csi20_metric": my_csi20_metric,\
    "my_csi35_metric": my_csi35_metric,\
    "my_csi50_metric": my_csi50_metric,\
    "my_bias20_metric": my_bias20_metric,\
    "my_bias35_metric": my_bias35_metric,\
    "my_bias50_metric": my_bias50_metric,\
    })

#####

for ads in datasets:

    print('ads =',ads,flush=True)

    bad = \
        (data['Xdata_'+ads][:,:,:,0] == 0) & \
        (data['Xdata_'+ads][:,:,:,1] == 0) & \
        (data['Xdata_'+ads][:,:,:,2] == 0) & \
        (data['Xdata_'+ads][:,:,:,3] == 0) & \
        (data['Ydata_'+ads][:,:,:] == 0)

    preds = 60.*model.predict(data['Xdata_'+ads])
    preds[preds<0] = 0.
    preds[bad] = -1.E30

    print('preds shape =',preds.shape)
    print('preds dtype =',preds.dtype)

    nsamp, ny, nx = preds.shape
    print('nsamp,ny,nx =',nsamp,ny,nx)

    out_file = 'predictions_gremlin_'+ads+'_2d.bin'
    print('writing ',out_file,flush=True)
    f = open(out_file,'wb')
    np.array([nsamp],dtype=np.int32).tofile(f)
    np.array([ny],dtype=np.int32).tofile(f)
    np.array([nx],dtype=np.int32).tofile(f)
    preds.tofile(f)
    f.close()
