#! /usr/bin/env python

import cPickle, gzip
import numpy as np
from matplotlib.pyplot import imshow
from utils import *

from keras.models import Sequential
from keras.optimizers import SGD
from keras.utils import np_utils
from keras.layers.core import Activation,Flatten,Dropout,Dense
from keras.layers.convolutional import Convolution2D,MaxPooling2D
from keras.utils.visualize_util import plot

# Load the dataset  
num_classes = 10
X_train, y_train, X_test, y_test = getMNISTData()

# Rehape the data back into a 1x28x28 image.  
X_train = np.reshape(X_train, (X_train.shape[0], 1, 28, 28))
X_test = np.reshape(X_test, (X_test.shape[0], 1, 28, 28))

# Categorize the labels  
y_train = np_utils.to_categorical(y_train, num_classes)
y_test = np_utils.to_categorical(y_test, num_classes)

# Design the model  
model = Sequential()
model.add(Convolution2D(nb_filter=32, nb_row=3, nb_col=3, input_shape=(1, X_train.shape[2], X_train.shape[3])))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Convolution2D(nb_filter=64, nb_row=3, nb_col=3))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
# Add a fully-connected layer  
model.add(Dense(output_dim=128))
model.add(Dropout(0.5))
# Add another fully-connected layer with 10 neurons, one for each class of labels.  
model.add(Dense(output_dim=10))
# Add a softmax layer to force the 10 outputs to sum up to one so that we have a probability representation over the labels.  
model.add(Activation("softmax"))

model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True))

# Fit the model (10% of training data used as validation set).  
model.fit(X_train, y_train, nb_epoch=10, batch_size=32, validation_split=0.1, show_accuracy=True)

# Evaluate the model on test data.  
objective_score = model.evaluate(X_test, y_test, show_accuracy=True, batch_size=32)
print(objective_score)

model.save_weights('weights.h5')
