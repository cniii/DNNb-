'''
high level variables (16):

['jet_pt', 'jet_eta',
'track_2_d0_significance', 'track_3_d0_significance',
'track_2_z0_significance', 'track_3_z0_significance',
'n_tracks_over_d0_threshold', 'jet_prob', 'jet_width_eta', 'jet_width_phi',
'vertex_significance', 'n_secondary_vertices', 'n_secondary_vertex_tracks',
'delta_r_vertex', 'vertex_mass', 'vertex_energy_fraction']

mid level variables (28) * max tracks (15):'''

mid_var = ['D0', 'Z0', 'PHI', 'THETA', 'QOVERP',
           'D0D0',
           'Z0D0', 'Z0Z0',
           'PHID0', 'PHIZ0', 'PHIPHI',
           'THETAD0', 'THETAZ0', 'THETAPHI', 'THETATHETA',
           'QOVERPD0', 'QOVERPZ0', 'QOVERPPHI', 'QOVERPTHETA', 'QOVERPQOVERP',
           'track_weight',
           'mass', 'displacement', 'delta_eta_jet', 'delta_phi_jet',
           'displacement_significance', 'n_tracks', 'energy_fraction']

'''flavor (y):
signal --> y == 5
'''
import numpy as np
import matplotlib.pyplot as plt
import math


histo_sig = np.genfromtxt("histo_sig_collector_mid_100000000.csv", delimiter=',')
histo_bg = np.genfromtxt("histo_bg_collector_mid_100000000.csv", delimiter=',')
histo_c = np.genfromtxt("histo_c_collector_mid_100000000.csv", delimiter=',')
bino = np.genfromtxt("bin_collector_mid_100.csv", delimiter=',')


#histo_sig = np.ma.masked_where(np.nonzero(histo_sig), histo_sig)
'''
histo_bg = histo_bg[np.nonzero(histo_bg)]
histo_c = histo_c[np.nonzero(histo_c)]
'''

fig = plt.figure(figsize=(70, 40))
fig.suptitle('Mid Variables', fontsize=80)


for i in range(histo_sig.shape[0]):
  ax = fig.add_subplot(4, 7, i + 1)
  ax.set_yscale('log')
  ax.plot(bino[i, :][:-1], histo_sig[i, :], drawstyle='steps-post', color='blue', label='sig')
  ax.plot(bino[i, :][:-1], histo_bg[i, :], drawstyle='steps-post', color='red', label='bg')
  ax.plot(bino[i, :][:-1], histo_c[i, :], drawstyle='steps-post', color='green', label='c')
  ax.set_title(mid_var[i], fontsize=40)
  ax.legend(loc='upper right')

fig.savefig('mid_variables_100000000_test_log.png')
