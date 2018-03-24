
# coding: utf-8

# In[1]:


from part_1 import *
from part_1_verify import *
from data_restore import *
import random
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Conv2D, UpSampling2D, MaxPooling2D, Dropout, Activation
from keras.optimizers import SGD
import tensorflow as tf

class TrainModel(object):
    def __init__(self, masker):
        self.masker = masker
        self.restore = DataRestore()
        self.train_x = []
        self.train_y = []
        self.test_x = []
        self.test_y = []
        self.model = None
        self.verifier = Verifier(masker)
    
    def prepare_batch(self):
        # Extract dcm and mask file paths, and bound them in dictionary
        dcm_keys = []
        for (dirpath, dirnames, filenames) in walk(self.masker.dcm_folder):
            dcm_keys.extend(dirnames)
        
        mask_keys = []
        for (dirpath, dirnames, filenames) in walk(self.masker.mask_folder):
            mask_keys.extend(dirnames)
            
        dcm_mask_dict = {}
        for i in dcm_keys:
            for j in mask_keys:
                if i[4:14] == j[5:15]:
                    dcm_mask_dict[i] = j
        
        # Randomly select dcm and corresponding mask file, restore their data, use them as pair in batch
        train_x = []
        train_y = []
        test_x = []
        test_y = []
        # use 4 out of 5 patient's materials as training set
        for i in range(0, len(dcm_keys) - 1):
            dcm_chosen_key = dcm_keys[i]
            dcm_chosen_path = self.masker.dcm_folder + dcm_chosen_key + '/'
            dcm_names = []
            for (dirpath, dirnames, filenames) in walk(dcm_chosen_path):
                dcm_names.extend(filenames)
            for j in range(0, len(dcm_names) - 1):
                dcm_chosen_name = dcm_names[j]
                # restore dcm array
                dcm_file = dcm_chosen_path + dcm_chosen_name
                dcm = self.restore.restore_dcm(dcm_file)

                # restore corresponding mask array
                mask_key = dcm_mask_dict[dcm_chosen_key]
                mask_name = dcm_chosen_name
                mask_file = self.masker.mask_folder + mask_key + '/' + mask_name
                mask = self.restore.restore_mask(mask_file)

                # fill pair to batch
                train_x.append(dcm)
                train_y.append(mask)
        
        train_x = np.asarray(train_x)
        train_y = np.asarray(train_y)
        self.train_x = train_x.reshape(len(train_x),256,256,1)
        self.train_y = train_y.reshape(len(train_y),256,256,1)
        
        # use the last 1 patient's materials as testing set
        for i in range(len(dcm_keys) - 1, len(dcm_keys)):
            dcm_chosen_key = dcm_keys[i]
            dcm_chosen_path = self.masker.dcm_folder + dcm_chosen_key + '/'
            dcm_names = []
            for (dirpath, dirnames, filenames) in walk(dcm_chosen_path):
                dcm_names.extend(filenames)
            for j in range(0, len(dcm_names)):
                dcm_chosen_name = dcm_names[j]
                # restore dcm array
                dcm_file = dcm_chosen_path + dcm_chosen_name
                dcm = self.restore.restore_dcm(dcm_file)

                # restore corresponding mask array
                mask_key = dcm_mask_dict[dcm_chosen_key]
                mask_name = dcm_chosen_name
                mask_file = self.masker.mask_folder + mask_key + '/' + mask_name
                mask = self.restore.restore_mask(mask_file)

                # fill pair to batch
                test_x.append(dcm)
                test_y.append(mask)
        
        test_x = np.asarray(test_x)
        test_y = np.asarray(test_y)
        self.test_x = test_x.reshape(len(test_x),256,256,1)
        self.test_y = test_y.reshape(len(test_y),256,256,1)      
    
    def build_model(self):
        
        # link data

        model = Sequential()
        # Dense(64) is a fully-connected layer with 64 hidden units.
        # in the first layer, you must specify the expected input data shape:
        # here, 20-dimensional vectors.
        nb_filter = 1
        filter_size = 2
    
        model.add(Conv2D(nb_filter, filter_size, strides=(1, 1), padding='same', activation='relu',input_shape=(256, 256, 1),name='conv1-a'))
        model.add(MaxPooling2D(pool_size=(2, 2), name='pool1'))
        model.add(Conv2D(nb_filter, filter_size, strides=(1, 1), padding='same',activation='relu', name='conv2-a'))
        model.add(MaxPooling2D(pool_size=(2, 2), name='pool2'))
        model.add(Conv2D(nb_filter, filter_size, strides=(1, 1), padding='same',activation='relu', name='conv3-a'))
        model.add(MaxPooling2D(pool_size=(2, 2), name='pool3'))
        model.add(Conv2D(nb_filter, filter_size, strides=(1, 1), padding='same',activation='relu', name='conv4-a'))
        model.add(MaxPooling2D(pool_size=(2, 2), name='pool4'))
        model.add(Conv2D(nb_filter, filter_size, strides=(1, 1), padding='same',activation='relu', name='conv5'))
        model.add(UpSampling2D(size=(2, 2), data_format=None))
        model.add(Conv2D(nb_filter, filter_size, strides=(1, 1), padding='same',activation='relu', name='conv6'))
        model.add(UpSampling2D(size=(2, 2), data_format=None))
        model.add(Conv2D(nb_filter, filter_size, strides=(1, 1), padding='same',activation='relu', name='conv7'))
        model.add(UpSampling2D(size=(2, 2), data_format=None))
        model.add(Conv2D(nb_filter, filter_size, strides=(1, 1), padding='same',activation='relu', name='conv8'))
        model.add(UpSampling2D(size=(2, 2), data_format=None))
        model.add(Conv2D(nb_filter, filter_size, strides=(1, 1), padding='same',activation='relu', name='conv9'))

        model.compile(loss='squared_hinge',
                      optimizer='adam',
                      metrics=['accuracy'])
        
        self.model = model

    def train_model(self):
        self.model.fit(self.train_x, self.train_y, batch_size=8, shuffle=True, epochs=250)
    
    def evaluate_model(self):
        score = self.model.evaluate(self.train_x, self.train_y, verbose=0, batch_size = 8)
        print('Train score:', score[0])
        print('Train accuracy:', score[1])
        
        score = self.model.evaluate(self.test_x, self.test_y, verbose=0, batch_size = 8)
        print('Test score:', score[0])
        print('Test accuracy:', score[1])        
         
    def draw_prediction(self):
        predict_y = self.model.predict(self.test_x, batch_size=None, verbose=0, steps=None)
        
        print predict_y.shape
        predict = predict_y[0]
        print predict.shape

        self.verifier.draw_mask(predict)
        test_y = self.test_y[0]
        print test_y.shape
        self.verifier.draw_mask(test_y)
        
        

