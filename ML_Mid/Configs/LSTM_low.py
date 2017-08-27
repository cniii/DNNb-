import h5py
import numpy as np
import time
from sklearn.model_selection import train_test_split

start = time.time()
filepath = '/phys/groups/tev/scratch4/users/chengni/'

#filepath = '/Users/nhy/Desktop/DNN/DNNb/low_level/Data/'

f = h5py.File(filepath + 'gjj_Variables_low.hdf5', 'r')

'''#for testing
f = h5py.File(filepath+'mygjj_Variables.hdf5', 'r')'''

X = f['mid_input'][0:10000000, :]
y = f['y_input'][0:10000000, :]

# X = np.array(X_input)
# y = np.array(y_input)

#reshape the array
# X = np.reshape(X, (X.shape[0], 420))



# masking nan
print ('masking nan...')

mask = ~np.isnan(X).any(axis=0)
mask = mask[0, :]

print(mask.shape)
print(X.shape)

X = X[:, :, mask[:]]
print(X.shape)

# Normalization
print ('Normalizing...')

for i in range(X.shape[2]):
    var = X[:, :, i]
    var = (var - np.mean(var)) / np.std(var)
    X[:, :, i] = var

# Train Test split and random shuffle
print ('Splitting train test sets...')

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=20)

# print(X_train.shape)
# print(y_train.shape)

# X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1]))
# y_train = np.reshape(y_train, (y_train.shape[0], y_train.shape[1]))

end = time.time()
print (('prep time'), (end - start))

# Training...
from keras.layers import GRU, Dense, Dropout, MaxoutDense, Activation, Masking, Embedding, LSTM
from keras.models import Sequential
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import SGD
from keras.utils import np_utils

#build the LSTM neutral network
model = Sequential()
model.add(LSTM(420, input_shape=(X_train.shape[1], X_train.shape[2]), dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(X.shape[1], input_dim = X.shape[1], activation='relu'))
model.add(Dense(X.shape[1], activation='relu'))
model.add(Dense(3, activation='sigmoid'))

#train the model
print("train the model...")
sgd = SGD(lr=2e-3, decay=1e-4, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])
model.fit(X_train, y_train, epochs=100, batch_size=100)

# try:
#     history = model.fit(X_train, y_train, batch_size=100,
#                         callbacks=[
#                             # EarlyStopping(verbose=True, patience=20),
#                             ModelCheckpoint(filepath, monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1)
#                         ],
#                         epochs=100
#                         )

# except KeyboardInterrupt:
#     print('Training ended early.')

# print("history keys", history.history.keys())

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

np.savetxt("tpr_lstm.csv", np.sort(tpr), delimiter=',')
np.savetxt("fpr_lstm.csv", np.sort(fpr), delimiter=',')
np.savetxt("tprc_lstm.csv", np.sort(tprc), delimiter=',')
np.savetxt("fprc_lstm.csv", np.sort(fprc), delimiter=',')
