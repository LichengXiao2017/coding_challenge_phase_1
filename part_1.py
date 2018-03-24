
# coding: utf-8

# In[8]:


from parser import Parser
from os import walk
import os
import numpy as np
import csv
import re
import datetime



# In[12]:


class Masker(object):
    def __init__(self):
        self.parser = Parser()
        # image_folder is the location containing folders corresponding to patients' images
        self.image_folder = self.get_image_folder()
        # icontour_folder is the location containing folders corresponding to patients' icontours
        self.icontour_folder = self.get_icontour_folder()
        # dcm_folder is the location containing folders corresponding to patients' dcm(parsed image)
        self.dcm_folder = self.get_dcm_folder()
        # icontour_coords_lst_folder is the location containing folders corresponding to patients' icontour coords list
        self.icontour_coords_lst_folder = self.get_icontour_coords_lst_folder()
        # mask_folder is the location containing folders corresponding to patients' masks
        self.mask_folder = self.get_mask_folder()
        # initialize link dictionary between image and icontour folder id
        self.image_icontour_path_dict = {}
        self.log_path = ''
        self.new_link_path = ''
        self.new_link_name = ''
        self.new_link_content = []
        # enable printing all array elements
        np.set_printoptions(threshold='nan')
        
        self.get_image_icontour_link()
        self.initialize_log_path()
        self.initialize_new_link()
        
        
        self.mask = None
        self.coords_lst = None
        
        pass
    
    # method to get image folder
    def get_image_folder(self):
        # this part should be replaced by a function that allow the user to select and return folder location
        return 'final_data/dicoms/'
    
    # method to get icontour folder
    def get_icontour_folder(self):
        # this part should be replaced by a function that allow the user to select and return folder location
        return 'final_data/contourfiles/'
    
    # method to get dcm folder
    def get_dcm_folder(self):
        # this part should be replaced by a function that allow the user to select and return folder location
        return 'processed_data/dcm/'
    
    # method to get icontour coords list folder
    def get_icontour_coords_lst_folder(self):
        # this part should be replaced by a function that allow the user to select and return folder location
        return 'processed_data/icontour_coords_lst/'

    # method to get mask folder
    def get_mask_folder(self):
        # this part should be replaced by a function that allow the user to select and return folder location
        return 'processed_data/maskfiles/'

    # method to store the link between image and icontour folder id
    def get_image_icontour_link(self):
        with open('final_data/link.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.image_icontour_path_dict[row['patient_id']] = row['original_id']
     
    # initiliaze log path
    def initialize_log_path(self):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        log_path = 'logs/' + date + '/'
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.log_path = log_path
        
    # initialize new_link.csv file
    def initialize_new_link(self):
        self.new_link_path = 'processed_data/'
        self.new_link_name = 'new_link.csv'
        
    # Define method to write content to new file
    def write_new_file(self, string, file_name, path_name):
        file = open(path_name + str(file_name),'w') 
        file.write(str(string) + '\n') 
        file.close()
        
    # Define method to append content to the end of existing file
    def append_file(self, string, file_name, path_name):
        file = open(path_name + file_name,'a') 
        file.write(str(string) + '\n')
        file.close()

    # Define method to add mask folder id to new link file
    def add_new_link(self):
        with open('final_data/link.csv','r') as csvinput:
            with open(self.new_link_path + self.new_link_name, 'w') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator='\n')
                reader = csv.reader(csvinput)

                all = []
                row = next(reader)
                row.append('mask_id')
                all.append(row)

                for row in self.new_link_content:
                    all.append(row)

                writer.writerows(all)
        
    # Define method to generate mask files
    def get_mask(self):
        for key in self.image_icontour_path_dict.keys():
            # Extract image file names
            image_path = self.image_folder + key + '/'
            image_names = []
            for (dirpath, dirnames, filenames) in walk(image_path):
                image_names.extend(filenames)
    
            # Extract icontour file names
            icontour_path = self.icontour_folder + self.image_icontour_path_dict[key] + '/' + 'i-contours/'
            icontour_names = []
            for (dirpath, dirnames, filenames) in walk(icontour_path):
                icontour_names.extend(filenames)

            # Define coords_lst path
            coords_lst_key = 'COORDS_LST_' + key
            coords_lst_path = self.icontour_coords_lst_folder + coords_lst_key + '/'
            if not os.path.exists(coords_lst_path):
                os.makedirs(coords_lst_path)    
                
            # Define dcm path
            dcm_key = 'DCM_' + key
            dcm_path = self.dcm_folder + dcm_key + '/'
            if not os.path.exists(dcm_path):
                os.makedirs(dcm_path)
    
            # Define mask path
            mask_key = 'MASK_' + key
            mask_path = self.mask_folder + mask_key + '/'
            if not os.path.exists(mask_path):
                os.makedirs(mask_path)
                
                

            # Create new link
            self.new_link_content.append([key, self.image_icontour_path_dict[key], mask_key])

            # For each image file, if it has corresponding known icontour, parse the pair, save the mask file.
            for image_name in image_names:
                # Extract image id
                image_id = int(re.sub(r'\D', "", image_name))
                for icontour_name in icontour_names:
                    # Extract icontour id
                    icontour_id = int(icontour_name[8:12])
                    if icontour_id == image_id:
                        dcm_dict = self.parser.parse_dicom_file(image_path + image_name)
                        # store dcm as .txt file
                        dcm_name = str(image_id) + '.txt'
                        self.write_new_file(dcm_dict, dcm_name, dcm_path)
                        
                        coords_lst = self.parser.parse_contour_file(icontour_path + icontour_name)
                        # store coords_lst as .txt file
                        coords_lst_name = str(image_id) + '.txt'
                        self.write_new_file(coords_lst, coords_lst_name, coords_lst_path)    
                        
                        # width and height of mask is determined by colums and rows of image
                        mask = self.parser.poly_to_mask(coords_lst, dcm_dict['pixel_data'].shape[1], dcm_dict['pixel_data'].shape[0])
                        mask_name = str(image_id) + '.txt'
                        # store mask as .txt file
                        self.write_new_file(mask, mask_name, mask_path)
                        
                        # upgrade log
                        now = datetime.datetime.now()
                        log_name = now.strftime("%H:%M") + '.txt'
                        log_content = now.strftime("%Y-%m-%d %H:%M:%S") + ' created mask file ' + mask_path + mask_name + ' from ' + image_path + image_name + ' and ' + icontour_path + icontour_name
                        self.append_file(log_content, log_name, self.log_path)
                        
                        self.mask = mask
                        self.coords_lst = coords_lst                        
                        
        self.add_new_link()

