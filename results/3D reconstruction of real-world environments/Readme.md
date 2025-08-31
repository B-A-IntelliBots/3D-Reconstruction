## 3D Reconstruction Results: Point Clouds & Textured Meshes  

After bench-marking, **DISK + LightGlue** was identified as the optimal Feature Extractor–Matcher combination within the HLoc pipeline. Using this configuration, the [Google Colab Hierarchical Localization](https://colab.research.google.com/drive/1MrVs9b8aQYODtOGkoaGNF9Nji3sbCNMQ) notebook is employed to generate the final 3D point cloud models of indoor environments (e.g., **Supermarket** and **Dormitory**).  

The resulting point cloud is then refined and undistorted using [COLMAP](https://github.com/colmap/colmap). Finally, [OpenMVS](https://github.com/cdcseacave/openMVS) is used to reconstruct high-quality 3D meshes from the point cloud, while associating them with the original images to create textured 3D models.  

The images below showcase both the raw 3D point clouds and the rendered textured-mesh reconstructions of the captured real-world environments.
<div align="center">
<img width="800" height="372" alt="3DMARKETpng" src="https://github.com/user-attachments/assets/5f4514b1-72ff-4f93-b8ee-7218f164632b" />

<img width="800" height="304" alt="3DReconstruction-modified" src="https://github.com/user-attachments/assets/7733d47a-da2a-47e6-aa44-cc5ea35e9b8e" />
</div>
