<div align="center">
  
# 3D Reconstruction

An end-to-end 3D reconstruction benchmark to identify the most effective combination of (feature extractor, feature matcher) in hierarchical localization pipelines using rigorous quantitative mathematical metrics.

![](https://img.shields.io/badge/v3.11-green?style=plastic&logo=python&label=Python3&labelColor=black&color=green)
</div>
<div align="center">
<img width="1759" height="670" alt="3DReconstruction-modified" src="https://github.com/user-attachments/assets/ffd49e92-56b4-43b8-a0fb-b6192f1f8d93" />
<img width="1180" height="250" alt="EXTRACTOR_MATCHER" src="https://github.com/user-attachments/assets/c873e968-21fb-49c0-9423-00bcf1dd3c3d" />
</div>


## 📖 Overview & Methodology
<div align="center">
<img width="587" height="303" alt="ThreeDReconstructionPipelinepng" src="https://github.com/user-attachments/assets/308e3d87-a716-467c-a4ac-7e35e1212544" />
</div>

This project introduces a **comprehensive benchmark** to evaluate and select the most effective combination of **feature extractors and feature matchers** in hierarchical localization pipelines.
The evaluation is based on the following key metrics:  
- ### Keypoint Extraction  
Measuring the number of keypoints detected by each feature extractor.  

- ### Inlier Matches & Point Cloud Density  
Assessing the number of inlier matches produced by different feature matchers (with a unified feature extractor). This is crucial since it affects the density of the point cloud generated after the triangulation stage occurs.

- ### Pose Accuracy
Comparing the estimated camera extrinsic parameters (*rotation* and *translation*) with the ground truth for specific viewpoints using advnaced metrics: ***fundamental and Essential matrices***. These, particularly, assist with quantifying the spatial & localization accuracy across each extractor–matcher combination.  

This methodology provides a **consistent and reliable framework for benchmarking**, ensuring a fair comparison of different approaches and guiding the selection of the **optimal pipeline configuration**. Ultimately, this leads to generating a **well-representative rendered mesh** through the **multi-view stereo (MVS) reconstruction pipeline**.  
