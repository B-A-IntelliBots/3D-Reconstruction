## Usage Guide

The script **`Extraction_Matching_data_logging.py`** is designed to log matching data between each query image and the captured database images. This process supports a deeper evaluation of different feature extraction and matching pipelines.

### What the script does:
- Logs the number of keypoints extracted from different feature extractors.
- Records the number of **inlier** and **outlier** matches between each pair of database images.
- Provides the foundation for computing the **pose accuracy** of the database cameras.

### Demo & Integration
To understand how this script is used in practice, you can follow the provided Google Colab demo: ➡️ ![](https://img.shields.io/badge/Open_in_Colab-blue?logo=google%20Colab&labelColor=gray&color=blue&link=https%3A%2F%2Fcolab.research.google.com%2Fdrive%2F1xQuMfWvgOEdBc6qVztHwKYVdp9CaD92e%23scrollTo%3Df6fbdb5c)

The demo illustrates how to integrate `Extraction_Matching_data_logging.py` into the sourced [Hierarchical Localization (HLOC)](https://colab.research.google.com/drive/1MrVs9b8aQYODtOGkoaGNF9Nji3sbCNMQ) Google Colab environment by inserting the script into the workflow.

---
