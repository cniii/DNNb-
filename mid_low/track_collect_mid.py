'''
high level variables (16):

[jet_pt, jet_eta,
track_2_d0_significance, track_3_d0_significance,
track_2_z0_significance, track_3_z0_significance,
n_tracks_over_d0_threshold, jet_prob, jet_width_eta, jet_width_phi,
vertex_significance, n_secondary_vertices, n_secondary_vertex_tracks,
delta_r_vertex, vertex_mass, vertex_energy_fraction]

mid level variables (28) * max tracks (15):

[D0, Z0, PHI, THETA, QOVERP,
D0D0,
Z0D0, Z0Z0,
PHID0, PHIZ0, PHIPHI,
THETAD0, THETAZ0, THETAPHI, THETATHETA,
QOVERPD0, QOVERPZ0, QOVERPPHI, QOVERPTHETA, QOVERPQOVERP,
track_weight,
mass, displacement, delta_eta_jet, delta_phi_jet,
displacement_significance, n_tracks, energy_fraction]

flavor (y):
signal --> y == 5
'''

import numpy as np

filepath = '/phys/groups/tev/scratch4/users/kaifulam/dguest/gjj-pheno/v1/julian/raw_data'

jet_var_sig_collect = []
jet_var_bg_collect = []
mid_sig_collect = []
mid_bg_collect = []
y_collect = []

for i in range(10000000):
    if i % 10000 == 0:
        print '@line number k = ', i

    #high = np.load(filepath+'/saved_batches/clean_dijet_high_'+str(i)+'.npy')
    mid = np.load(filepath+'/saved_batches_test/clean_dijet_mid_'+str(i)+'.npy')
    y = np.load(filepath+'/saved_batches_test/clean_dijet_y_'+str(i)+'.npy')
    #print 'mid', mid

    if y == 5:
        jet_var_sig_collect.append(mid[:,0:2])
        mid = mid[:,2:]
        mid = np.reshape(mid, (15,28), order='C')
        mid_sig_collect.append(mid)
        #print 'jet_collect', jet_var_sig_collect
        #print 'mid_collect', mid_sig_collect
    else:
        jet_var_bg_collect.append(mid[:,0:2])
        mid = mid[:,2:]
        mid = np.reshape(mid, (15,28), order='C')
        mid_bg_collect.append(mid)

    y_collect.append(y)

jet_var_sig_collect = np.asarray(jet_var_sig_collect)
jet_var_bg_collect = np.asarray(jet_var_bg_collect)
mid_sig_collect = np.asarray(mid_sig_collect)
mid_bg_collect = np.asarray(mid_bg_collect)
y_collect = np.asarray(y_collect)

print 'jet_var_sig_collect.shape', jet_var_sig_collect.shape
print 'mid_sig_collect.shape', mid_sig_collect.shape
print 'mid_bg_collect.shape', mid_bg_collect.shape
print 'y_collect', y_collect

#below is for histogram
histo_sig_collector = []
histo_bg_collector = []
bin_collector = []


for k in range(mid_sig_collect.shape[2]):
    print k
    var_sig = mid_sig_collect[:,:,k]
    var_bg = mid_bg_collect[:,:,k]
    #trk_sig_wt = mid_sig_collect[:,:,20]
    #trk_bg_wt = mid_bg_collect[:,:,20]

    #remove nan for plotting, ##with corresponding wt
    ind_sig = ~np.isnan(var_sig)
    sig = var_sig[ind_sig]
    #sig_wt = trk_sig_wt[ind_sig]
    #print 'trk_wt', trk_wt
    ind_bg = ~np.isnan(var_bg)
    bg = var_bg[ind_bg]
    #bg_wt = trk_bg_wt[ind_bg]

    #create bins
    max_sig, min_sig = sig.max(), sig.min()
    max_bg, min_bg = bg.max(), bg.min()
    bin_max, bin_min = max(max_sig, max_bg), min(min_sig, min_bg)
    bins = np.linspace(bin_min, bin_max, 101)

    #histogram
    hist_sig, bins = np.histogram(sig, normed=True, bins=bins)
    hist_bg, bins = np.histogram(bg, normed=True, bins=bins)

    histo_sig_collector.append(hist_sig)
    histo_bg_collector.append(hist_bg)
    bin_collector.append(bins)

histo_sig_collector = np.asarray(histo_sig_collector)
histo_bg_collector = np.asarray(histo_bg_collector)
bin_collector = np.asarray(bin_collector)

print 'histo_sig_collector', histo_sig_collector.shape
print 'histo_bg_collector', histo_bg_collector.shape


np.savetxt("histo_sig_collector.csv", histo_sig_collector, delimiter=',')
np.savetxt("histo_bg_collector.csv", histo_bg_collector, delimiter=',')
np.savetxt("bin_collector.csv", bin_collector, delimiter=',')
