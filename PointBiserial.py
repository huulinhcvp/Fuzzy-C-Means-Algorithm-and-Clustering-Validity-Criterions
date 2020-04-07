#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from scipy.spatial import distance
import numpy as np
import sys


class PointBiserial:
    def __init__(self, data_frame, K, N, cluster_labels, cluster_centers=None, center=None, data_clusters=None):
        self.data_frame = data_frame
        self.K = K
        self.N = N
        self.cluster_centers = cluster_centers
        self.data_clusters = data_clusters 
        self.center = center
        self.cluster_labels = cluster_labels
        
    def w_d(self):
        s = 0
        for l in range(self.K):
            Nl = len(self.data_clusters[l])
            s = s + Nl * (Nl - 1)
        return s // 2
    def N_t(self):
        return (self.N) * (self.N - 1) // 2
    def b_d(self):
        return self.N_t() - self.w_d()
    def compute_distances(self):
        i = 0
        distance_pairs = []
        d_w = 0; d_b = 0
        
        while i < self.N-1:
            j = i+1
            while j < self.N:
                tmp = distance.euclidean(self.data_frame[i], self.data_frame[j])
                if self.cluster_labels[i] == self.cluster_labels[j]:
                    d_w = d_w + tmp
                else:
                    d_b = d_b + tmp
                distance_pairs.append(tmp)
                j += 1
            i += 1
        pairs = np.asarray(distance_pairs)
        s_d = np.std(pairs)
        d_w = d_w / self.w_d()
        d_b = d_b / self.b_d()
        return s_d, d_w, d_b
    
    def PB(self):
        t = self.N_t()
        w_d = self.w_d()
        b_d = self.b_d()
        s_d, d_w, d_b = self.compute_distances()
        return (d_b - d_w) * (np.sqrt(w_d * (b_d / (t**2)))) / s_d
    
    