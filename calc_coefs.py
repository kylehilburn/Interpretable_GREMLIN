import numpy as np
import sys

f = open('covar.bin','rb')
nparm = np.fromfile(f,dtype=np.int32,count=1)[0]
print('nparm=',nparm)
meany = np.fromfile(f,dtype=np.float64,count=1)[0]
cross = np.fromfile(f,dtype=np.float64,count=nparm)
covar = np.fromfile(f,dtype=np.float64,count=nparm*nparm).reshape((nparm,nparm))
f.close()

#print(meany)
#print(np.min(cross),np.max(cross))
#print(np.min(covar),np.max(covar))

cinv = np.linalg.inv(covar)

w = np.transpose( np.matmul(cinv,cross) )

#print(w.shape)
#print(w.dtype)
#print(np.min(w),np.max(w))

f = open('coefs.bin','wb')
np.array([nparm],dtype=np.int32).tofile(f)
w.tofile(f)
f.close()
