### Import module
import os, sys, stat
from shutil import move
import glob
import time
import shutil
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imshow
from skimage.restoration import denoise_tv_chambolle
import skimage
from skimage.transform import rescale, resize, downscale_local_mean
from skimage import data, color, img_as_uint
from skimage.measure import label, regionprops
from skimage.morphology import binary_erosion
from skimage.morphology import binary_dilation

from PIL import Image # for reading header information

from skimage.morphology import watershed, disk, ball

import pandas as pd

#### Import custom libraries
import sys
sys.path.insert(0, 'INSERT PATH TO THE FOLDER WHERE TOOLBOX IS SAVED')

import importlib
import toolbox as bf
importlib.reload(bf)
####


### Scan INPUT ################################################################
folder_input = 'INSERT PATH TO THE PARENT FOLDER WITH SCAN FOLDERS'



# additional parameters
ID_tag_length = 3
group_tag_length = 3

folders = glob.glob( os.path.join( folder_input, '*ID*') ) # ID is out search term
folders.sort()
print(len(folders))


for folder_number, fldr in enumerate(folders):
    print(fldr)
    if os.path.isdir(fldr):
        if '_aligned' in fldr:
            print('Already aligned..')
        else:
            new_name = fldr+'_aligned_'
            print(new_name)


            tag   = 'ID' + fldr[ (fldr.find('ID') + 2):(fldr.find('ID') + ID_tag_length + 2) ]
            group = 'g'  + fldr[ (fldr.find('g')  + 1):(fldr.find('g')  + group_tag_length + 1) ]
            print(tag)

            ### ALIGN CHANNELS
            print('Reading raw tiffs..')
            auto, spec = bf.readRawTiffs(fldr)

            if auto.shape[0] == spec.shape[0]:

                print('Aligning channels..')
                fail_count = 0
                for i in range(auto.shape[0]):
                    print(i)
                    temp_auto = auto[i,:,:]
                    temp_spec = spec[i,:,:]
                    bf.saveNifti(temp_auto, fldr + '/' + 'temp_auto.nii.gz')
                    bf.saveNifti(temp_spec, fldr + '/' + 'temp_spec.nii.gz')


                    # #def __init__(self, moving, fixed, elastix_path, result_path):
                    moving = fldr + '/' + 'temp_auto.nii.gz'
                    fixed = fldr + '/' + 'temp_spec.nii.gz'

                    #### NOTE: Working directory and paramter files for registrations
                    # ### CREATE A FOLDER "elastix"
                    # ### ADD A FOLDER "workingDir" along with registration parameter files in the "elastix" folder

                    elastix_path = 'INSERT FULL PATH TO A FOLDER CALLED "elastix"'
                    result_path = fldr
                    hu = bf.Huginn(moving,fixed,elastix_path,result_path)

                    ##def registration(params, result_name, init_trans=r'', f_mask=r'', save_nifti=True, datatype='uint16'):
                    try:
                        hu.registration('Par0000affine_cm_2d.txt', 'auto_aff_'+str(i), save_nifti=False, datatype='uint16')
                    except:
                        print("Registration failed..")
                        fail_count = fail_count+1

                # Change name of folder
                new_name = new_name+str(fail_count)
                os.rename(fldr, new_name)
