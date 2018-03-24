
# coding: utf-8

# In[ ]:


from os import walk
import re

class DataRestore(object):
    def __init__(self):
        pass
    
    def restore_coords_lst(self, coords_file):
        f = open(coords_file, 'r')
        coords_lst = f.read()
        coords_lst = eval(coords_lst)
        return coords_lst
    
    def restore_mask(self, mask_file):
        f = open(mask_file, 'r')
        mask = f.read()
        mask = re.sub(r'\]', '],', mask)
        mask = re.sub(r'\],\],', ']]', mask)
        mask = re.sub(r'e', 'e,', mask)
        mask = re.sub(r'e,\]', 'e]', mask)
        mask = eval(mask)
        return mask
        
    def restore_dcm(self, dcm_file):
        f = open(dcm_file, 'r')
        dcm = f.read()
        dcm = re.sub(r'array\(', '', dcm)
        dcm = re.sub(r', dtype=int16\)', '', dcm)
        dcm = re.sub(r'\{\'pixel_data\': ', '', dcm)
        dcm = re.sub(r'\}', '', dcm)
        dcm = eval(dcm)
        return dcm
        

    
    

