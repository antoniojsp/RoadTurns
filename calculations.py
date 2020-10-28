import math
from math import cos, sin, asin, radians, sqrt


class Mathematica:

    # calculate a distance between to cardinal points. Input (2 set float of coordinates, output, distance in float in meters) HELPER FUNCTION
    def __distance(self, ini_lat, ini_lon, fin_lat, fin_lon):
        dif_lat = radians(ini_lat) - radians(fin_lat)
        dif_lon = radians(ini_lon) - radians(fin_lon)
        earth_radio = 6371 # radius in km
        partial_result = (sin(dif_lat/2))**2 + cos(radians(ini_lat)) * cos(radians(fin_lat)) * (sin(dif_lon/2))**2
        distance = earth_radio * asin(sqrt(partial_result)) * 2 * 1000# multiply by 1000 to convert to 	distance in meters
        return distance

    # Input: 2 int, Start index of the gpx points file where the coord lives, End, index where the coord ending lives. Output, distance of segment.
    def route_distance(self, gpx_list, start, end):
        segment = 0
        for i in range(start, end):
            segment += self.__distance(gpx_list[i].get_lat(), gpx_list[i].get_long(), gpx_list[i + 1].get_lat(), gpx_list[i + 1].get_long())
        return segment

    # calculate angle. Provide 3 lists, each one containing lats and long. b is the vertex. HELPER FUNCTION
    def __get_angle(self, a, b, c):
        angular = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
        result = angular + 360 if angular < 0 else angular
        return result

    # return a string signaling what direction is following.
    def turning(self, gpx_list, center, range):
        degrees = 0

        try:
            a = [gpx_list[center - range].get_lat(), gpx_list[center - range].get_long()]
            b = [gpx_list[center].get_lat(), gpx_list[center].get_long()]
            c = [gpx_list[center + range].get_lat(), gpx_list[center + range].get_long()]
            degrees = self.__get_angle(a, b, c)
        except:
            degrees = 0

        turn_direction = ""
        # print(degrees)
        if degrees > 210:
            turn_direction = "Right"
        elif degrees < 150:
            turn_direction = "Left"
        elif center == 0:
            turn_direction = "Start"
        else:
            turn_direction = "Straight"

        return turn_direction
