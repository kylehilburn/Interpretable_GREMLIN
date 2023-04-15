from datetime import datetime
import sys

def read_datetimes(filename='sample_datetimes.txt'):

    datetimes = {'TRAIN':[], 'TEST':[]}

    f = open(filename,'r')

    for aline in f:

        if aline.startswith('*'):
            akey = aline.replace('*','').strip()
            continue
        
        items = [anitem.strip() for anitem in aline.split()]
        
        samplenumber = int(items[0])
        adatetime = datetime.strptime(items[1], '%Y%m%d%H%MZ')

        datetimes[akey].append(adatetime)

    f.close()

    return datetimes
