
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
from data_restore import DataRestore
from os import walk
import os
import re
import numpy as np


# In[5]:


class Verifier(object):
    def __init__(self, masker):
        self.masker = masker
        self.restore = DataRestore()

    # Define method to draw the output image of contour
    def draw_save_icontour(self, coords_lst, icontour_key, icontour_name):
        for coords in coords_lst:    
            x = coords[0]
            y = coords[1]
            plt.scatter(x, y)
        plt.xlim(0,255)
        plt.ylim(0,255)
        icontour_path = 'processed_data/icontour_coords_images/' + icontour_key + '/'
        if not os.path.exists(icontour_path):
            os.makedirs(icontour_path)
        plt.savefig(icontour_path + re.sub(r'\D', "", icontour_name) + '.png')
        print plt.show()
    
    # Similar method without saving .png file
    def draw_icontour(self, coords_lst):
        for coords in coords_lst:    
            x = coords[0]
            y = coords[1]
            plt.scatter(x, y)
        plt.xlim(0,255)
        plt.ylim(0,255)
        icontour_path = 'processed_data/icontour_coords_images/' + icontour_key + '/'
        if not os.path.exists(icontour_path):
            os.makedirs(icontour_path)
        plt.savefig(icontour_path + re.sub(r'\D', "", icontour_name) + '.png')
        print plt.show()
        
    # Define method to draw the output image of mask
    # It looks the same as contour image, so the contours are parsed correct
    # We can use statistical method to compare the accuracy of all contour-mask pairs to further verify it.
    def draw_save_mask(self, mask, mask_key, mask_name):
        for i in range(0, len(mask)):    
            for j in range(0, len(mask)):
                if mask[i][j] == True:
                    plt.scatter(j, i)
        plt.xlim(0,255)
        plt.ylim(0,255)
        mask_path = 'processed_data/mask_images/' + mask_key + '/'
        if not os.path.exists(mask_path):
            os.makedirs(mask_path)
        plt.savefig(mask_path + re.sub(r'\D', "", mask_name) + '.png')
        print plt.show()
     
    # Similar method without saving .png file
    def draw_mask(self, mask):
        for i in range(0, len(mask)):    
            for j in range(0, len(mask)):
                # if the probability of pixel being true is high, draw the dot
                if mask[i][j] > 0.9:
                    plt.scatter(j, i)
        plt.xlim(0,255)
        plt.ylim(0,255)
        print plt.show()

    def draw_icontour_and_mask(self):
        # Extract coords_lst and mask file paths, and bound them in dictionary
        coords_lst_keys = []
        for (dirpath, dirnames, filenames) in walk(self.masker.icontour_coords_lst_folder):
            coords_lst_keys.extend(dirnames)
        
        mask_keys = []
        for (dirpath, dirnames, filenames) in walk(self.masker.mask_folder):
            mask_keys.extend(dirnames)
            
        coords_lst_mask_dict = {}
        for i in coords_lst_keys:
            for j in mask_keys:
                if i[11:21] == j[5:15]:
                    coords_lst_mask_dict[i] = j
        
        # For each coords_lst and corresponding mask file, restore their data, draw and save .png graph
        for key in coords_lst_keys:
            coords_lst_path = self.masker.icontour_coords_lst_folder + key + '/'
            coords_lst_names = []
            for (dirpath, dirnames, filenames) in walk(coords_lst_path):
                coords_lst_names.extend(filenames)
            for name in coords_lst_names:
                coords_file = coords_lst_path + name
                coords_lst = self.restore.restore_coords_lst(coords_file)
                self.draw_save_icontour(coords_lst, key, name)

                mask_key = coords_lst_mask_dict[key]
                mask_name = name
                mask_file = self.masker.mask_folder + mask_key + '/' + mask_name
                mask = self.restore.restore_mask(mask_file)        
                self.draw_save_mask(mask, mask_key, mask_name)
            
        

