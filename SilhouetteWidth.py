#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.spatial import distance
import numpy as np
import sys

class SilhouetteWidth:
    def __init__(self, data_frame, K, N, cluster_labels, cluster_centers=None, center=None, data_clusters=None):
        self.data_frame = data_frame
        self.K = K
        self.N = N
        self.cluster_centers = cluster_centers
        self.data_clusters = data_clusters 
        self.center = center
        self.cluster_labels = cluster_labels
        
    def compute_a_p_j(self, Xj, Np, p):
        i = 0; s = 0
        while i < Np:
            Xi = self.data_clusters[p][i]
            s  = s + distance.euclidean(Xj, Xi)
            i += 1
        if Np == 1:
            return 0
        else:
            return (1.00 / (Np-1)) * s
        
    def compute_d_q_j(self, Xj, Nq, q):
        i = 0; s = 0
        while i < Nq:
            Xi = self.data_clusters[q][i]
            s = s + distance.euclidean(Xj, Xi)
            i += 1
        return (1.00 / Nq) * s
    
    def compute_b_p_j(self, Xj, p):
        MIN = sys.maxsize
        for q in range(self.K):
            if q != p:
                d_q_j = self.compute_d_q_j(Xj, len(self.data_clusters[q]), q)
                if d_q_j < MIN:
                    MIN = d_q_j
        return MIN
    
    def silhouette_x_j(self, Xj, Np, p):
        a_p_j = self.compute_a_p_j(Xj, Np, p)
        b_p_j = self.compute_b_p_j(Xj, p)
        tmp = max(a_p_j, b_p_j)
        
        return (b_p_j - a_p_j) / tmp
    def SWC(self):
        s = 0
        for p in range(self.K):
            Np = len(self.data_clusters[p])
            j = 0
            if Np != 1:
                while j < Np:
                    Xj = self.data_clusters[p][j]
                    s = s + self.silhouette_x_j(Xj, Np, p)
                    j += 1
        return s / self.N
    
                
                