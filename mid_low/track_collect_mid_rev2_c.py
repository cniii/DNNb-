'''
Mid level variables (16):

[jet_pt, jet_eta,
{D0, Z0, PHI, THETA, QOVERP,D0D0, Z0D0, Z0Z0, PHID0, PHIZ0, PHIPHI,
THETAD0, THETAZ0, THETAPHI, THETATHETA,QOVERPD0, QOVERPZ0, QOVERPPHI,
QOVERPTHETA, QOVERPQOVERP, mass, displacement, delta_eta_jet, delta_phi_jet,
displacement_significance, n_tracks, energy_fraction}(repeat 15 times)]

flavor (y):
signal --> y == 5
'''

_binning = {0: [-8, 8], 1: [-300, 300], 2: [-0.5, 0.5], 3: [-0.5, 0.5],
            4: [-2, 2], 5: [0, 0.005], 6: [-0.001, 0.01], 7: [0, 0.25], 8: [-0.0001, 0.0001], 9: [-0.0001, 0.0001],
            10: [0, 2.5], 11: [-2, 1.5], 12: [-0.0001, 0.0001], 13: [-1.5, 1.5], 14: [0, 5], 15: [0, 0.001],
            16: [-0.0001, 0.0001], 17: [0, 3], 18: [-5, 5], 19: [0, 0.0001], 20: [0, 1],
            21: [0, 40], 22: [-1000, 1000], 23: [-8, 8], 24: [-4, 4], 25: [0, 500],
            26: [0, 16], 27: [0, 1.2]}

import numpy as np
import h5py

'''
filepath = '/phys/groups/tev/scratch4/users/chengni/'
f = h5py.File(filepath + 'gjj_Variables_mid.hdf5', 'r')
'''
# for small dataset testing
filepath = '/Users/nhy/Desktop/DNN/Github_local/DNNb/mid_low/gjj_Variables_mid.hdf5'
f = h5py.File(filepath, 'r')

# only include first 100
mid = f['mid_input'][0:100, 0:15]  # 15 tracks
y = f['y_input'][0:100, 0:15]

mid_sig_collect = mid[y[:, 2].astype(bool), :, :]
mid_c_collect = mid[y[:, 1].astype(bool), :, :]
mid_bg_collect = mid[y[:, 0].astype(bool), :, :]

# same as Rev1 below
histo_sig_collector = []
histo_bg_collector = []
histo_c_collector = []
bin_collector = []

# histogram for each variable k
for k in range(mid_sig_collect.shape[2]):
    var_sig = []
    var_c = []
    var_bg = []
    for j in range(mid_sig_collect.shape[1]):
        var_sig.extend(mid_sig_collect[:, j, k])
        var_c.extend(mid_c_collect[:, j, k])
        var_bg.extend(mid_bg_collect[:, j, k])

    var_sig = np.asarray(var_sig)
    var_c = np.asarray(var_c)
    var_bg = np.asarray(var_bg)

    # remove nan for plotting
    sig = var_sig[~np.isnan(var_sig)]
    bg = var_bg[~np.isnan(var_bg)]
    c = var_c[~np.isnan(var_c)]

    # create bins
    if k in _binning:
        bin_min, bin_max = _binning.get(k)
    else:
        max_sig, min_sig = sig.max(), sig.min()
        max_bg, min_bg = bg.max(), bg.min()
        bin_max, bin_min = max(max_sig, max_bg), min(min_sig, min_bg)
    bins = np.linspace(bin_min, bin_max, 101)

    '''
    print ('sig: ', sig.shape, 'bg: ', bg.shape, 'mid: ', c.shape)
    if sig.shape[0] > 0:
        max_sig, min_sig = sig.max(), sig.min()
    else:
        max_sig, min_sig = 0, 0
    if bg.shape[0] > 0:
        max_bg, min_bg = bg.max(), bg.min()
    else:
        max_bg, min_bg = 0, 0
    if c.shape[0] > 0:
        max_c, min_c = c.max(), c.min()
    else:
        max_c, min_c = 0, 0
    bin_max, bin_min = max(max_sig, max_bg, max_c), min(min_sig, min_bg, min_c)
    bins = np.linspace(bin_min, bin_max, 101)
    '''

    # histogram
    hist_sig, bins = np.histogram(sig, normed=True, bins=bins)
    hist_c, bins = np.histogram(c, normed=True, bins=bins)
    hist_bg, bins = np.histogram(bg, normed=True, bins=bins)

    histo_sig_collector.append(hist_sig)
    histo_c_collector.append(hist_c)
    histo_bg_collector.append(hist_bg)
    bin_collector.append(bins)

histo_sig_collector = np.asarray(histo_sig_collector)
histo_c_collector = np.asarray(histo_c_collector)
histo_bg_collector = np.asarray(histo_bg_collector)
bin_collector = np.asarray(bin_collector)

np.savetxt("histo_sig_collector_mid_100.csv", histo_sig_collector, delimiter=',')
np.savetxt("histo_c_collector_mid_100.csv", histo_c_collector, delimiter=',')
np.savetxt("histo_bg_collector_mid_100.csv", histo_bg_collector, delimiter=',')
np.savetxt("bin_collector_mid_100.csv", bin_collector, delimiter=',')
