import numpy as np
import pandas as pd

descriptors={
    "A": [0.07, -1.73, 0.09],
    "V": [-2.69, -2.53, -1.29],
    "L": [-4.19, -1.03, -0.98],
    "I": [-4.44, -1.68, -1.03],
    "P": [-1.22, 0.88, 2.23],
    "F": [-4.92, 1.30, 0.45],
    "W": [-4.75, 3.65, 0.85],
    "M": [-2.49, -0.27, -0.41],
    "K": [2.84, 1.41, -3.14],
    "R": [2.88, 2.52, -3.44],
    "H": [2.41, 1.74, 1.11],
    "G": [2.23, -5.36, 0.30],
    "S": [1.96, -1.63, 0.57],
    "T": [0.92, -2.09, -1.40],
    "C": [0.71, -0.97, 4.13],
    "Y": [-1.39, 2.32, 0.01],
    "N": [3.22, 1.45, 0.84],
    "Q": [2.18, 0.53, -1.14],
    "D": [3.64, 1.13, 2.36],
    "E": [3.08, 0.39, -0.07],
}

def calculate_acc(z_descriptors, max_lag=5):
    """
    Calculates auto-covariance (Ajj) and cross-covariance (Cjk) terms for a given sequence of z-descriptors.
    
    Parameters:
    - z_descriptors: A (n x 3) numpy array where each row represents an amino acid and columns are z1, z2, z3 descriptors.
    - max_lag: Maximum lag to compute for ACC terms.
    
    Returns:
    - acc_features: A numpy array of shape (45,), containing the ACC terms for the protein sequence.
    """
    n, D = z_descriptors.shape  # n is sequence length, D should be 3 (z1, z2, z3)
    acc_features = []
    
    # Calculate mean of each z descriptor
    mean_descriptors = np.mean(z_descriptors, axis=0)
    
    # Cross-covariance terms (Cjk)
    acc_display=[]
    arr=[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    for j,k in arr:
        # for k in range(j + 1, D):  # Ensure j < k for unique pairs
        for lag in range(1, max_lag + 1,1):
            acc_sum = 0
            count = 0
            for i in range(n - lag):
                # acc_sum += (z_descriptors[i, j] - mean_descriptors[j]) * (z_descriptors[i + lag, k] - mean_descriptors[k])/(n-lag)
                sum = ((z_descriptors[i, j]) * (z_descriptors[i + lag, k]))/(n-lag)
                acc_sum+=sum
                count += 1
            # acc_features.append(acc_sum / count if count > 0 else 0)
            acc_features.append(acc_sum if count > 0 else 0)
            rep = f"({j+1},{k+1}) lag->{lag} = {acc_sum:.4f}"
            acc_display.append(rep)
            # Printing the acc matrix- (use for manual testing)
            # print(j+1,k+1," ",lag,"=",acc_sum)

    return np.array(acc_features),acc_display


def acc_predictor():
    # df=pd.read_csv('dataset/viral.csv')
    df=pd.read_csv("dataset/bacterial.csv")
    # Generate ACC features for training data
    df = df.dropna(subset=['label', 'sequence'])
    df = df.sort_values(by='swiss-prot')
    sequences = df['sequence']# Your actual sequences
    y = df['label'].map({"yes":1,"no":0}).values  # 1 for antigen, 0 for non-antigen
    X=[]
    for seq in sequences:
        z_descriptors=[]
        for a in seq:
            if(a in descriptors):
                z_descriptors.append(np.array(descriptors[a]))
        z_descriptors=np.array(z_descriptors)
        # # Compute ACC features
        acc_features = calculate_acc(z_descriptors, max_lag=5)
        X.append(acc_features)    
    X=np.array(X)
    print(X.shape)
    return X,y

def get_acc(seq):
    z_descriptors=[]
    for a in seq:
        if(a in descriptors):
            z_descriptors.append(np.array(descriptors[a]))
    z_descriptors=np.array(z_descriptors)

    # # Compute ACC features
    acc_features = calculate_acc(z_descriptors, max_lag=5)
    return acc_features