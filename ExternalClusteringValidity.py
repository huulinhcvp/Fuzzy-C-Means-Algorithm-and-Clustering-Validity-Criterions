#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class RandIndex:
    def __init__(self, N, data_frame, original_labels, cluster_labels):
        self.N = N
        self.data_frame = data_frame
        self.original_labels = original_labels
        self.cluster_labels = cluster_labels
        
    def isSimilar(self, label1, label2):
        return label1==label2
        
    def RI(self):
        i = 0; a = 0; b = 0; c = 0; d = 0
        while i < self.N-1:
            j = i + 1
            while j < self.N:
                if self.isSimilar(self.original_labels[i], self.original_labels[j]):
                    if self.cluster_labels[i]==self.cluster_labels[j]:
                        a += 1
                    else:
                        b += 1
                else:
                    if self.cluster_labels[i]==self.cluster_labels[j]:
                        c += 1
                    else:
                        d += 1
                j += 1
            i += 1
        RI_idx = 0
        try:
            RI_idx = (a + d) / (a + b + c + d)
        except:
            RI_idx = 0
        return RI_idx
    
class AdjustedRandIndex(RandIndex):
    def ARI(self):
        i = 0; a = 0; b = 0; c = 0; d = 0
        while i < self.N-1:
            j = i + 1
            while j < self.N:
                if self.isSimilar(self.original_labels[i], self.original_labels[j]):
                    if self.cluster_labels[i]==self.cluster_labels[j]:
                        a += 1
                    else:
                        b += 1
                else:
                    if self.cluster_labels[i]==self.cluster_labels[j]:
                        c += 1
                    else:
                        d += 1
                j += 1
            i += 1
        ARI_idx= 0
        exp1 = ((a+c) * (a+b)) / (float(a+b+c+d))
        exp2 = ((a+c) + (a+b)) / 2.0
        try:
            ARI_idx = (a - exp1) / (exp2 - exp1)
        except:
            ARI_idx = 0
        return ARI_idx
        
class JaccardCoefficient(RandIndex):
    def JC(self):
        i = 0; a = 0; b = 0; c = 0
        while i < self.N-1:
            j = i + 1
            while j < self.N:
                if self.isSimilar(self.original_labels[i], self.original_labels[j]):
                    if self.cluster_labels[i]==self.cluster_labels[j]:
                        a += 1
                    else:
                        b += 1
                else:
                    if self.cluster_labels[i]==self.cluster_labels[j]:
                        c += 1
                j += 1
            i += 1
        JC_idx = 0
        try:
            JC_idx = float(a) / (a+b+c)
        except:
            JC_idx = 0
        return JC_idx
        