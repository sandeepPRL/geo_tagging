import exifread
from PIL import Image
import os
import math
from PIL.ExifTags import TAGS
from numpy.linalg import inv
from decimal import Decimal
import numpy as np
focal_length=[]
FocalLengthIn35m=[]
Radius = 6378.1
print('Radius of the Earth ',Radius)
l = []
class Intencive:
    def __init__(self,path):
        self.path=path
        self.ret = {}
        self.get_exif(path)
        self.val=43.27
    def getGPS(self,filepath):

        im = Image.open(filepath)
        self.width, self.height = im.size
        print('width==>',self.width)
        print('height==>',self.height)

        return self.width,self.height
    def get_exif(self,fn):
        i = Image.open(fn)
        info = i._getexif()

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            self.ret[decoded] = value
        print('rect====', self.ret.keys())
        return self.ret

    def crop_factor(self):
        print(self.ret.get('FocalLength'))
        tu = self.ret.get('FocalLength')
        self.fr = tu[0]/tu[1]
        print('focal length===>',self.fr)
        crop_fac= self.ret.get('FocalLengthIn35mmFilm') /self.fr
        print('crop_fac==>',crop_fac)
        diag=self.diagola_full_frame(crop_fac)
        print("diagonal value",diag)
        # f_cap=self.py(fr)
        # print('f_cap',f_cap)
        return crop_fac,diag


    def diagola_full_frame(self,crop_fac):
        dia=self.val/crop_fac
        print('diagonal====',dia)


        return dia
    def pytho(self):
        width,hei=self.getGPS(self.path)
        w_h=width/hei
        print("w_h value",w_h)
        return w_h
    def py(self,dia,w_h):
        # crop=self.crop_factor()
        width, hei = self.getGPS(self.path)
        print("inside py",dia,w_h)
        h=(dia)/math.sqrt((w_h)**2+1)
        print(h)
        w=w_h*h
        print('www',w)
        f_cap = self.fr*width
        f_cap= f_cap/w
        print('f_cap', f_cap)
        f = (w/(2*self.fr))
        # fov=  2 *(math.degrees(math.atan(f)))
        # print('tan inverse in degree ',fov)
        fov = 2 * (math.atan(f))
        print('feild of view is ===>',fov)

        distance= math.hypot(self.width, self.height)
        print('dis after pythago===',distance)
        distance = round((17 * distance)/self.val,5)
        print('distance is ===>',distance)

        r_x_minus = fov

        return f_cap,distance,r_x_minus

file_path = '0002_C.jpg'
# gps = getGPS(file_path)
curr = os.path.dirname(__file__)
abs_path = os.path.join(curr, file_path)
obj = Intencive(abs_path)
w, h = obj.getGPS(abs_path)
# crop= obj.crop_factor(fo,foi)
c,dia = obj.crop_factor()
print("c, dia values",c,dia)
w_h = obj.pytho()
print("w_h val at end",w_h)
x, y, r_x_minus = obj.py(dia,w_h)
print("x, y, r_x_minus======", x, y, r_x_minus)
print('=============================================')

def _convert_to_degress(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)

def log_lat_value(filepath):
    with open(filepath, 'rb') as f:
        tags = exifread.process_file(f)
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')

        if latitude:
            lat_value = _convert_to_degress(latitude)
            # print(lat_value)
            if latitude_ref.values != 'N':
                lat_value = -lat_value
        else:
            return {}
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values != 'E':
                lon_value = -lon_value
        else:
            return {}
        return {'latitude': lat_value, 'longitude': lon_value}
    # return {}

log_lat = log_lat_value(file_path)

print('logitude and latitude value is ====>',log_lat)
latitude1 = log_lat['latitude']
latitude = math.radians(latitude1)
print('latitude',latitude)
longitude1 = log_lat['longitude']
longitude = math.radians(longitude1)
print('longitude',longitude)
# for key in log_lat.keys():
#     log= log_lat[key]
#     print('{}' .format(key),log)

print('=============================================')
i=4
a=np.zeros(shape=(i,i))

a[0][0] = x
a[0][1] = 0
a[0][2] = w/2
a[0][3] =0
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
print('intensiv matrix')
print(a)
print('====================================')

i=4
distance_matrix=np.zeros(shape=(i,i))

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
print('distance_matrix')
print(distance_matrix)

print('====================================')

i=4
positive_matrix=np.zeros(shape=(i,i))

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
print('positive_matrix')
# print('math cos cheking ==========',math.cos(-0.028))
print(positive_matrix)
print('=============================================')

i=4
negative_matrix=np.zeros(shape=(i,i))

negative_matrix[0][0] = 1
negative_matrix[0][1] = 0
negative_matrix[0][2] = 0
negative_matrix[0][3] = 0

negative_matrix[1][0] = 0
negative_matrix[1][1] = math.cos(r_x_minus)
negative_matrix[1][2] = math.sin( r_x_minus)
negative_matrix[1][3] = 0

negative_matrix[2][0] = 0
negative_matrix[2][1] = -(math.sin( r_x_minus))
negative_matrix[2][2] = math.cos(r_x_minus)
negative_matrix[2][3] = 0

negative_matrix[3][0] = 0
negative_matrix[3][1] = 0
negative_matrix[3][2] = 0
negative_matrix[3][3] = 1
print('negative_matrix')

print(negative_matrix)
# negative_matrix1=inv(negative_matrix)
# print('negative_matrix1',negative_matrix1)
print('=============================================')

print('distance matrix * Rx(90) degree positive matrix')

result = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0 ,0] ]
for i in range(len(distance_matrix)):
    for j in range(len(positive_matrix[0])):
        for k in range(len(positive_matrix)):
            result[i][j] += distance_matrix[i][k] * positive_matrix[k][j]
for r in result:
    print(r)
print(' ====================================================================')
print('final result negative_matrixr_x(- alpha) * (distance matrix * Rx(90) degree positive matrix) ')
final_result = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0 ,0] ]
for i in range(len(negative_matrix)):
    for j in range(len(result[0])):
        for k in range(len(result)):
            final_result[i][j] += negative_matrix[i][k] * result[k][j]
for r in final_result:
    print(r)


print(' ====================================================================')
print('I * E matrix result')
final_matrix = [[0, 0, 0, 0],
	            [0, 0, 0, 0],
	            [0, 0, 0, 0],
                [0, 0, 0, 0]]
for i in range(len(a)):
    for j in range(len(final_result[0])):
        for k in range(len(final_result)):
            final_matrix[i][j] += a[i][k] * final_result[k][j]
for r in final_matrix:
    
    print(r)
final_matrix = np.array(final_matrix)
print(final_matrix)
xmax, xmin = final_matrix.max(), final_matrix.min()
final_result = (final_matrix - xmin)/(xmax - xmin)
print('=================final marix after normalization===========================',final_result)
# # print('inverse of a matrix')
# # ainv = np.linalg.inv(final_matrix)
# # print(ainv)

def pixel_to_world(w,h,ainv):
    matrix = np.zeros(shape=(4, 1))
    matrix[0][0] = w
    matrix[1][0] = h
    matrix[2][0] = 1
    matrix[3][0] = 1
    print('pixel_to_world',matrix)

    in_matrix = [[0],
                 [0],
                 [0],
                 [0]]
    for i in range(len(ainv)):
        for j in range(len(matrix[0])):
            for k in range(len(matrix)):
                in_matrix[i][j] += ainv[i][k] * matrix[k][j]
    print('in matrix ',in_matrix)
    return in_matrix
def eq_distance(e1,e2):
    dist=0
    for i in range(0,4):
        dist += ((e1[i][0]-e2[i][0])**2)
    dist= math.sqrt(dist)
    return dist

m1=pixel_to_world(0,0,final_result)
m2=pixel_to_world( obj.width,0,final_result)
m3=pixel_to_world(obj.width,obj.height,final_result)
m4=pixel_to_world(0,obj.height,final_result)
m5 =pixel_to_world(obj.width/2,obj.height/2,final_result)

print('m1==',m1)
print('m2==',m2)
print('m3==',m3)
print('m4==',m4) 
print('m5==',m5)

d1 = eq_distance(m1,m2)
print(d1)
d2 = eq_distance(m2,m3)
print(d2)
d3 = eq_distance(m3,m4)
print(d3)
d4 = eq_distance(m4,m1)
print(d4)
d5 = eq_distance(m1,m3)
print(d5)
d6 = eq_distance(m2,m4)
print(d6)
d7 = eq_distance(m2,m5)
print(d7)
d8 = eq_distance(m1,m5)
print(d8)
d9 = eq_distance(m3,m5)
print(d9)
d10 = eq_distance(m4,m5)
print(d10)
# dist = d10 / 72
# dist = dist / 39370

def div(dist):
    dist=dist/72
    dist=dist/39370
    return dist
dis_km_12 = div(d1)
# print('distance of m1,m2 in km ', dis_km_12 )
# dis_km_23 = div(d2)
# print('distance of m2,m3 in km', dis_km_23 )
# dis_km_34 = div(d3)
# print('distance of m3,m4 in km',dis_km_34 )
# dis_km_41 = div(d4)
# print('distance of m3,m4 in km',dis_km_41 )
# dis_km_13 = div(d5)
# print('distance of m1,m3 in km',dis_km_13 )
# dis_km_24 = div(d6)
# print('distance of m2,m4 in km',dis_km_24 )
dis_km_25 = div(d7)
print('distance of m2,m5 in km',dis_km_25 )
dis_km_15 = div(d8)
print('distance of m1,m5 in km',dis_km_15 )
dis_km_35 = div(d9)
print('distance of m3,m5 in km',dis_km_35 )
dis_km_45 = div(d10)
print('distance of m4,m5 in km',dis_km_45 )

def angle1(d1):
    j = 0
    list_of_value=[]
    for i in range(0,3):
        a=d1[i][j]
        list_of_value.append(a)
    return list_of_value

def angle_calculation(cord1,cord2):
    coordinate_value = angle1(cord1)
    coordinate_value1 = angle1(cord2)
    # print("value of coordinate_value=======",coordinate_value)
    # print("value of coordinate_value1=======",coordinate_value1)
    a1 = coordinate_value[0]
    a2 = coordinate_value[1]
    a3 = coordinate_value[2]
    b1 = coordinate_value1[0]
    b2 = coordinate_value1[1]
    b3 = coordinate_value1[2]
    value = (a1*b1 + a2*b2 + a3*b3)
    value1 = math.sqrt(a1 ** 2 + a2 ** 2 + a3 ** 2) * math.sqrt(b1 ** 2 + b2 ** 2 + b3 ** 2)
    a = value/value1
    theta_value = math.acos(a)
    return theta_value
print('=============================================')

value_of_angle1 = angle_calculation(m5,m1)
print('angle value for m5,m1  ===>',value_of_angle1)
value_of_angle2 = angle_calculation(m5,m2)
print('angle value for m5,m2  ===>',value_of_angle2)
value_of_angle3 = angle_calculation(m5,m3)
print('angle value for m5,m3  ===>',value_of_angle3)
value_of_angle4 = angle_calculation(m5,m4)
print('angle value for m5,m4  ===>',value_of_angle4)

def coordinate_angle(ang,dis,lat1,lon1,R):
    lat2 = math.asin(math.sin(lat1) * math.cos(dis / R) +
                     math.cos(lat1) * math.sin(dis / R) * math.cos(ang))

    lon2 = lon1 + math.atan2(math.sin(ang) * math.sin(dis / R) * math.cos(lat1),
                             math.cos(dis / R) - math.sin(lat1) * math.sin(lat2))
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return lat2, lon2
new_cod_val = coordinate_angle(value_of_angle1, dis_km_15, latitude, longitude, Radius)
print(new_cod_val)

new_cod_val = coordinate_angle(value_of_angle2, dis_km_25, latitude, longitude, Radius)
print(new_cod_val)
#
new_cod_val = coordinate_angle(value_of_angle3, dis_km_35, latitude, longitude, Radius)
print(new_cod_val)

new_cod_val = coordinate_angle(value_of_angle4, dis_km_45, latitude, longitude, Radius)
print(new_cod_val)

lat= 53.4055429
lng= -2.9976502
zoom= 16
x =400000
y = 104
Radius = 6378.1

def getCoordinates(x, y):
    degreesPerPixelX = 360 / math.pow(2, zoom + 8)
    degreesPerPixelY = 360 / math.pow(2, zoom + 8) * math.cos(lat * math.pi / 180)


    lat1 = lat - degreesPerPixelY * ( y - y / 2)
    long= lng + degreesPerPixelX * ( x  - x / 2)
    return lat1,long
log = ('Something at 300,128', getCoordinates(x, y))
print(log)




x= 200
y= 100
wc = pixel_to_world(x/2,y/2, final_result)
print('world coordinate', wc)
di = eq_distance(m5,wc)
print(di)
dv = div(di)
print('division', dv)
angle = angle_calculation(m5,wc)
print('angle',angle)
cordinat = coordinate_angle(angle, di, latitude, longitude, Radius)
print('cordinate',cordinat)
