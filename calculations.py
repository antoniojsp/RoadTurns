import math
from math import cos, sin, asin, radians, sqrt

class Mathematica:

    # calculate a distance between to cardinal points
    def __distance(self, ini_lat, ini_lon, fin_lat, fin_lon):
        dif_lat = radians(ini_lat) - radians(fin_lat)
        dif_lon = radians(ini_lon) - radians(fin_lon)
        earth_radio = 6371 # radius in km
        partial_result = (sin(dif_lat/2))**2 + cos(radians(ini_lat)) * cos(radians(fin_lat)) * (sin(dif_lon/2))**2
        distance = earth_radio * asin(sqrt(partial_result)) * 2 * 1000# multiply by 1000 to convert to 	distance in meters
        return distance

    # use __distance to add up different distances between points.
    def get_angle(self, a, b, c):
        angular = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
        result = angular + 360 if angular < 0 else angular
        return result

    # return the angle "b" formed by a and c
    def route_distance(self, list, start, end):
        segment = 0
        for i in range(start, end):
          segment += self.__distance(list[i].get_lat(), list[i].get_long(), list[i + 1].get_lat(), list[i + 1].get_long())
        return segment
