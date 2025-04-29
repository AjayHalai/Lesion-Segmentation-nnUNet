#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 23:19:37 2023

@author: ah08
"""

import os
import argparse
import numpy as np
import SimpleITK as sitk
import glob
import pickle
import nibabel as nib
import numpy as np

parser = argparse.ArgumentParser(description="Converts predicted lesion and write as probability map",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--pathtofile", type=str, help="nnUNet model name")
parser.add_argument("--model", type=str, help="nnUNet model name")
parser.add_argument("--ids", type=str, help="subject ID")
parser.add_argument("--type", type=str, help="population type")
parser.add_argument("--dirp", type=str, help="Directory to data")
args = vars(parser.parse_args())
print(args)

# Set up parameters
pathtofile = args["pathtofile"]
dirp = args["dirp"]
group = args["type"]
ids = args["ids"]
model = args["model"]

os.chdir((os.path.join(pathtofile)))

npz=glob.glob((os.path.join(pathtofile,'MODEL_1','*.npz')))
pkl=glob.glob((os.path.join(pathtofile,'MODEL_1','*.pkl')))

with open(pkl[0], 'rb') as f:
    properties = pickle.load(f)
    
npz_data = np.load(npz[0])
#note npz_data file contains a key "probabilities", which is a 4D matrix. I need 2nd volume 
npz_array = npz_data['probabilities']
datatowrite=npz_array[1,:,:,:]

#make sure file has high precision (can change depending on needs)
itk_image = sitk.GetImageFromArray(datatowrite.astype(np.float32))
#this information is taken from pickle file
itk_image.SetSpacing(properties['sitk_stuff']['spacing'])
itk_image.SetOrigin(properties['sitk_stuff']['origin'])
itk_image.SetDirection(properties['sitk_stuff']['direction'])

output_fname='data1.nii.gz'

sitk.WriteImage(itk_image, output_fname)


npz=glob.glob((os.path.join(pathtofile,'MODEL_2','*.npz')))
pkl=glob.glob((os.path.join(pathtofile,'MODEL_2','*.pkl')))
    
npz_data = np.load(npz[0])
#note npz_data file contains a key "probabilities", which is a 4D matrix. I need 2nd volume 
npz_array = npz_data['probabilities']
datatowrite=npz_array[1,:,:,:]

#make sure file has high precision (can change depending on needs)
itk_image = sitk.GetImageFromArray(datatowrite.astype(np.float32))
#this information is taken from pickle file
itk_image.SetSpacing(properties['sitk_stuff']['spacing'])
itk_image.SetOrigin(properties['sitk_stuff']['origin'])
itk_image.SetDirection(properties['sitk_stuff']['direction'])

output_fname='data2.nii.gz'

sitk.WriteImage(itk_image, output_fname)

# Load the two NIfTI files
img1 = nib.load('data1.nii.gz')
img2 = nib.load('data2.nii.gz')

# Extract data arrays from each file
data1 = img1.get_fdata(dtype=np.float32)
data2 = img2.get_fdata(dtype=np.float32)

# Calculate the average
average_data = (data1 + data2) / 2

# Convert to float32 explicitly to ensure lower file size
average_data = average_data.astype(np.float32)

# Create a new NIfTI image with the reduced precision data
average_img = nib.Nifti1Image(average_data, img1.affine)

# Save the averaged image to a new .nii.gz file
nib.save(average_img, 'data.nii.gz')