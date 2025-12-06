# Lesion-Segmentation-nnUNet

Automated lesion segmentation for chronic and acute stroke MRI using nnU-Net (v2.3.1).

This repository provides:
- Pretrained nnU-Net models
- Shell scripts to run the segmentation pipeline
- Utilities for probability maps and brain masking (SynthStrip)

You can apply our trained models to segment stroke lesions from your own MRI scans.

## Download Pretrained Models & Scripts (Required)

Please download the entire project folder from OneDrive:
🔗 [https://universityofcambridgecloud-my.sharepoint.com/:f:/r/personal/ah2042_cam_ac_uk/Documents/AHalai/github/Lesion-Segmentation-nnUNet?csf=1&web=1&e=hbkt7B]

This folder contains:

**scripts**/ segmentation scripts (acute + chronic)

**results**/ conatins pretrained nnU-Net model files
- Dataset013_ATLASv2/
  - chronic T1w model
- Dataset110_SOOPDWI/     
  - acute DWI+ADC model

**work/**  auto-created output workspace

## Environment Setup 

The segmentation pipeline requires a working nnU-Net environment (v2.3.1) with PyTorch and supporting libraries.

All required software installation steps and environment instructions are provided inside the scripts themselves:
- scripts/run_lesionseg.sh (chronic model)
- scripts/run_lesionseg_acute.sh (acute model)
  
📌 Please open the script and follow the instructions at the top to prepare your environment before running the pipeline.

## Chronic Stroke Lesion Segmentation (T1w MRI)

The chronic lesion model uses T1-weighted MRI only, trained on ATLAS v2.
- Script: scripts/run_lesionseg.sh
- Inputs Required: T1-weighted image (e.g., sub-001_T1w.nii.gz)
- Before running, open the script and edit the paths in the "USER CONFIGURATION" section.

**Run** the chronic pipeline: 
bash run_lesionseg.sh

This will:
- Preprocess the T1w image
- Run nnUNetv2 predictions from two architectures
- Ensemble predictions
- Apply postprocessing
- Output the lesion segmentation + probability map

## Acute Stroke Lesion Segmentation (DWI + ADC)
The acute model is trained on the SOOP-DWI dataset and requires two modalities: DWI Trace image & ADC map

- Script: scripts/run_lesionseg_acute.sh
- Inputs Required: DWI trace and DWI ADC for each subject
- Before running, open the script and edit the paths in the "USER CONFIGURATION" section.

**Run** the acute pipeline:
bash run_lesionseg_acute.sh

This will:
- preprocess DWI + ADC 
- Run nnUNetv2 predictions from two architectures
- Ensemble predictions
- Apply postprocessing
- Output the lesion segmentation + probability map
  
## Important Notes
- Acute and chronic models are **not interchangeable**
- Acute segmentation requires **both ADC and DWI Trace**
- Chronic segmentation uses **T1w only**
- Both models run under the same conda environment
- CPU prediction is slower; GPU recommended for acute segmentation

## Citation
If you use this resource in your research, please cite:

Truzman, T., Halai, A., & Lambon Ralph, M. A. (in prep). Lesion segmentation of acute and chronic stroke using nnU-Net.
