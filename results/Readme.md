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

*Figure 5: Number of total&inlier matches of “Sagrada Familia” .*

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

**Conclusion:**  
SuperGlue and LightGlue consistently outperform NN-ratio. Considering computational efficiency, **LightGlue** is selected as the preferred matcher.
