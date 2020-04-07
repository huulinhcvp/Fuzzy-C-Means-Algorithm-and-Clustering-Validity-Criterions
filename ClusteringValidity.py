#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 06:38:36 2020

@author: huu_linh
"""
from scipy.spatial import distance
import numpy as np
from DaviesBouldin import DaviesBouldin
from CalinskiHarabasz import CalinskiHarabasz
from Dunn import Dunn
from SilhouetteWidth import SilhouetteWidth
from SimplifiedSilhouette import SimplifiedSilhouette
from PBM import PBM
from C import C
from PointBiserial import PointBiserial
from C_per_sqrt_K import C_per_sqrt_K

class ClusteringValidity:
    def __init__(self, data_frame, K, N, cluster_labels, cluster_centers=None, center=None, data_clusters=None):
        """
        Cac tham so
        ----------
        data_frame : ndarray
            N diem du lieu duoc luu tru trong data_frame
            e.g:
                data_frame = array([[4.0, 5.1, 2.3], [1.5, 4.2, 1.4]]) --> 2 diem du lieu, moi diem la du lieu 3 chieu
        K : int
            K cum.
        N : int
            N diem du lieu.
        cluster_labels : ndarray
            mang mot chieu duoc luu tru duoi dang ndarray, chua cac nhan tuong ung voi tung diem du lieu
            e.g:
                [1, 1, 0, 0, 2, 2, 3, 3, 3]
                data_frame[i] nam trong cum co nhan cluster_labels[i]
        Returns
        -------
        None.

        """
        self.data_frame = data_frame
        self.K = K
        self.N = N
        self.cluster_labels = cluster_labels
        self.data_clusters = self.data_Clt()
        self.cluster_centers = self.compute_centers()
        self.center = self.centroid()
        
    def centroid(self):
        """
        Returns
        -------
        numpy array
            mang gom n gia tri ung voi n thuoc tinh cua data points, mang nay bieu thi center cua toan bo data sets.

        """
        return self.data_frame.mean(axis=0)
    def data_Clt(self):
        """
        

        Returns
        -------
        data_clusters : list
            Bieu thi danh sach K cum du lieu, moi cum nay la mot mang numpy luu tru cac data points trong cum do.

        """
        
        dt = [[] for _ in range(self.K)]
        for i in range(self.N):
            data_point = self.data_frame[i]
            dt[self.cluster_labels[i]].append((data_point))
            
        data_clusters = []
        j = 0
        while j < self.K:
            if len(dt[j]) != 0:
                data_clusters.append(dt[j])
            j += 1
        self.K = len(data_clusters)
        
        return data_clusters
    
    def compute_centers(self):
        """
        

        Returns
        -------
        cluster_centers : numpy array
            mang cac center tuong ung voi moi cum (mang K x n)

        """
        cluster_centers = np.zeros((self.K, self.data_frame.shape[1]), dtype=float)
        #print("data_clusters = ", data_clusters)
        for i in range(self.K):
            cluster_centers[i, :] = np.asarray(self.data_clusters[i]).mean(axis = 0)
        return cluster_centers
    
    def DB_idx(self):
        """
            Davies-Bouldin index
        """
        index = DaviesBouldin(self.data_frame, self.K, self.N, self.cluster_labels, self.cluster_centers, self.center, self.data_clusters)
        return index.compute_DB()
    
    def VRC_idx(self):
        """

        Returns
        -------
        TYPE: float
            Calinski-Harabasz index.

        """
        index = CalinskiHarabasz(self.data_frame, self.K, self.N, self.cluster_labels, self.cluster_centers, self.center, self.data_clusters)
        return index.VRC()
    
    def DN_idx(self):
        """
        Returns
        -------
        TYPE: float
            Dunn index.

        """
        index = Dunn(self.data_frame, self.K, self.N, self.cluster_labels, self.cluster_centers, self.center, self.data_clusters)
        return index.DN()
    def SWC_idx(self):
        """
            Silhouette Width Criterion
        """
        index = SilhouetteWidth(self.data_frame, self.K, self.N, self.cluster_labels, self.cluster_centers, self.center, self.data_clusters)
        return index.SWC()
    
    def SSWC_idx(self):
        """
            Simplified Silhouette
        """
        index = SimplifiedSilhouette(self.data_frame, self.K, self.N, self.cluster_labels, self.cluster_centers, self.center, self.data_clusters)
        return index.SSWC()
    
    def PBM_idx(self):
        """
            PBM index
        """
        index = PBM(self.data_frame, self.K, self.N, self.cluster_labels, self.cluster_centers, self.center, self.data_clusters)
        return index.PBM()

    def CI_idx(self):
        """
            C index
        """
        index = C(self.data_frame, self.K, self.N, self.cluster_labels, self.cluster_centers, self.center, self.data_clusters)
        return index.CI()
    def PB_idx(self):
        """
            PointBiserial index
        """
        index = PointBiserial(self.data_frame, self.K, self.N, self.cluster_labels, self.cluster_centers, self.center, self.data_clusters)
        return index.PB()
    def CK_idx(self):
        """

        Returns
        -------
        TYPE: float
            C / sqrt(K) index.

        """
        index = C_per_sqrt_K(self.data_frame, self.K, self.N, self.cluster_labels, self.cluster_centers, self.center, self.data_clusters)
        return index.CK()
        