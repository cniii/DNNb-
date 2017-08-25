import numpy as np
import h5py


#path to the directory
filepath = '/phys/groups/tev/scratch4/users/kaifulam/dguest/gjj-pheno/v1/julian/raw_data'

#adjust number of input
n_samples = 10000000
n_batch = 100000
n_rep = n_samples / n_batch

#write into the h5py file with two dataset
f = h5py.File('/phys/groups/tev/scratch4/users/chengni/gjj_Variables_low_08.hdf5', 'w')
dset_mid = f.create_dataset('mid_input', (n_samples, 15, 28), maxshape=(None, 15, 28))
dset_y = f.create_dataset('y_input', (n_samples, 3), maxshape=(None, 3))

#loop over the variables in batches
for k in range(n_rep):
    print 'k = ', k

    #shape(X): n * 15 * 18
    #shape(y): n * 3
    X_input = np.empty([n_batch, 15, 28])
    y_input = np.empty([n_batch, 3])

    #each batch
    for i in range(0, n_batch):
        if i % 1000 == 0:
            print '@line number i = ', i

        # load mid-level numpy files
        print 'loading clean_dijet_mid_' + str(k * n_batch + i) + '.npy'
        mid = np.load(filepath + '/saved_batches_test/clean_dijet_mid_' + str(k * n_batch + i) + '.npy')
        print 'loading y...'
        y = np.load(filepath + '/saved_batches_test/clean_dijet_y_' + str(k * n_batch + i) + '.npy')

        # loop over the 15 groups
        for j in range(15):
            print("loading@ j = ", j)
            X_input[i, j, :] = mid[0, 2 + j * 28: 2 + (j + 1) * 28]

        # y==5 is b jet signal; y==4 is c jet signal; For y: column 0 background, column 1 charm, column 2 bottom
        if y == 5:
            y_input[i, :] = [0, 0, 1]
        elif y == 4:
            y_input[i, :] = [0, 1, 0]
        else:
            y_input[i, :] = [1, 0, 0]

    # Set hdf5 dataset
    dset_mid[0 + k * n_batch: (1 + k) * n_batch, ...] = np.asarray(X_input)
    dset_y[0 + k * n_batch: (1 + k) * n_batch, ...] = np.asarray(y_input)

#create four variable groups
track_var = dset_mid.create_group("track_variables")
track_covar = dset_mid.create_group("track_covariance")
track_wei = dset_mid.create_group("track_weight")
vertex_variables = dset_mid.create_group("vertex_variables")

track_var = dset_mid[:, :, 0 : 5]
track_covar = dset_mid[:, :, 5 : 20]
track_weight = dset_mid[:, :, 20]
vertex_variables = dset_mid[:, :, 21 : 28]
