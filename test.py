#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from sklearn import metrics
from sklearn.cluster import KMeans
from ClusteringValidity import ClusteringValidity
from FuzzyCMeans import FuzzyCMeans
from ExternalClusteringValidity import RandIndex, AdjustedRandIndex, JaccardCoefficient

def input_data():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    data = pd.read_csv(file_path,header=0)
    return data

if __name__ == '__main__':
    print("FUZZY C MEANS CLUSTERING ALGORITHM:")
    print("WARNING:")
    print("\t1: Make sure that the data fields are numeric")
    print("\t2: If your datasets have been labeled. Make sure the column containing the data label is in the LAST column of datasets")
    print("\t3: If your datasets have ID field. Make sure the column containing the data ID is in the FIRST column of datasets")
    print("Let's choose your csv file , do you want to open a file (y/n) ?:", end =' ')
    bools = input()
    if bools == "n":
        exit()
    
    df_full = input_data()
    columns = list(df_full.columns)
    print("\nDatasets have been labeled (y / n)?: ", end = ' ')
    check_labels = input(); original_labels = None

    if check_labels == 'y' or check_labels == 'Y':
        original_labels = list(map(str, df_full[columns[-1]]))
        print("Original Labels:")
        print(original_labels)
        df_full.drop(columns[-1], axis=1, inplace=True)
        del columns[-1]
    print("\nDatasets have ID field (y / n)?:", end = ' ')
    check_id = input()
    if check_id == 'y' or check_id == 'Y':
        df_full.drop(columns[0], axis=1, inplace=True)
        del columns[0]
    df = df_full.dropna()
    df = df[columns]
    df = pd.get_dummies(df, dtype=float)
    df = df.dropna()
    data_frame = np.asarray(df, dtype=float)
    #number of data points
    N = len(data_frame)
    print("Dataset:")
    print(data_frame)
    
    K = 2
    while True:
        print("How many cluster do you want? import (K is integer, N is length of datasets, 1 < K < N) K = ", end = '')
        K1 = int(input())
        if 1 < K1 <= N:
            K = K1
            break
    
    #condition for terminate
    epsilon = 1e-4
    while True:
        print("Select the stop condition (1e-4 <= epsilon <= 1e-3): epsilon = ", end = '')
        e = float(input())
        if e <= 1e-3 and e >= epsilon:
            epsilon = e
            break
    
    #Fuzzy parameter
    m = 2.35
    while True:
        print("Select the fcm parameter (1.5 < m < 3.0): m = ", end = ' ')
        m1 = float(input())
        if 1.5 < m1 < 3.0:
            m = m1
            break
    
    
    my_clustering = FuzzyCMeans(m, data_frame, N, K, epsilon)
    my_cluster_centers, my_labels = my_clustering.FCM()
    print("Cluster labels = ", my_labels)
    my_compute_ind = ClusteringValidity(data_frame, K, N, my_labels)
    
    """
    kmeans_clustering = KMeans(n_clusters=3, random_state=0).fit(data_frame)
    kmeans_centers, kmeans_labels = kmeans_clustering.cluster_centers_, kmeans_clustering.labels_
    #print(kmeans_labels)
    #compute_idx_kmeans = ClusteringValidity(data_frame, K, N, kmeans_labels)
    """
    
    print("\n\n----------START CLUSTERING VALIDITY----------")
    print("\n\n***Relative Clustering Validity Criteria***\n")
    print("1: Davies-Bouldin Index:")
    print("\tMY_PROGRAM = ", my_compute_ind.DB_idx())
    #print("\tSKLEARN.KMeans = ", compute_idx_kmeans.DB_idx())
    
    print("-------------------")
    print("2: Calinski-Harabasz Index:")
    print("\tMY_PROGRAM = ", my_compute_ind.VRC_idx())
    #print("\tSKLEARN = ", compute_idx_kmeans.VRC_idx())
    
    print("-------------------")
    print("3: Dunn Index:")
    print("\tMY_PROGRAM = ", my_compute_ind.DN_idx())
    #print("\tSKLEARN = ", kmeans_DN_idx.DN_idx())
    
    print("-------------------")
    print("4: Silhouette Width index:")
    print("\tMY_PROGRAM = ", my_compute_ind.SWC_idx())
    
    print("-------------------")
    print("5: Simplified Silhouette Width index:")
    print("\tMY_PROGRAM = ", my_compute_ind.SSWC_idx())
    
    print("-------------------")
    print("6: PBM index:")
    print("\tMY_PROGRAM = ", my_compute_ind.PBM_idx())
    
    print("-------------------")
    print("7: C index:")
    print("\tMY_PROGRAM = ", my_compute_ind.CI_idx())
    
    print("-------------------")
    print("8: Point Biserial index:")
    print("\tMY_PROGRAM = ", my_compute_ind.PB_idx())
    
    print("-------------------")
    print("9: C per Sqrt(K) index:")
    print("\tMY_PROGRAM = ", my_compute_ind.CK_idx())
    
    
    
    if check_labels=='y' or check_labels=='Y':
        RandI = RandIndex(N, data_frame, original_labels, my_labels)
        AdjustedRandI = AdjustedRandIndex(N, data_frame, original_labels, my_labels)
        JaccardCoeff = JaccardCoefficient(N, data_frame, original_labels, my_labels)
        print("\n\n***External CLustering Validity Criteria***\n")
        print("1: Rand Index:")
        print("\tMY_PROGRAM = ", RandI.RI())
        
        print("-------------------")
        print("2: Adjusted Rand Index:")
        print("\tMY_PROGRAM = ", AdjustedRandI.ARI())
        
        
        print("-------------------")
        print("3: Jaccard Coefficient:")
        print("\tMY_PROGRAM = ", JaccardCoeff.JC())
    print("\n\n----------END CLUSTERING VALIDITY----------")
        
        
