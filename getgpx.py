#data structure that hols
import gpxpy

# I prefer to use a class instead of a dict since allows to extends easily in future if required. Names are more clear to indicate its parts.


class Points : #  class that holds info of one point. The idea is create an array of this object.
    def __init__(self,lat, long, elev, time):
        self.__index = 0
        self.__lat = lat
        self.__long = long
        self.__elev = elev
        self.__time = time
        self.__index += 1

    def get_index(self):
        return self.__index

    def get_lat(self):
        return self.__lat

    def get_long(self):
        return self.__long

    def get_elev(self):#to extend the project
        return self.__elev

    def get_time(self):
        return self.__time


#  it creates an array of Puntos and return an array with all the coordinates in the gpx file.
def get_points(gpx_list):
    position = []

    for track in gpx_list.tracks:
        for segment in track.segments:
            for point in segment.points:
                position.append((Points(point.latitude, point.longitude, point.elevation, point.time)))

    return position
