import math

lat= 53.4055429
lng= -2.9976502
zoom= 16
x =400
y = 400


def getCoordinates(x, y):
    degreesPerPixelX = 360 / math.pow(2, zoom + 8)
    degreesPerPixelY = 360 / math.pow(2, zoom + 8) * math.cos(lat * math.pi / 180)


    lat1 = lat - degreesPerPixelY * ( y - y / 2)
    long= lng + degreesPerPixelX * ( x  - x / 2)
    return lat1,long


# log('SW', getCoordinates(0, y));
# log('NE', getCoordinates(x, 0));
# log('SE', getCoordinates(x, y));
# log('NW', getCoordinates(0, 0));
log = ('Something at 300,128', getCoordinates(350, 111118));
print(log)
def LatLon_from_XY(ProductSceneGeoCoding, x, y):
    #From x,y position in satellite image (SAR), get the Latitude and Longitude
    geopos = ProductSceneGeoCoding.getGeoPos(PixelPos(x, y), None)
    latitude = geopos.getLat()
    longitude = geopos.getLon()
    return latitude, longitude
latitude, longitude = LatLon_from_XY(sg, 12000, 2000)