## Usage Guide

### 1. Feature Matching Data Logging

The script **`Extraction_Matching_data_logging.py`** is designed to log Feature-matched data between each query image and the captured database images. This process supports a deeper evaluation of different feature extraction and matching pipelines.

### What the script does:
- Logs the number of keypoints extracted from different feature extractors.
- Records the number of **inlier** and **outlier** matches between each pair of database images.
- Provides the foundation for computing the **pose accuracy** of the database cameras.

### Demo & Integration
To understand how this script is used in practice, you can follow the provided Google Colab demo: ➡️ ![](https://img.shields.io/badge/Open_in_Colab-blue?logo=google%20Colab&labelColor=gray&color=blue&link=https%3A%2F%2Fcolab.research.google.com%2Fdrive%2F1xQuMfWvgOEdBc6qVztHwKYVdp9CaD92e%23scrollTo%3Df6fbdb5c)

The demo illustrates how to integrate `Extraction_Matching_data_logging.py` into the sourced [Hierarchical Localization (HLOC)](https://colab.research.google.com/drive/1MrVs9b8aQYODtOGkoaGNF9Nji3sbCNMQ) Google Colab environment by inserting the script into the workflow.

---
### 2. Camera Pose Estimation
The script **`Camera_pose_estimation.py`** is designed to compare estimated camera extrinsic parameters (rotation and translation) against ground truth for selected viewpoints. It leverages advanced multiple-view-geometry metrics, including the **Fundamental** and **Essential** matrices.
<div align="center">
<img width="544" height="390" alt="Rlative Rotation and Translation" src="https://github.com/user-attachments/assets/464bea15-1e91-4521-ac76-f06599d002db" />
</div>

#### Key Functions
- Utilizes **`gt.py`** to extract ground-truth parameters (R, T) from the **`.h5`** file format ([Sagrada_Familia_Gd](https://github.com/B-A-IntelliBots/3D-Reconstruction/tree/main/data/Sagrada_Familia/Ground_Truth_Cemera_Extrinsics),[Abraham Lincoln Statue_Gd](https://github.com/B-A-IntelliBots/3D-Reconstruction/tree/main/data/Abraham-Lincoln-Statue/Ground_Truth_Cemera_Extrinsics),[Tree_Gd](https://github.com/B-A-IntelliBots/3D-Reconstruction/tree/main/data/Tree/Ground_Truth_Cemera_Extrinsics)).  
- Imports feature extraction and matching results with the following specifications:  
  - **`kp_q_queryID_databaseID_(Extractor+Matcher combination).txt`** ([1](https://github.com/B-A-IntelliBots/3D-Reconstruction/tree/main/data/Sagrada_Familia/Eval_kp_db_familia),[2](https://github.com/B-A-IntelliBots/3D-Reconstruction/tree/main/data/Abraham-Lincoln-Statue/Eval_kp_db_statue),[3](https://github.com/B-A-IntelliBots/3D-Reconstruction/tree/main/data/Tree/Eval_kp_db_Tree)) → keypoints from a query image and their corresponding matches in a database image.  
  - **`kp_db_databaseID_queryID_(Extractor+Matcher combination).txt`** → the inverse keypoint matches.
  - **(Extractor+Matcher combination)**: the type of Feature Extractor-Matcher {**`sl`**: SuperPoint+LightGlue, **`sift`**: Sift+NN_ratio, **`ss`**:SuperPoint+SuperGlue, **`disk`**: Disk+LightGlue}
- Computes the **rotation error** between the estimated and ground-truth rotations.  
- Computes the **translational direction error**, since the Essential matrix only provides the translation vector up to scale (making the exact relative translation magnitude unattainable).   
