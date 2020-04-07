#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.spatial import distance
import numpy as np

class CalinskiHarabasz:
    
    def __init__(self, data_frame, K, N, cluster_labels, cluster_centers=None, center=None, data_clusters=None):
        self.data_frame = data_frame
        self.K = K
        self.N = N
        self.cluster_centers = cluster_centers
        self.center = center
        self.data_clusters = data_clusters
        self.cluster_labels = cluster_labels
        
    
    def compute_Wl(self, l):
        xl = self.cluster_centers[l]
        n = (self.data_frame.shape[1])
        Wl = np.zeros((n , n), dtype=float)
        for xi in self.data_clusters[l]:
            P = (xi - xl).reshape(n, 1)
            Wl = Wl + (P.dot(P.reshape(1, n)))
        return Wl
    def compute_W(self):
        n = (self.data_frame.shape[1])
        W = np.zeros((n , n), dtype=float)
        for l in range(self.K):
            W = W + self.compute_Wl(l)
        return W
    
    def compute_B(self):
        n = (self.data_frame.shape[1])
        B = np.zeros((n , n), dtype=float)
        for l in range(self.K):
            P = (self.cluster_centers[l] - self.center).reshape(n, 1)
            B = B + len(self.data_clusters[l]) * P.dot(P.reshape(1, n))
        return B
    def VRC(self):
        
        Trace_B = np.trace(self.compute_B())
        Trace_W = np.trace(self.compute_W())
        
        return (Trace_B / Trace_W) * ((self.N - self.K) / (self.K - 1))    
            
    