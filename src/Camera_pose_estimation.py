"""
Pose Estimation from Fundamental & Essential Matrix
---------------------------------------------------
This script estimates the relative camera pose (rotation & translation)
between two calibrated images using matched keypoints, the Fundamental matrix,
and the Essential matrix.

Steps:
1. Load camera intrinsics & extrinsics for query and database images.
2. Load keypoints detected in both images.
3. Estimate the Fundamental matrix using RANSAC.
4. Compute the Essential matrix using intrinsics.
5. Recover relative rotation and translation from the Essential matrix.
6. Compare estimated pose with ground truth pose.
"""

# ----------------------------- Imports -----------------------------------
import os
import math
import random
import csv
from glob import glob
from copy import deepcopy
from collections import namedtuple

import numpy as np
import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm

from gt import gt_params   # Ground-truth intrinsics & extrinsics

# Ensure correct OpenCV version
assert cv2.__version__ > "4.5", "OpenCV >= 4.5 is required"

# --------------------- Camera Intrinsics & Extrinsics ---------------------
# IDs of the two images under comparison
query_id = 10      # Query image ID
db_id = 19         # Database image ID
EM_type='sift' #the type of Feature Extractor-Matcher {sl: SuperPoint+LightGlue, sift: Sift+NN_ratio, ss:SuperPoint+SuperGlue, disk: Disk+LightGlue}

# Load intrinsics (K) and extrinsics (R, T) for query & database images
K_query, R_query, T_query = gt_params(query_id)
K_db, R_db, T_db = gt_params(db_id)

# -------------------------- Helper Functions ------------------------------

def euler_rotation_matrix(yaw, pitch, roll):
    """
    Compute a rotation matrix from Euler angles.
    Angles are given in degrees and converted to radians internally.

    Parameters:
    - yaw   : Rotation about Z-axis (degrees)
    - pitch : Rotation about Y-axis (degrees)
    - roll  : Rotation about X-axis (degrees)

    Returns:
    - R: 3x3 rotation matrix
    """
    yaw = math.radians(yaw)
    pitch = math.radians(pitch)
    roll = math.radians(roll)

    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])

    R_y = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])

    R_z = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw),  np.cos(yaw), 0],
        [0, 0, 1]
    ])

    return R_z @ R_y @ R_x


def rotation_matrix_to_euler_angles(R):
    """
    Convert a rotation matrix to Euler angles (roll, pitch, yaw) in degrees.
    Assumes ZYX rotation order.

    Parameters:
    - R: 3x3 rotation matrix

    Returns:
    - euler_angles: [roll, pitch, yaw] in degrees
    """
    sy = np.sqrt(R[0, 0]**2 + R[1, 0]**2)
    singular = sy < 1e-6

    if not singular:
        roll = np.arctan2(R[2, 1], R[2, 2])
        pitch = np.arctan2(-R[2, 0], sy)
        yaw = np.arctan2(R[1, 0], R[0, 0])
    else:
        roll = np.arctan2(-R[1, 2], R[1, 1])
        pitch = np.arctan2(-R[2, 0], sy)
        yaw = 0

    return np.array([roll, pitch, yaw]) * 180 / np.pi


def load_keypoints(filename):
    """
    Load 2D keypoints from a text file (Nx2).

    Parameters:
    - filename: path to file containing 2D coordinates

    Returns:
    - arr: numpy array of shape (N, 2)
    """
    with open(filename, "r") as file:
        lines = file.readlines()

    arr = np.zeros((len(lines), 2))
    for i, line in enumerate(lines):
        arr[i, :] = [float(num) for num in line.split()]

    return arr


def normalize_keypoints(keypoints, K):
    """
    Normalize keypoints using camera intrinsics.

    Parameters:
    - keypoints: (N,2) pixel coordinates
    - K: 3x3 intrinsic matrix

    Returns:
    - normalized_keypoints: (N,2)
    """
    Cx, Cy = K[0, 2], K[1, 2]
    fx, fy = K[0, 0], K[1, 1]
    return (keypoints - np.array([[Cx, Cy]])) / np.array([[fx, fy]])


def compute_essential_matrix(F, kp1, kp2):
    """
    Compute Essential matrix from Fundamental matrix and recover pose.

    Parameters:
    - F   : 3x3 Fundamental matrix
    - kp1 : (N,2) keypoints from query image
    - kp2 : (N,2) keypoints from database image

    Returns:
    - E: Essential matrix
    - R: Relative rotation (3x3)
    - T: Relative translation (3x1, up to scale)
    """
    E = (K_db.T @ F @ K_query).astype(np.float64)
    kp1n = normalize_keypoints(kp1, K_query)
    kp2n = normalize_keypoints(kp2, K_db)
    _, R, T, _ = cv2.recoverPose(E, kp1n, kp2n)
    return E, R, T


def rotation_error(R_est, R_gt):
    """
    Compute rotation error between estimated and ground truth rotations.

    Parameters:
    - R_est: estimated rotation matrix
    - R_gt : ground truth rotation matrix

    Returns:
    - error: rotation error (degrees, L2 norm over Euler differences)
    """
    diff = rotation_matrix_to_euler_angles(R_est) - rotation_matrix_to_euler_angles(R_gt)
    return np.linalg.norm(diff)


def translation_angle_error(T_est, T_gt):
    # This function computes the spatial angle between the estimated relative translation vector from the Essential Matrix and The ground Truth relative Translation Vector between two images
    # the angle between the two vectors is taken to be the evaluation metric since it is not attainable to get the exact relative estimated Translation vector from the Essential matrix as it yields mathematically a vector up-to-scale
    """
    Parameters:
    - T_est: estimated translation vector (3x1)
    - T_gt : ground truth translation vector (3x1)

    Returns:
    - angle_error: angle in degrees
    """
    cos_sim = float(np.dot(T_est.T, T_gt)) / (np.linalg.norm(T_est) * np.linalg.norm(T_gt))
    cos_sim = np.clip(cos_sim, -1.0, 1.0)  # numerical stability
    return math.degrees(math.acos(cos_sim))


# ------------------------------- Main -------------------------------------

if __name__ == "__main__":

    # Load matched keypoints between query and db images
    kp_query = load_keypoints(f"kp_q_{query_id}_{db_id}_{EM_type}.txt")
    kp_db = load_keypoints(f"kp_db_{db_id}_{query_id}_{EM_type}.txt")

    # Estimate Fundamental matrix using RANSAC
    F, mask = cv2.findFundamentalMat(
        kp_query, kp_db,
        method=cv2.USAC_MAGSAC,
        ransacReprojThreshold=0.25,
        confidence=0.99999,
        maxIters=10000
    )

    # Compute Essential matrix & recover relative pose
    _, R_est, T_est = compute_essential_matrix(F, kp_query, kp_db)

    # Ground truth relative pose between two images
    R_gt = R_db @ R_query.T
    T_gt = T_db - (R_gt @ T_query)

    # Print results
    print("Estimated Rotation:\n", R_est, "\n")
    print("Estimated Translation:\n", T_est, "\n")
    print("Ground Truth Rotation:\n", R_gt, "\n")
    print("Ground Truth Translation:\n", T_gt, "\n")

    # Compute and report errors
    print("Rotation matrix error (degrees):", rotation_error(R_est, R_gt))
    print("Translation vector angle error (degrees):", translation_angle_error(T_est, T_gt))
