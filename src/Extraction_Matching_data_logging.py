#//////////////////////////
# for each pair of query keypoint and its matched 3D point,
# we need to find its corresponding keypoint in each database image
# that observes it. We also count the number of inliers in each.
import numpy as np
inliers = np.array(log["PnP_ret"]["inlier_mask"])
mkp_q = log["keypoints_query"]
n = len(log["db"])
kp_idxs, kp_to_3D_to_db = log["keypoint_index_to_db"]
counts = np.zeros(n)
dbs_kp_q_db = [[] for _ in range(n)]
inliers_dbs = [[] for _ in range(n)]
for i, (inl, (p3D_id, db_idxs)) in enumerate(zip(inliers, kp_to_3D_to_db)):
  track = model.points3D[p3D_id].track
  track = {el.image_id: el.point2D_idx for el in track.elements}
  for db_idx in db_idxs:
    counts[db_idx] += inl
    kp_db = track[log["db"][db_idx]]
    dbs_kp_q_db[db_idx].append((i, kp_db))
    inliers_dbs[db_idx].append(inl)
db_sort = np.argsort(-counts)
for db_idx in db_sort[:2]: # db_sort[:x], x here is the top xth db_idx with the highest num. of matches
   db = model.images[log["db"][db_idx]]
   db_name = db.name
   db_kp_q_db = np.array(dbs_kp_q_db[db_idx])
   kp_q = mkp_q[db_kp_q_db[:, 0]]
   kp_db = np.array([db.points2D[i].xy for i in db_kp_q_db[:, 1]])
   inliers_db = inliers_dbs[db_idx]
dim=np.shape(kp_q)
print(np.shape(kp_q))
file= open("/content/Hierarchical-Localization/datasets/sacre_coeur/kp_q.txt","w+") #rename kp_q.txt with kp_q_queryIDX_dbIDX_ExtractorMatcher.txt
for i in range(dim[0]):
  a=kp_q[i,0]
  b=kp_q[i,1]
  file.write(str(a))
  file.write(" ")
  file.write(str(b))
  file.write("\n")
file.close()
file= open("/content/Hierarchical-Localization/datasets/sacre_coeur/kp_db.txt","w+") #rename kp_db.txt with kp_db_dbIDX_qIDX_ExtractorMatcher.txt
for i in range(dim[0]):
  a=kp_db[i,0]
  b=kp_db[i,1]
  file.write(str(a))
  file.write(" ")
  file.write(str(b))
  file.write("\n")
file.close()
#//////////////////////////
