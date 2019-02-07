# from EXIF_Data import *
# from matrix import *
import os
import math

# path=abs_path
class Sensor:
    val = 43.27
    def __init__(self,obj):
        self.__obj = obj
    def crop_factor(self):
        # print(self.ret.get('FocalLength'))
        focal_len = self.__obj.ret.get('FocalLength')
        self.focal_length = focal_len[0] / focal_len[1]
        print('focal length===>', self.focal_length)
        crop_fac = self.__obj.ret.get('FocalLengthIn35mmFilm') / self.focal_length
        print('crop_fac==>', crop_fac)

        return crop_fac
    def diagola_full_frame(self, crop_fac):
        # print(type(pa.val),type(crop_fac),crop_fac)
        dia = self.val / crop_fac
        # print('diagonal xxx====', dia)

        return dia

    def pytho(self,w,h):
        # width, hei = r.getGPS(self.path)
        w_h = w / h
        print("w_h value", w_h)
        return w_h

    def py(self, dia, w_h,width,hei):
        # width, hei = r.getGPS(self.path)
        print("inside py", dia, w_h)
        h = (dia) / math.sqrt((w_h) ** 2 + 1)
        print(' print h value',h)
        w = w_h * h
        print('sensor width value is==', w)
        print("focal length==",self.focal_length)
        f_cap = self.focal_length * width
        f_cap = f_cap / w
        print('f_cap value is==', f_cap)
        f = (w / (2 * self.focal_length))
        # print("fffffffffffff",f)
        fov = 2 * (math.atan(f))
        # fov = (math.atan(f))
        print('feild of view is ===>', fov)

        distance = math.hypot(width, hei)
        print('pythagorus algo value===', distance)
        distance = (self.focal_length * distance) / self.val
        print('distance is ===>', distance)

        r_x_minus = fov
        print('r_x_minus is =====',r_x_minus)

        return f_cap, distance, r_x_minus

    def overall(self,path):
        wi,he=self.__obj.getGPS(path)
        print(wi,he)
        foc_len=self.__obj.focal_lenth(path)
        print(foc_len)
        log,lat = self.__obj.log_lat_value(path)
        print('log lat',log,lat)
        crop_f= self.crop_factor()
        print(crop_f)
        dia1= self.diagola_full_frame(crop_f)
        pytho = self.pytho(wi,he)
        f_c,dist,r_x = self.py(dia1,pytho,wi,he)
        print(f_c,dist,r_x)

        return f_c,dist,r_x, wi,he,log,lat

