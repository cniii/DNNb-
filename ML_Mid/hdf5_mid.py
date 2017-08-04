import numpy as np
import h5py

# input data path
filepath = '/phys/groups/tev/scratch4/users/kaifulam/dguest/gjj-pheno/v1/julian/raw_data'
# create the dst hdf5 file
f = h5py.File('/phys/groups/tev/scratch4/users/chengni/gjj_Variables_mid.hdf5', 'w')

# number of input data files
size = 10000000
var_num = 28
batch = 10000
group = size / batch

# Create dataset
dset_var = f.create_dataset('mid_variables', (1, 422, size))
dset_pid = f.create_dataset('mid_pid', (3, size))

# # create groups - 15 tracks
# for j in range(var_num):
#     g = f.create_group('track_' + str(j))

# write the data from src
for j in range(group):
    print '@group ' + str(j) + '/' + str(group)
    mid = np.empty([422, batch])
    pid = np.empty([3, batch])
    for k in range(batch):
        mid_tmp = np.load(filepath + '/saved_batches_test/clean_dijet_mid_' + str(j * batch + k) + '.npy')
        y = np.load(filepath + '/saved_batches_test/clean_dijet_y_' + str(j * batch + k) + '.npy')

        mid[:, k] = mid_tmp

        if y == 5:
            pid[:, k] = [0, 0, 1]
        elif y == 4:
            pid[:, k] = [0, 1, 0]
        else:
            pid[:, k] = [1, 0, 0]

    # put into the data set
    dset_var[:, :, j * batch: (j + 1) * batch] = mid
    dset_pid[:, j * batch: (j + 1) * batch] = y

# for j in range(15):
#     f['track_' + str(j)] = dset_var[:, j * 28: (j + 1) * 28, :]
