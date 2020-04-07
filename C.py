#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from scipy.spatial import distance
import numpy as np
import sys

class C:
    def __init__(self, data_frame, K, N, cluster_labels, cluster_centers=None, center=None, data_clusters=None):
        self.data_frame = data_frame
        self.K = K
        self.N = N
        self.cluster_centers = cluster_centers
        self.data_clusters = data_clusters 
        self.center = center
        self.cluster_labels = cluster_labels
        
    def compute_N_w(self):
        s = 0
        for i in range(self.K):
            tmp = (len(self.data_clusters[i])) ** 2
            s = s + tmp
        s = s - self.N
        return s // 2
    def Nt(self):
        return  (self.N * (self.N - 1)) // 2
    
    def compute_list_distance(self):
        distance_pairs = []; i = 0
        while i < self.N - 1:
            j = i+1
            while j < self.N:
                t = distance.euclidean(self.data_frame[i], self.data_frame[j])
                distance_pairs.append(t)
                j += 1
            i += 1
        pairs = np.asarray(distance_pairs, dtype=float)
        pairs.sort()
        return pairs
    
    def compute_S(self):
        s = 0
        for p in range(self.K):
            Np = len(self.data_clusters[p])
            i = 0
            while i < Np-1:
                j = i+1
                while j < Np:
                    dist = distance.euclidean(self.data_clusters[p][i], self.data_clusters[p][j])
                    s = s + dist
                    j += 1
                i += 1
        return s
    
    def compute_max_min(self):
        pairs = self.compute_list_distance()
        """
        print("pairs_distance = ", end = ' ')
        i = 0
        while i < 5 and i < self.Nt():
            print(pairs[i], end = ' ')
            i += 1
        """
        Nw = self.compute_N_w()
        pairs_min = pairs[:Nw]
        start = self.Nt() - Nw
        pairs_max = pairs[start:]
        return pairs_max.sum(), pairs_min.sum()
    def CI(self):
        S = self.compute_S()
        S_max, S_min = self.compute_max_min()
        return (S - S_min) / (S_max - S_min)
    
        