## 1. Extractor Algorithms – Keypoint Analysis  

The number of extracted keypoints plays a vital role in 3D reconstruction, influencing both density and completeness of the final model. To evaluate this, we applied three feature extraction algorithms (**SIFT, DISK, and SuperPoint**) on multiple datasets:  

- **10 images** of the *Abraham Lincoln Memorial Statue*  
- **19 images** from the *Tree* dataset  
- **20 images** from the *Sagrada Familia* dataset  

(All datasets are sourced from [IMC 2020-2021](https://www.cs.ubc.ca/~kmyi/imw2020/data.html).)  

The resulting keypoint counts were summarized, for comparison, and visualized in the following **bar charts**: 
<div align="center">
<p float="left">
<img width="48%" alt="image" src="https://github.com/user-attachments/assets/6d378f00-4fbb-4280-8f80-ad879f84ad99" />
<img width="46.5%" alt="image" src="https://github.com/user-attachments/assets/acf4140d-48b5-4fa4-9441-77d2bcbca1b5" />
  
*Figure 1&2: The extracted keypoints from “the Abraham Lincoln statue” image set on the left, and “Tree” image set on the right.* 
<img width="500" height="232" alt="image" src="https://github.com/user-attachments/assets/3c3578d5-b87d-4c46-8e22-94f730ed0769" />

*Figure 3: The extracted keypoints from “Sagrada Familia” image set.*
</div>


## Keypoint Extraction Results  

The bar charts in Figs. (1,2,3) show the number of extracted keypoints (Y-axis) across image IDs (X-axis).  

- **Abraham Lincoln Memorial set**  
  - DISK consistently reaches the 5000-keypoint limit.  
  - SIFT yields fewer due to smooth, low-texture surfaces.  
  - SuperPoint slightly outperforms SIFT but remains below DISK.  

- **Tree set**  
  - DISK and SIFT both reach the maximum number of keypoints.  
  - SuperPoint extracts about half as many.  
  - Missing bars = unregistered images (unused in reconstruction), not zero keypoints.  
  - SIFT performs better in rich-texture environments, though DISK still leads.  

- **Sagrada Familia set**  
  - DISK extracts the most keypoints.  
  - SIFT follows, then SuperPoint.  

**Summary:**  
DISK consistently outperforms other extractors across all environments. SIFT is highly dependent on texture richness, while SuperPoint remains stable but below DISK.  

---

## 2. Matcher Algorithms – Inlier/Total Matches Analysis  

After keypoint extraction, matching algorithms identify correspondences between image pairs.  
- A higher **total match count** generally yields denser 3D reconstructions.  
- The **inlier/total match ratio** reflects accuracy, as inliers (validated by RANSAC) ensure consistent camera parameters and better 3D localization.  

We evaluated **three matchers** — **SuperGlue, LightGlue, and NN-ratio test** — using the same extractor (**SuperPoint**).  

For each dataset, two bar charts were generated:  
- **Left chart:** total matches per image pair  
- **Right chart:** inlier matches per image pair
<div align="center">
<img width="600" height="275" alt="image" src="https://github.com/user-attachments/assets/5c3a4715-f2b4-42e3-907a-a8f985f806c4" />
  
*Figure 4: Number of total&inlier matches of “the Abraham Lincoln memorial statue”.*

<img width="600" height="275" alt="image" src="https://github.com/user-attachments/assets/355a56de-4088-408d-b076-7a3de34c9030" />

*Figure 5: Number of total&inlier matches of “tree”.*

<img width="600" height="275" alt="image" src="https://github.com/user-attachments/assets/f2832b7e-f19d-48a2-99e1-acd0e1c6738d" />

*Figure 6: Number of total&inlier matches of “Sagrada Familia” .*

</div>

## Matcher Performance Analysis  

- **Abraham Lincoln Memorial (Fig. 4):**  
  - NN-ratio shows the weakest, sparsest performance.  
  - SuperGlue and LightGlue provide stable, consistent and the highest number of matches across image pairs.  
  - Inlier-to-total match ratios are acceptable for all algorithms.  
- **Tree dataset (Fig. 5):**  
  - NN-ratio improves due to rich textures, yielding more matches.  
  - SuperGlue and LightGlue consistently extract ~500 matches.  
  - LightGlue slightly outperforms SuperGlue in memory and computation.  
- **Sagrada Familia (Fig. 6):**  
  - All algorithms show similar trends.  
  - Inlier ratios converge to 1, likely due to the dataset’s environmental characteristics.

**Summary:**  
SuperGlue and LightGlue consistently outperform NN-ratio. Considering computational efficiency, **LightGlue** is selected as the preferred matcher.

---

## 4. Pose Estimation Error Metric  

To assess the accuracy of candidate combinations (e.g., **DISK+LightGlue**) in 3D reconstruction, we evaluate pose estimation quality using the **fundamental matrix**. This matrix encodes the relative **rotation** and **translation** between two cameras from matched keypoints.  

From the estimated fundamental matrix, we extract the rotation matrix and translation vector, which are then compared to ground truth data from the **Image Matching Challenge 2021**. The evaluation consists of two error types:  

- **Rotation Error**: Euler angles (Roll, Pitch, Yaw) from the estimated rotation are compared with ground truth using **Mean Squared Error**.  
- **Translation Error**: Since translation from the fundamental matrix is scale-ambiguous, the **angle between the estimated and normalized ground truth vectors** is used.

This metric is applied on every pair of the dataset (**Abraham Lincoln Memorial**, **Tree dataset**, **Sagrada Familia**) consistently across all combinations (SIFT+NN-ratio, SuperPoint+SuperGlue, SuperPoint+LightGlue) for a fair performance comparison.  
<div align="center">
<img width="600" height="257" alt="image" src="https://github.com/user-attachments/assets/c9ee9dc9-4a37-4ce8-b979-5a89b203b61b" />
  
*Figure 7: Rotation Euler Error for all image pairs.*

<img width="600" height="257" alt="image" src="https://github.com/user-attachments/assets/bbf276cf-de0c-482d-9f52-55ddfa8ddab3" />

*Figure 8: Translation vector angle Errors for all image pairs.*
</div>

To compare combinations fairly, a **harmonic mean** is employed, as it reduces the influence of outlier errors compared to the arithmetic mean.  

<p align="center" style="font-family: 'Cambria Math', 'STIXGeneral', 'Times New Roman', serif; font-size: 16px;">
HM = n / ( &Sigma;<sub>i=1</sub><sup>n</sup> (1 / x<sub>i</sub>) )
</p>

The table below reports the harmonic mean of rotation and translation errors for each combination across all pairs
<div align="center">
<img width="600" height="150" alt="image" src="https://github.com/user-attachments/assets/2e86d7fe-4716-47ce-b510-fddf1ccd7bab" />
</div>

## Conclusion: the Optimal Combination  

According to the preceding Table, **Disk+LightGlue** achieves the lowest harmonic mean in rotation error, followed by **SuperPoint+LightGlue**. For translation error, **SuperPoint+LightGlue** performs best, with Disk+LightGlue close behind. Despite this, Disk+LightGlue excels in both rotation accuracy and the number of triangulated keypoints, making it the **optimal choice for 3D reconstruction**. Besides, the following images further visually confirm this observed trend.
<div align="center">
<img width="800" height="670" alt="image" src="https://github.com/user-attachments/assets/a8a8fc48-e780-431c-8ff0-83b2a53e9c7e" />

<img width="800" height="666" alt="image" src="https://github.com/user-attachments/assets/e2c076ec-53df-4ff0-819b-b72be6ea0176" />

</div>
