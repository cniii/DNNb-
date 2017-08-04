import numpy as np
import h5py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

f = h5py.File('/Users/nhy/Desktop/DNN/Github_local/Data/gjj_Variables_mid_100.hdf5', 'r')

mid_var = ['D0', 'Z0', 'PHI', 'THETA', 'QOVERP',
           'D0D0',
           'Z0D0', 'Z0Z0',
           'PHID0', 'PHIZ0', 'PHIPHI',
           'THETAD0', 'THETAZ0', 'THETAPHI', 'THETATHETA',
           'QOVERPD0', 'QOVERPZ0', 'QOVERPPHI', 'QOVERPTHETA', 'QOVERPQOVERP',
           'track_weight',
           'mass', 'displacement', 'delta_eta_jet', 'delta_phi_jet',
           'displacement_significance', 'n_tracks', 'energy_fraction']

mid_tracks = []

for j in range(15):
  for k in range(28):
    mid_tracks.append(mid_var[k] + '_track' + str(j + 1))


mid = f['mid_input'][:]

fig = plt.figure

k = 10

df = pd.DataFrame(data=mid[:, k - 1, :])

print(np.shape(df))

corr = df.corr()

print(np.shape(corr))

plt.title('Mid and Low Level Correlation_Track' + str(k))

sns.set(style="white")

sns.heatmap(corr, xticklabels=mid_var, yticklabels=mid_var, cmap="YlGnBu")

plt.yticks(rotation=0)
plt.xticks(rotation=90)

plt.savefig('Mid_Corr' + '_track' + str(k) + '.png')
