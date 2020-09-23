import numpy as np


class FuzzyCMeansType2:
    def __init__(self, m, data_frame, N, n_clusters, eps=1e-4, max_count=1e+5):
        self.m = m  # tham so fuzzy
        self.max_count = max_count  # so vong lap toi da
        self.eps = eps  # epsilon, dieu kien dung
        self.data_frame = data_frame  # data sets
        self.N = N  # kich thuoc data sets
        self.K = n_clusters  # so nhan cum

    def dist(self, A, B):
        return np.linalg.norm(A - B, keepdims=False)

    def initializeMembershipMatrix(self):
        """

        Return Matrix K x N
        -------
        TYPE: numpy array
            khoi tao ngay nhien ma tran K x N co cac phan tu thuoc (0, 1)
            tong cac phan tu tren moi cot deu bang 1

        """
        matrix = np.random.rand(self.K, self.N)
        tmp = matrix.sum(axis=0)
        return matrix / tmp

    def updateCenters(self, membership_mat):
        """

        Parameters
        ----------
        membership_mat : numpy array
            ma tran bieu thi tu cach thanh vien cua cac phan tu trong moi cum khac nhau

        Returns
        -------
        center_clusters : numpy array
            mang cac center (K x n) tuong ung voi K cum theo thu tu.

        """

        new_membership_mat = membership_mat * 3/2 - 1 / 2
        center_clusters = np.zeros((self.K, self.data_frame.shape[1]))
        for i in range(self.K):
            center = np.zeros(self.data_frame.shape[1])
            s = 0
            for j in range(self.N):
                t = (new_membership_mat[i][j] ** self.m)
                s += t
                tmp1 = t * self.data_frame[j, :]
                center += tmp1
            center_clusters[i, :] = center / s
        return center_clusters

    def updateMembershipMatrix(self, center_clusters):
        """
        Parameters
        ----------
        center_clusters : numpy array
            mang cac center (K x n) tuong ung voi K cum theo thu tu.

        Returns
        -------
        matrix : numpy array
            ma tran bieu thi tu cach thanh vien cua cac phan tu trong moi cum khac nhau.

        """

        matrix = np.random.rand(self.K, self.N)
        p = 2 / (self.m - 1)
        matrix_distance = np.zeros((self.N, self.K))
        inverse_matrix_distance = np.zeros((self.N, self.K))
        for i in range(self.N):
            for j in range(self.K):
                matrix_distance[i, j] = self.dist(self.data_frame[i, :], center_clusters[j, :])

        inverse_matrix_distance = 1.00 / matrix_distance

        for j in range(self.K):
            # Cj = center_clusters[j, :]
            for i in range(self.N):
                # Xi = self.data_frame[i, :]
                # dist_Xi_Cj = self.dist(Xi, Cj)
                s = 0
                for k in range(self.K):
                    # Ck = center_clusters[k, :]
                    t = matrix_distance[i, j] * inverse_matrix_distance[i, k]
                    s += (t ** p)
                matrix[j, i] = float(1) / s
        return matrix

    def findLabels(self, membership_mat):
        """
        Parameters
        ----------
        membership_mat : numpy array
            mma tran bieu thi tu cach thanh vien cua cac phan tu trong moi cum khac nhau.

        Returns
        -------
        labels : numpy array
            mang gom N phan tu bieu thi labels cua phan tu tuong ung trong datasets.
        """
        matrix = (membership_mat == membership_mat.max(axis=0))
        labels = np.arange(self.N)
        for i in range(self.N):
            for j in range(self.K):
                if matrix[j][i] == True:
                    labels[i] = j
        return labels

    def normalizeData(self):
        a = np.max(self.data_frame, axis=0)
        b = np.min(self.data_frame, axis=0)
        for i in range(self.data_frame.shape[0]):
            for j in range(self.data_frame.shape[1]):
                self.data_frame[i][j] = (self.data_frame[i][j] - b[j]) / (a[j] - b[j])

    def FCM(self):
        self.normalizeData()
        matrix = self.initializeMembershipMatrix()
        tmp = matrix
        cluster_centers = np.zeros((self.K, self.data_frame.shape[1]))
        count = 0
        while True:
            cluster_centers = self.updateCenters(matrix)
            matrix = self.updateMembershipMatrix(cluster_centers)
            terminate = (np.linalg.norm(matrix - tmp))
            tmp = matrix
            if ((terminate < self.eps) or (count >= self.max_count)):
                break
            print("terminate = ", terminate)
            count += 1

        labels = self.findLabels(matrix)

        return cluster_centers, labels
