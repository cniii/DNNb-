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
'''
_binning = {0: [0, 300], 1: [-3, 3], 2: [0, 2.5], 3: [0, 5],
            4: [0, 5], 5: [0, 5], 6: [0, 10], 7: [0, 0.04], 8: [0, 0.4], 9: [0, 0.4],
            10: [0, 5], 11: [0, 10], 12: [0, 10], 13: [0, 7], 14: [0, 25], 15: [0, 5],
            16: [0, 100], 17: [0, 100], 18: [0, 100], 19: [0, 100], 20: [0, 100],
            21: [0, 100], 22: [0, 100], 23: [0, 100], 24: [0, 100], 25: [0, 100],
            26: [0, 100], 27: [0, 100], 28: [0, 100], 29: [0, 100]}
'''
import numpy as np
import h5py

'''
filepath = '/phys/groups/tev/scratch4/users/chengni/'
f = h5py.File(filepath + 'gjj_Variables_mid.hdf5', 'r')
'''
# for small dataset testing
filepath = '/Users/nhy/Desktop/DNN/Github_local/Simulation/Mid_level/gjj_Variables_mid.hdf5'
f = h5py.File(filepath, 'r')

# small dataset: 10x15
mid = f['mid_input'][0:10]
y = f['y_input'][0:10]

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

    var_sig = mid_sig_collect[:, :, k]
    var_c = mid_c_collect[:, :, k]
    var_bg = mid_bg_collect[:, :, k]

    # remove nan for plotting
    sig = var_sig[~np.isnan(var_sig)]
    bg = var_bg[~np.isnan(var_bg)]
    c = var_c[~np.isnan(var_c)]

    # create bins
    '''
    if k in _binning:
        bin_min, bin_max = _binning.get(k)
    else:
        max_sig, min_sig = sig.max(), sig.min()
        max_bg, min_bg = bg.max(), bg.min()
        max_c, min_c = c.max(), c.min()
        bin_max, bin_min = max(max_sig, max_bg, max_c), min(min_sig, min_bg, min_c)
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

np.savetxt("histo_sig_collector_mid.csv", histo_sig_collector, delimiter=',')
np.savetxt("histo_c_collector_mid.csv", histo_c_collector, delimiter=',')
np.savetxt("histo_bg_collector_mid.csv", histo_bg_collector, delimiter=',')
np.savetxt("bin_collector_mid.csv", bin_collector, delimiter=',')
