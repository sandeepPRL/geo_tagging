import numpy as np
# from EXIF_Data import *
# from sensor import *
import math
import os
# abs_path=path
class Matrix:
    def __init__(self, pa):
        self.__obj = pa


    def set_mat_maul(self, dist_mat,pos_m):
        self.mat_maul = self.multiplication(dist_mat,pos_m)

    def set_mat_maul2(self, neg_m):
        self.mat_maul2 = self.multiplication(neg_m,self.mat_maul)

    def set_mat_mul3(self, m):
        self.mat_mul3 = self.multiplication(m,self.mat_maul2)
        self.mat_mul3 =  np.array(self.mat_mul3)
        print('=============before normalization', self.mat_mul3)

        xmax, xmin = self.mat_mul3.max(), self.mat_mul3.min()
        self.mat_mul3 = (self.mat_mul3 - xmin)/(xmax - xmin)
        print("After normalization:")
        print(self.mat_mul3)

    def calculate_inverse_matrix(self):
        self.ainv = self.int_ex(self.mat_mul3)

    def intensive_matrix(self,x,w,h):
        i = 4
        a = np.zeros(shape=(i, i))

        a[0][0] = x
        a[0][1] = 0
        a[0][2] = w / 2
        a[0][3] = 0
        a[1][0] = 0
        a[1][1] = x
        a[1][2] = h / 2
        a[1][3] = 0
        a[2][0] = 0
        a[2][1] = 0
        a[2][2] = 1
        a[2][3] = 0
        a[3][0] = 0
        a[3][1] = 0
        a[3][2] = 0
        a[3][3] = 1
        # print(a)
        return a
    def distance_mat(self,y):
        i = 4
        distance_matrix = np.zeros(shape=(i, i))

        distance_matrix[0][0] = 1
        distance_matrix[0][1] = 0
        distance_matrix[0][2] = 0
        distance_matrix[0][3] = 0

        distance_matrix[1][0] = 0
        distance_matrix[1][1] = 1
        distance_matrix[1][2] = 0
        distance_matrix[1][3] = 0

        distance_matrix[2][0] = 0
        distance_matrix[2][1] = 0
        distance_matrix[2][2] = 1
        distance_matrix[2][3] = y

        distance_matrix[3][0] = 0
        distance_matrix[3][1] = 0
        distance_matrix[3][2] = 0
        distance_matrix[3][3] = 1
        # print('=======distance_matrix==========')
        # print(distance_matrix)
        return distance_matrix

    def pos_mat(self):
        i = 4
        positive_matrix = np.zeros(shape=(i, i))

        positive_matrix[0][0] = 1
        positive_matrix[0][1] = 0
        positive_matrix[0][2] = 0
        positive_matrix[0][3] = 0

        positive_matrix[1][0] = 0
        positive_matrix[1][1] = 0
        positive_matrix[1][2] = -1
        positive_matrix[1][3] = 0

        positive_matrix[2][0] = 0
        positive_matrix[2][1] = 1
        positive_matrix[2][2] = 0
        positive_matrix[2][3] = 0

        positive_matrix[3][0] = 0
        positive_matrix[3][1] = 0
        positive_matrix[3][2] = 0
        positive_matrix[3][3] = 1
        # print('positive_matrix')
        # print(positive_matrix)
        return positive_matrix
    def neg_mat(self,r_x_minus):
        i = 4
        negative_matrix = np.zeros(shape=(i, i))

        negative_matrix[0][0] = 1
        negative_matrix[0][1] = 0
        negative_matrix[0][2] = 0
        negative_matrix[0][3] = 0

        negative_matrix[1][0] = 0
        negative_matrix[1][1] = math.cos(r_x_minus)
        negative_matrix[1][2] = math.sin(r_x_minus)
        negative_matrix[1][3] = 0

        negative_matrix[2][0] = 0
        negative_matrix[2][1] = -(math.sin(r_x_minus))
        negative_matrix[2][2] = math.cos(r_x_minus)
        negative_matrix[2][3] = 0

        negative_matrix[3][0] = 0
        negative_matrix[3][1] = 0
        negative_matrix[3][2] = 0
        negative_matrix[3][3] = 1
        # print('negative_matrix')

        # print(negative_matrix)
        return negative_matrix
    def multiplication(self,val1,val2):
        result = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]

        for i in range(len(val1)):
            for j in range(len(val2[0])):
                for k in range(len(val2)):
                    result[i][j] += val1[i][k] * val2[k][j]
                    # final_matrix[i][j] += val1[i][k] * val2[k][j]
                    # ainv = np.linalg.inv(final_matrix)
        return result

    def int_ex(self,result):

        ainv = np.linalg.inv(result)
        return ainv
