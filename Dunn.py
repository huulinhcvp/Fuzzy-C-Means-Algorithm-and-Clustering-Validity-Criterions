#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from scipy.spatial import distance
import numpy as np
import sys

class Dunn:
    """
        Dunn index:
            mot bien the cua chi so Dunn goc
            Do phuc tap: O(nN + nk^2)
        Cac tham so:
            data_frame: du lieu goc gom cac data points
            K: so cum
            N: so data points
            cluster_labels: mot ndarray luu tru cac nhan cua cac data points (theo thu tu)
            cluster_centers: mot ndarray 2 chieu luu tru cac centers cua K cum, theo thu tu
            data_clusters: la mot mang cua K cum; moi cum luu tru cac data points cua cum do
                data_clusters[i] luu tru cac data points cua cum i
                --> kich thuoc: N phan tu
    """
    
    def __init__(self, data_frame, K, N, cluster_labels, cluster_centers=None, center=None, data_clusters=None):
        self.data_frame = data_frame
        self.K = K
        self.N = N
        self.cluster_centers = cluster_centers
        self.data_clusters = data_clusters 
        self.center = center
        self.cluster_labels = cluster_labels
    
    
    def set_distance(self, p, q):
        return distance.euclidean(self.cluster_centers[p], self.cluster_centers[q])
    
    def diameter(self, l):
        Nl = len(self.data_clusters[l])
        p = 2.00 / Nl; s = 0
        for i in range(Nl):
            s = s + distance.euclidean(self.data_clusters[l][i], self.cluster_centers[l])
        return s * p
            
    def maxDiameter(self):
        MAX = -sys.maxsize
        for i in range(self.K):
            d = self.diameter(i)
            if d > MAX:
                MAX = d
        return MAX
    def DN(self):
        MIN = sys.maxsize
        max_diameter = self.maxDiameter()
        p = 0
        while p < self.K-1:
            q = p+1
            while q < self.K:
                tmp = self.set_distance(p, q) / max_diameter
                if tmp < MIN:
                    MIN = tmp
                q += 1
            p += 1
        return MIN
                
        
        