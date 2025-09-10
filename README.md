**Lesion-Segmentation-nnUNet**

Automated lesion segmentation of chronic stroke T1-weighted (T1w) MRI scans using nnU-Net.

This repository provides scripts and pretrained models fo automatically segmenting chronic stroke lesions from T1w images. You can apply our trained models to segment your own MRI scans.

- Input: Chronic T1w MRI of a stroke patient
- Output: Binary lesion map

📦 Download Pretrained Models & Resources

Please download the complete folder from the following link:
🔗 [https://universityofcambridgecloud-my.sharepoint.com/:f:/r/personal/ah2042_cam_ac_uk/Documents/AHalai/github/Lesion-Segmentation-nnUNet?csf=1&web=1&e=hbkt7B]

The folder includes three subdirectories:

* scripts/ – Shell scripts to run the segmentation pipeline
* work/ – Output directory where your results will be saved
* results/ – Pretrained nnU-Net model files

🚀 How to Run

Use the script _runlesionseg.sh_ to run the segmentation. 
Please see the script for:
* Required software installations
* Environment setup instructions

📖 **Citation**
If you use this resource in your research, please cite:

Truzman, T., Halai, A., & Lambon Ralph, M. A. (in prep). Lesion segmentation of acute and chronic stroke using nnU-Net.
