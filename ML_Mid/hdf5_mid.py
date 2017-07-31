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
dset = f.create_dataset('mid_variables')
dset = f.create_dataset('mid_pid')

# create groups - 15 tracks
for j in range(var_num):
    g = f.create_group('track_' + 1)

# write the data from src
for j in range(size):
    var = np.load(filepath + '/saved_batches_test/clean_dijet_mid_' + str(k * n_batch + i) + '.npy')
    pid = np.load(filepath + '/saved_batches_test/clean_dijet_y_' + str(k * n_batch + i) + '.npy')


'''
n_samples = 10000000
# n_samples = n_samples / 100 #less reps for testing purposes
n_batch = 10000
n_rep = n_samples / n_batch

dset_mid = f.create_dataset('mid_input', (n_samples, 15, 28), maxshape=(None, 15, 28))
dset_y = f.create_dataset('y_input', (n_samples, 3), maxshape=(None, 3))

# another for loop for n_samples
for k in range(n_rep):
    print 'k = ', k

    X_input = np.empty([n_batch, 15, 28])
    y_input = np.empty([n_batch, 3])

    for i in range(0, n_batch, 15):
        if i % 1000 == 0:
            print ('@line number i = ', i)

        # load mid-level numpy files
        print('loading clean_dijet_mid_' + str(k * n_batch + i) + '.npy')
        mid = np.load(filepath + '/saved_batches_test/clean_dijet_mid_' + str(k * n_batch + i) + '.npy')
        print 'loading y...'
        y = np.load(filepath + '/saved_batches_test/clean_dijet_y_' + str(k * n_batch + i) + '.npy')

        # loop over the 15 groups
        for j in range(15):
            print("loading@ j = ", j)
            X_input[i, j, :] = mid[0, 2 + j * 28: 2 + (j + 1) * 28]

        #X_input[i, :, :] = mid
        # y==5 is b jet signal; y==4 is c jet signal; For y: column 0 background, column 1 charm, column 2 bottom
        if y == 5:
            y_input[i, :] = [0, 0, 1]
        elif y == 4:
            y_input[i, :] = [0, 1, 0]
        else:
            y_input[i, :] = [1, 0, 0]

    # remove nan
    X_input = X_input[~np.isnan(X_input)]

    # Set hdf5 dataset
    dset_mid[0 + k * n_batch: (1 + k) * n_batch, ...] = np.asarray(X_input)
    dset_y[0 + k * n_batch: (1 + k) * n_batch, ...] = np.asarray(y_input)
'''
