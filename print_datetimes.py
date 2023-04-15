from netCDF4 import Dataset, num2date
from datetime import datetime, timedelta
import numpy as np

in_file = 'gremlin_conus2_dataset.nc'

# Samples 0 to 1797 were used for training and samples 1798 to 2245 were used for testing

ds = Dataset(in_file,'r')

times = ds.variables['time']
dates = num2date(times[:], units=times.units, calendar=times.calendar)

print('*TRAIN*')
for isamp in range(0,1798):
    adate = dates[isamp]
    if adate.second == 59: adate = adate + timedelta(seconds=1)
    print(isamp, adate.strftime('%Y%m%d%H%MZ'))

print('*TEST*')
for isamp in range(1798,2246):
    adate = dates[isamp]
    if adate.second == 59: adate = adate + timedelta(seconds=1)
    print(isamp-1798, adate.strftime('%Y%m%d%H%MZ'))

ds.close()
