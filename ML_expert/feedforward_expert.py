import h5py
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

start = time.time()
filepath = '/phys/groups/tev/scratch4/users/chengni/'

f = h5py.File(filepath + 'gjj_Variables_expert.hdf5', 'r')

'''#for testing
f = h5py.File(filepath+'mygjj_Variables.hdf5', 'r')'''

X = f['high_input'][:, :]
y = f['y_input'][:, :]

# masking nan
print ('masking nan...')

mask = ~np.isnan(X).any(axis=0)

print(mask.shape)
print(X.shape)

X = X[:, mask[:],]
print(X.shape)


# Normalization
print ('Normalizing...')

scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(X)

# Train Test split and random shuffle
print ('Splitting train test sets...')

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=20)

# print(X_train.shape)
# print(y_train.shape)


end = time.time()
print (('prep time'), (end - start))

# Training...
from keras.layers import GRU, Highway, Dense, Dropout, MaxoutDense, Activation, Masking
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.utils import np_utils

#build the feedforward neutral network
model = Sequential()
#test 9 hidden layers
model.add(Dense(420, input_dim = X.shape[1], activation='relu'))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(3))
model.add(Activation("softmax"))

#train the model
print("train the model...")
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=100, batch_size=100)

#predict
y_hat = model.predict(X_test, batch_size=100)

'''ROC Curve (Recall)
True Positive Rate (tpr) = TP / P = TP / (TP + FN)
False Positive Rate (fpr) = FP / N = FP / (FP + TN) = 1 - TN / (FP + TN)

for classification:
TPR = P(test positive | is bottom jet)
FPR = P(test negative | not bottom jet)

Finding TPR:
Set probability Threshold
collect all the true signal in y
for corresponding y_hat, see how many y_hats are above Threshold'''

#output the result

tpr = []
fpr = []

for i in range(100):
    th = i / float(100)
    TP = np.sum((y_hat[:, 2] >= th) * y_test[:, 2])
    tpr.append(TP / float(np.sum(y_test[:, 2])))

    TN = np.sum((y_hat[:, 2] < th) * (1 - y_test[:, 2]))
    fpr.append(1 - TN / float(np.sum(y_test[:, 0] + y_test[:, 1])))

tpr = np.concatenate([[0.0], tpr])
fpr = np.concatenate([[0.0], fpr])

tprc = []
fprc = []

for i in range(100):
    th = i / float(100)
    TP = np.sum((y_hat[:, 1] >= th) * y_test[:, 1])
    tprc.append(TP / float(np.sum(y_test[:, 1])))

    TN = np.sum((y_hat[:, 1] < th) * (1 - y_test[:, 1]))
    fprc.append(1 - TN / float(np.sum(y_test[:, 0] + y_test[:, 2])))

tprc = np.concatenate([[0.0], tprc])
fprc = np.concatenate([[0.0], fprc])

np.savetxt("tpr_expert_9L.csv", np.sort(tpr), delimiter=',')
np.savetxt("fpr_expert_9L.csv", np.sort(fpr), delimiter=',')
np.savetxt("tprc_expert_9L.csv", np.sort(tprc), delimiter=',')
np.savetxt("fprc_expert_9L.csv", np.sort(fprc), delimiter=',')
