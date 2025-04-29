#!/bin/bash

###########################################
# nnU-Net Lesion Segmentation Script
# Author: Tammar Truzman
# This script runs chronic stroke lesion segmentation using pretrained nnU-Net models on T1-weighted images.
###########################################

############## ENVIRONMENT SETUP ##############

## 💡 One-time setup for conda environment:
# conda create -p /your/path/envs/lesion_segmentation python=3.11
# conda activate /your/path/envs/lesion_segmentation
# pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu118
# pip install git+https://github.com/MIC-DKFZ/nnUNet.git@v2.3.1
# pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git
# pip install nipreps antspyx nibabel SimpleITK numpy

############## START OF USER CONFIGURATION ##############

# 📁 Path to the main project directory — change this!
dirp=/your/full/path/to/your_project_folder/

# 🧠 Input T1w scan for segmentation — change this!
inputt1file="$dirp"/bids/sub-001/anat/sub-001_T1w.nii.gz

# no need to change. Loop for multiple subjects
ids=001
type=Patients
model=Dataset013_ATLASv2

############## SYSTEM VARIABLES ##############

conda activate "$dirp"/conda_env/lesion_segmentation

export OPENBLAS_NUM_THREADS=2
export GOTO_NUM_THREADS=2
export OMP_NUM_THREADS=2

export nnUNet_raw="$dirp"/raw
export nnUNet_preprocessed="$dirp"/preprocessed
export nnUNet_results="$dirp"/results
export CUDA_DEVICE_ORDER=PCI_BUS_ID

############## FOLDER SETUP ##############

outdir="$dirp"/work/nnunet/sub-"$ids"/anat/
tmpdir="$dirp"/work/tmp
mkdir -p "$dirp"/scripts
mkdir -p "$outdir" "$tmpdir"

############## FILE PREP ##############
t1=$(basename "$inputt1file")
sub=$(basename "$t1" .nii.gz)
cp "$inputt1file" "$tmpdir"/"$sub"_0000.nii.gz

############## MODEL INFERENCE (Ensemble of 2 architectures) ##############

# Run prediction with 3D full-resolution model
nnUNetv2_predict -d "$model" -i "$tmpdir" -o "$tmpdir"/"$sub"/MODEL_1 -f 0 1 2 3 4 -tr nnUNetTrainer -c 3d_fullres -p nnUNetPlans --save_probabilities -npp 12 -nps 12 -device cpu
# Run prediction with residual encoder-decoder variant
nnUNetv2_predict -d "$model" -i "$tmpdir" -o "$tmpdir"/"$sub"/MODEL_2 -f 0 1 2 3 4 -tr nnUNetTrainer -c 3d_fullres_resenc -p nnUNetPlans --save_probabilities -npp 12 -nps 12 -device cpu
# Ensemble predictions
nnUNetv2_ensemble -i "$tmpdir"/"$sub"/MODEL_1 "$tmpdir"/"$sub"/MODEL_2 -o "$tmpdir"/"$sub"/ -np 12

# Apply post-processing
nnUNetv2_apply_postprocessing -i "$tmpdir"/"$sub"/ -o "$tmpdir"/"$sub"/PP -np 12 \
-pp_pkl_file "$nnUNet_results"/"$model"/ensembles/ensemble___nnUNetTrainer__nnUNetPlans__3d_fullres___nnUNetTrainer__nnUNetPlans__3d_fullres_resenc___0_1_2_3_4/postprocessing.pkl \
-plans_json "$nnUNet_results"/"$model"/ensembles/ensemble___nnUNetTrainer__nnUNetPlans__3d_fullres___nnUNetTrainer__nnUNetPlans__3d_fullres_resenc___0_1_2_3_4/plans.json

############## FINAL PROCESSING ##############

# Convert probability outputs to usable lesion maps
python "$dirp"/scripts/probabilities_to_file.py --dirp "$dirp" --type "$type" --ids sub-"$ids" --model "$model" --pathtofile "$tmpdir"
# Mask prediction to brain-only (removes voxels outside brain)
python "$dirp"/scripts/mask_prediction.py --model "$dirp"/work/synthstrip.1.pt --pathtofile "$tmpdir"

# Copy outputs to final location
cp "$tmpdir"/"$sub".nii.gz "$outdir"/sub-"$ids"_run-01_T1w_label-lesion_roi.nii.gz
cp "$tmpdir"/data.nii.gz "$outdir"/sub-"$ids"_run-01_T1w_label-lesionprob_roi.nii.gz

############## DONE 🎉 ##############

echo "Segmentation complete! Check output in: $outdir"
