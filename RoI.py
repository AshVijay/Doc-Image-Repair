from keras.layers import Input, Conv2D, Dense, Flatten,MaxPooling2D,SeparableConv2D,Dropout,SpatialDropout2D
from keras.models import Model, Sequential
from keras.regularizers import l2
from keras import backend as K
from keras.optimizers import SGD,Adam
from keras.losses import binary_crossentropy
from keras.callbacks import EarlyStopping, TensorBoard, LearningRateScheduler, ModelCheckpoint
import numpy.random as rng
import para
import random
import copy
import time
import numpy as np
import tensorflow as tf
import keras
import generator
from keras.initializers import RandomNormal

input_shape=(40,38,1)

convnet = Sequential()
convnet.add(Conv2D(32,(5,5),activation='relu',input_shape=input_shape, kernel_initializer=RandomNormal(0,1e-2)
                   ,kernel_regularizer=l2(2e-4),bias_initializer=RandomNormal(0.5,1e-2)))

convnet.add(MaxPooling2D())
convnet.add(SpatialDropout2D(0.1))

convnet.add(Conv2D(64,(3,3),activation='relu', kernel_initializer=RandomNormal(0,1e-2)
                   ,kernel_regularizer=l2(2e-4),bias_initializer=RandomNormal(0.5,1e-2)))

convnet.add(MaxPooling2D())
convnet.add(SpatialDropout2D(0.1))

convnet.add(Conv2D(128,(3,3),activation='relu', kernel_initializer=RandomNormal(0,1e-2)
                   ,kernel_regularizer=l2(2e-4),bias_initializer=RandomNormal(0.5,1e-2)))

convnet.add(MaxPooling2D())
convnet.add(SpatialDropout2D(0.1))

convnet.add(Flatten())
convnet.add(Dropout(0.5))
convnet.add(Dense(512,activation="sigmoid", kernel_initializer=RandomNormal(0,1e-2)
                  ,kernel_regularizer=l2(1e-3),bias_initializer=RandomNormal(0.5,1e-2)))
convnet.add(Dense(2,activation='softmax',bias_initializer=RandomNormal(0.5,1e-2)))

optimizer = Adam(0.00006)

convnet.compile(loss="categorical_crossentropy",optimizer=optimizer, metrics=['accuracy'])

convnet.summary()
callback_list = []
train_name = str(int(time.time()))
callback_list.append(ModelCheckpoint(filepath=para.data_result_path+'/models/checkpoint_RoI.h5', monitor='val_loss', verbose=1, save_best_only=True,mode='auto'))
#callback_list.append(EarlyStopping(monitor='val_loss', patience=para.patience))
callback_list.append(TensorBoard(log_dir=para.data_result_path+'/logs/' + str(train_name),update_freq='epoch'))


train_generator = generator.RoIGenerator()
val_generator = generator.RoIGenerator()

convnet.fit_generator(epochs=para.epochs,
                generator=train_generator,
                steps_per_epoch=para.steps_per_epoch,
                validation_data=val_generator,
                validation_steps=400,
                callbacks=callback_list)
