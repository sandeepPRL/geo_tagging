import exifread
from PIL import Image
import os
import math
from PIL.ExifTags import TAGS
class Intencive:
    def __init__(self,path):
        self.path=path
        self.ret = {}
        self.focal_lenth(path)
        self.val=43.27
    def getGPS(self,filepath):
        # print("file patttt",filepath)

        im = Image.open(filepath)
        self.width, self.height = im.size
        print('width==>',self.width)
        print('height==>',self.height)

        return self.width,self.height

    def focal_lenth(self,fn):
        i = Image.open(fn)
        info = i._getexif()

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            self.ret[decoded] = value
        # print('rect====', self.ret.keys())
        return self.ret

    def _convert_to_degress(self,value):
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
        return d + (m / 60.0) + (s / 3600.0)

    def log_lat_value(self,filepath):

        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f)
            latitude = tags.get('GPS GPSLatitude')
            latitude_ref = tags.get('GPS GPSLatitudeRef')
            longitude = tags.get('GPS GPSLongitude')
            longitude_ref = tags.get('GPS GPSLongitudeRef')

            if latitude:
                lat_value = self._convert_to_degress(latitude)
                # print(lat_value)
                if latitude_ref.values != 'N':
                    lat_value = -lat_value
            else:
                return {}
            if longitude:
                lon_value = self._convert_to_degress(longitude)
                if longitude_ref.values != 'E':
                    lon_value = -lon_value
            else:
                return {}
            lo_lat = {'latitude': lat_value, 'longitude': lon_value}
            latitude1 = lo_lat['latitude']
            latitude = math.radians(latitude1)
            longitude1 = lo_lat['longitude']
            longitude = math.radians(longitude1)
            return longitude, latitude
