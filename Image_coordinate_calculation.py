import math
import numpy as np

class Newcoordinate:
    def __init__(self, mat):
        self.__obj = mat

    def pixel_to_world(self,w, h, mat_mul3):
        matrix = np.zeros(shape=(4, 1))
        matrix[0][0] = w
        matrix[1][0] = h
        matrix[2][0] = 1
        matrix[3][0] = 1
        print('pixel_to_world', matrix)

        in_matrix = [[0],
                     [0],
                     [0],
                     [0]]
        for i in range(len(mat_mul3)):
            for j in range(len(matrix[0])):
                for k in range(len(matrix)):
                    in_matrix[i][j] += mat_mul3[i][k] * matrix[k][j]
        return in_matrix
    #
    def eq_distance(self,e1, e2):
        dist = 0
        for i in range(0, 4):
            dist += ((e1[i][0] - e2[i][0]) ** 2)
        dist = math.sqrt(dist)
        return dist
    #
    #
    def div(self,dist):
        dist = dist / 72
        dist = dist / 39370
        return dist

    def angle1(self,d1):
        j = 0
        list_of_value = []
        for i in range(0, 3):
            a = d1[i][j]
            list_of_value.append(a)
        return list_of_value

    def angle_calculation(self,cord1, cord2):
        coordinate_value = self.angle1(cord1)
        coordinate_value1 = self.angle1(cord2)
        # print("value of coordinate_value=======",coordinate_value)
        # print("value of coordinate_value1=======",coordinate_value1)
        a1 = coordinate_value[0]
        a2 = coordinate_value[1]
        a3 = coordinate_value[2]
        b1 = coordinate_value1[0]
        b2 = coordinate_value1[1]
        b3 = coordinate_value1[2]
        value = (a1 * b1 + a2 * b2 + a3 * b3)
        value1 = math.sqrt(a1 ** 2 + a2 ** 2 + a3 ** 2) * math.sqrt(b1 ** 2 + b2 ** 2 + b3 ** 2)
        a = value / value1
        theta_value = math.acos(a)
        return theta_value

    def coordinate_angle(self,ang, dis, lat1, lon1, R):
        lat2 = math.asin(math.sin(lat1) * math.cos(dis / R) +
                         math.cos(lat1) * math.sin(dis / R) * math.cos(ang))

        lon2 = lon1 + math.atan2(math.sin(ang) * math.sin(dis / R) * math.cos(lat1),
                                 math.cos(dis / R) - math.sin(lat1) * math.sin(lat2))
        lat2 = math.degrees(lat2)
        lon2 = math.degrees(lon2)
        return lat2, lon2
