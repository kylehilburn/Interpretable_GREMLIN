import numpy as np
from scipy.stats import pearsonr
import sys

################################################################

refthrs = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]

stat_names = ['mean(goes-mrms)', 'std(goes-mrms)', 'rmsd', 'pearson_rsq', 'r_square', 'pod_5', 'far_5', 'csi_5', 'bias_5', 'pod_10', 'far_10', 'csi_10', 'bias_10', 'pod_15', 'far_15', 'csi_15', 'bias_15', 'pod_20', 'far_20', 'csi_20', 'bias_20', 'pod_25', 'far_25', 'csi_25', 'bias_25', 'pod_30', 'far_30', 'csi_30', 'bias_30', 'pod_35', 'far_35', 'csi_35', 'bias_35', 'pod_40', 'far_40', 'csi_40', 'bias_40', 'pod_45', 'far_45', 'csi_45', 'bias_45', 'pod_50', 'far_50', 'csi_50', 'bias_50']

################################################################

def r_square(y_true,y_pred):
    ss_res = np.sum(np.square(y_true-y_pred))
    ss_tot = np.sum(np.square(y_true-np.mean(y_true)))
    return ( 1 - ss_res/(ss_tot + np.finfo(np.float32).eps) )

################################################################

def get_refc_stats(goes,mrms):

# inputs, required:
#   goes = goes refc (prediction)
#   mrms = mrms refc (truth)

# outputs:
#   stats = dictionary of stats

    stats = {}

    stats['mean(goes-mrms)'] = np.mean(goes-mrms)
    stats['std(goes-mrms)'] = np.std(goes-mrms)
    stats['rmsd'] = np.sqrt(np.mean((goes-mrms)**2))
    stats['pearson_rsq'] = pearsonr(mrms,goes)[0]**2
    stats['r_square'] = r_square(mrms,goes)

    for rthr in refthrs:

        hasrad = mrms > rthr
        nrad = np.sum(hasrad)

        hassat = goes > rthr
        nsat = np.sum(hassat)

        if nrad == 0:
            stats['pod_'+str(rthr)] = np.nan
            stats['far_'+str(rthr)] = np.nan
            stats['csi_'+str(rthr)] = np.nan
            stats['bias_'+str(rthr)] = np.nan
#            stats['nrad_'+str(rthr)] = nrad
#            stats['nsat_'+str(rthr)] = nsat
            continue

        nhit = np.sum(  hasrad &  hassat )
        nmis = np.sum(  hasrad & ~hassat )
        nfal = np.sum( ~hasrad &  hassat )

        try:
            csi = float(nhit) / float(nhit + nmis + nfal)
        except ZeroDivisionError:
            csi = np.nan
        try:
            pod = float(nhit) / float(nhit + nmis)
        except ZeroDivisionError:
            pod = np.nan
        try:
            far = float(nfal) / float(nhit + nfal)  #FA ratio
        except ZeroDivisionError:
            far = np.nan
        try:
            bias = float(nhit + nfal) / float(nhit + nmis)
        except ZeroDivisionError:
            bias = np.nan

        stats['pod_'+str(rthr)] = pod
        stats['far_'+str(rthr)] = far
        stats['csi_'+str(rthr)] = csi
        stats['bias_'+str(rthr)] = bias
#        stats['nrad_'+str(rthr)] = nrad
#        stats['nsat_'+str(rthr)] = nsat

    return stats
