import h5py
import numpy as np
# Open the HDF5 file
def h5(x):
    with h5py.File(str(x)+'.h5', 'r') as hdf_file:
    # List all groups and datasets in the file
        K = hdf_file['K'];T = hdf_file['T'];R = hdf_file['R']  
        dataK = K[:];
        dataR = R[:];
        dataT = T[:];
        TT=np.zeros((3,1))
        TT[0]=dataT[0]
        TT[1]=dataT[1]
        TT[2]=dataT[2]
        return dataK,dataR,TT;
def gt_params(x):
    K,R,T=h5(x);
    return K,R,T;
