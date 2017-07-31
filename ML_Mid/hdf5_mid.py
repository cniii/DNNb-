import numpy as np
import h5py

# input data path
filepath = '/phys/groups/tev/scratch4/users/kaifulam/dguest/gjj-pheno/v1/julian/raw_data'
# create the dst hdf5 file
f = h5py.File('/phys/groups/tev/scratch4/users/chengni/gjj_Variables_mid.hdf5', 'w')

# number of input data files
size = 10000000
var_num = 28

# Create dataset
dset_var = f.create_dataset('mid_variables', (15, 28, size))
dset_pid = f.create_dataset('mid_pid', (3, size))

# create groups - 15 tracks
for j in range(var_num):
    g = f.create_group('track_' + str(j))

# write the data from src
for j in range(size):
    if j % 1000 == 0:
        print 'loading #' + str(j)

    mid = np.empty([15, 28])
    pid = np.empty([3])

    mid_tmp = np.load(filepath + '/saved_batches_test/clean_dijet_mid_' + str(j) + '.npy')
    y = np.load(filepath + '/saved_batches_test/clean_dijet_y_' + str(j) + '.npy')

    for k in range(15):
        mid[k, :, :] = np.resize(np.transpose(mid_tmp[28 * k: 28 * (k + 1), [28])
    if y == 5:
        pid[:] = [0, 0, 1]
    elif y == 4:
        pid[:] = [0, 1, 0]
    else:
        pid[:] = [1, 0, 0]

    # put into the data set
    dset_var[:, :, j] = mid
    dset_pid[:, j] = y

for j in range(15):
    f['track_' + str(j)] = dset_var[j, :, :]
