#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from scipy.spatial import distance
import numpy as np
import sys


class C_per_sqrt_K:
    def __init__(self, data_frame, K, N, cluster_labels, cluster_centers=None, center=None, data_clusters=None):
        self.data_frame = data_frame
        self.K = K
        self.N = N
        self.cluster_centers = cluster_centers
        self.data_clusters = data_clusters 
        self.center = center
        self.cluster_labels = cluster_labels
        
    def compute_SST_SSW(self, q):
        SST_q = 0
        for i in range(self.N):
            absolute = np.abs(self.data_frame[i][q] - self.center[q]) ** 2
            SST_q = SST_q + absolute
        
        SSW_q = 0
        for l in range(self.K):
            Nl = len(self.data_clusters[l])
            Xlq = self.cluster_centers[l][q]
            for i in range(Nl):
                tmp = np.abs(self.data_clusters[l][i][q] - Xlq) ** 2
                SSW_q = SSW_q + tmp
        return SST_q, SSW_q
    
    def CK(self):
        n = self.data_frame.shape[1]
        res = 0
        for q in range(n):
            SST_q, SSW_q = self.compute_SST_SSW(q)
            SSB_q = SST_q - SSW_q
            res = res + np.sqrt((SSB_q / SST_q))
        return res * (1.00 / n) * (1.00 / np.sqrt(self.K))
    
            
                
    