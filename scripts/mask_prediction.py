#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 23:19:37 2023

@author: ah08
"""

import os
import argparse
import numpy as np
from nipreps.synthstrip.wrappers.nipype import SynthStrip
import ants
import glob
import nibabel as nib


parser = argparse.ArgumentParser(description="Mask automated predicted lesion to brain only (i.e., remove regions outside of brain)",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--pathtofile", type=str, help="nnUNet model name")
parser.add_argument("--model", type=str, help="nnUNet model name")
args = vars(parser.parse_args())
print(args)

# Set up parameters
pathtofile = args["pathtofile"]
model = args["model"]

os.chdir((os.path.join(pathtofile)))

t1file=glob.glob((os.path.join(pathtofile,'*0000.nii.gz')))
nu=os.path.join(pathtofile,'T1_nu.nii.gz')
brain=os.path.join(pathtofile,'T1_brain.nii.gz')
image = ants.image_read(t1file[0])

# Run N4 correction
n4 = ants.abp_n4(image)
ants.image_write(n4, nu)

# Run SynthStrip for skull stripping
synthstrip = SynthStrip()
output_image = synthstrip.run(in_file=nu, model=model, num_threads=16)

# Load input 
pred = nib.load(t1file[0].replace('_0000', ''))
mask=nib.load(output_image.outputs.out_mask)

# Get image data arrays
data1 = pred.get_fdata()
data2 = mask.get_fdata()

# Multiply the images together
union = data1 * data2
binary_mask = (union > 0).astype(np.uint8)

# Save the binary mask as a new NIfTI file
binary_mask_nii = nib.Nifti1Image(binary_mask, affine=pred.affine, header=pred.header)
nib.save(binary_mask_nii, t1file[0].replace('_0000', ''))

