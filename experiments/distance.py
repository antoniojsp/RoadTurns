from getgpx import get_points
import gpxpy
from math import cos, sin, asin, radians, sqrt
# file = open('09_27_20.gpx', 'r')#just for testing, it won't be here in final version
# parseado = gpxpy.parse(file)
# list = get_points(parseado)#array of objects that hold information like lat, long, elev, time. It holds all the info from the gpx file, every point (Look up in getgpx.py to see how the class is defined)

#start and end points in the gpx file. This function will roll over each point and calculate the distance of a segment(from one point to another) and add up to give the total distance.
#The way I have organized everything is that the function that detects changes in street will return the index value where this happens and return the index (among the name of the street)  For instance, the route starts in NW Sprouce Ave (index 0,44.587662, -123.256691) and goes to Higland dr (index 88, 44.587414, -123.2624050 and turns right. Now, if we put start = 0 and end = 88), it returns the distance of all the points between that range.
#calculates distance between two points using the harvestein formula for spheric shapes.
file = open('09_27_20.gpx', 'r')
parseado = gpxpy.parse(file)
list = get_points(parseado)#array of objects that hold information like lat, long, elev, time.


def distance(ini_lat, ini_lon, fin_lat, fin_lon):
	dif_lat = radians(ini_lat) - radians(fin_lat)
	dif_lon = radians(ini_lon) - radians(fin_lon)
	earth_radio = 6371 #radius in km
	distance = (sin(dif_lat/2))**2 + cos(radians(ini_lat)) * cos(radians(fin_lat)) * (sin(dif_lon/2))**2
	distancia = earth_radio * asin(sqrt(distance)) * 2 * 1000 # multiply by 1000 to convert to 	distance in meters
	return distancia

def route_distance(start, end):
	segment = 0
	for i in range(start,end):
		segment+=distance(list[i].get_lat(), list[i].get_long(), list[i+1].get_lat(), list[i+1].get_long())
	return segment

# print("{:0.2f}".format(route_distance(0,88)))
