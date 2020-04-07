#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.spatial import distance
import numpy as np


class DaviesBouldin:
    def __init__(self, data_frame, K, N, cluster_labels, cluster_centers=None, center=None, data_clusters=None):
        self.data_frame = data_frame
        self.K = K
        self.N = N
        self.cluster_centers = cluster_centers
        self.cluster_labels = cluster_labels
        self.data_clusters = data_clusters
        self.center = center
                
        
    def compute_d(self, l, data_cluster):
        #so cum
        Nl = len(data_cluster)
        #centroid
        my_centers = self.cluster_centers[l]
        
        
        s = 0
        for xi in data_cluster:
            s += distance.euclidean(xi, my_centers)
        #print(s)
        #print(float(s / Nl))
            
        return float(s / Nl)
    
    def compute_Dlm(self, l, m, data_cluster_l, data_cluster_m):
        Dlm = 0.0
        try:
            d = distance.euclidean(self.cluster_centers[l], self.cluster_centers[m])
            #print("d = ", d)
            Dlm = float(1 / d) * (self.compute_d(l, data_cluster_l) + self.compute_d(m, data_cluster_m))
            #print(self.compute_d(l, data_cluster_l))
            #print(Dlm)
        except:
            Dlm = 0.0
        #print(Dlm)
        return Dlm
    
    
    def compute_Dl(self, l):
        list_D = []
        for m in range(self.K):
            if m != l:
                temp = self.compute_Dlm(l, m, np.asarray(self.data_clusters[l]),np.asarray(self.data_clusters[m]))
                list_D.append(temp)
        res = np.asarray(list_D)
        return res.max()
    
    #DaviesBouldin index
    def compute_DB(self):
        
        sigma_D = 0.0
        #print(data_clusters)
        
        for i in range(self.K):
            sigma_D += self.compute_Dl(i)
            
        return float(sigma_D) / float(self.K)
    
    