#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from scipy.spatial import distance
import numpy as np
import sys

class PBM:
    def __init__(self, data_frame, K, N, cluster_labels, cluster_centers=None, center=None, data_clusters=None):
        self.data_frame = data_frame
        self.K = K
        self.N = N
        self.cluster_centers = cluster_centers
        self.data_clusters = data_clusters 
        self.center = center
        self.cluster_labels = cluster_labels
        
    def compute_E_1(self):
        s = 0
        for i in range(self.N):
            s = s + distance.euclidean(self.data_frame[i], self.center)
        return s
    
    def compute_E_k(self):
        s = 0
        for l in range(self.K):
            Xl = self.cluster_centers[l]
            Nl = len(self.data_clusters[l])
            i = 0
            while i < Nl:
                Xi = self.data_clusters[l][i]
                s = s + distance.euclidean(Xi, Xl)
                i += 1
        return s
    
    def compute_D_k(self):
        MAX = -sys.maxsize
        l = 0
        while l < self.K-1:
            m = l+1
            while m < self.K:
                dist = distance.euclidean(self.cluster_centers[l], self.cluster_centers[m])
                if dist > MAX:
                    MAX = dist
                m += 1
            l += 1
        return MAX
    def PBM(self):
        E1 = self.compute_E_1()
        Ek = self.compute_E_k()
        Dk = self.compute_D_k()
        
        res = (1.00 / self.K) * (E1 / Ek) * Dk
        return res ** 2
    
            