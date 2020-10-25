#FINDS THE TURNING POINTS, IT RETURNS THE NAMES AND THE NUMBER OF THE INDEX WHERE THE TURNS ARE.
#it gets the info  from the points from the gpx files and perform a recursion search
#to get the points where the streets changes. used the module "google" from where it connects to google
#maps and get the name of the address where some point (lat,long) is located.
#returns and 2d Array witht [gpx index number, name of streets, latitude, longitud]
#latest version (10/20/20)
import googlemaps
import json
from google import get_name_google
from getgpx import *
import gpxpy
import math
from math import cos, sin, asin, radians, sqrt

# from distance import distance
from multiprocessing.pool import ThreadPool#multi process
# import threading
# from multiprocessing import Process#to run concurrently.

#Class will return 2d array with the result of the route
class Route:

    def __init__(self, list):
        self.__arr = []#The points from the gpx live here.
        for i in list:
            self.__arr.append(i)#filling up __arr with the points from the gpx file
        self.__pool = [""]*len(list)#cache to reduce the number of requests, collisions will prevent requesting more data.
        self.__storage =[]#partial results go here.
        self.__end = 0

    def __request(self,parts):#extract points, get the name address and add the info into the pool array(cache)
        thpool = ThreadPool(processes=1)#running concurrently
        interpolate = [""]*len(parts)# can request a list of requests.
        for i in parts:
            if self.__pool[i[1]] == "":#if the data is in the cache array, it will not request the data but use the one from the pool array
                # print(i[1])
                async_result = thpool.apply_async(get_name_google,(self.__arr[i[1]].get_lat(), self.__arr[i[1]].get_long()))
                interpolate[i[0]] = async_result.get()#holds more than one request.
                self.__pool[i[1]] = interpolate[i[0]]


    def __add_point(self, index):#for the first and last point:
        self.__storage.append(index)

    def __change(self, start, end):#list contains all the points, start first point, end last one and storage saves the results.
        middle = int((start+end)/2)
        parts1 = [[0,start],[1,middle],[2,end]]
        self.__request(parts1)
        # base case: when  the start, the middle and the end is the same.
        if self.__pool[start] == self.__pool[middle] and self.__pool[middle] == self.__pool[end]:
            return

        # when start and middle are equal and middle and end not equal(or viceverse), possible indication of a point of change.
        if (self.__pool[start] == self.__pool[middle] and  self.__pool[middle] != self.__pool[end]) or (self.__pool[start] != self.__pool[middle] and  self.__pool[middle] == self.__pool[end]):
            parts2 = [[0,middle+1], [1,middle-1]]
            self.__request(parts2)

            #checks if the next point from the middle is different, if it is, change detected and added.
            if  self.__pool[middle-1] != self.__pool[middle]:
                self.__storage.append(middle)
            elif self.__pool[start] != self.__pool[middle]:
                self.__change(start, middle)

            if self.__pool[middle] != self.__pool[middle+1]:
                self.__storage.append(middle+1)
            elif self.__pool[middle] != self.__pool[end]:
                self.__change(middle, end)

        else:
            parts3 = [[0,middle+1], [1,middle-1]]
            self.__request(parts3)
            if self.__pool[middle-1] != self.__pool[middle]:
                self.__storage.append(middle)

            elif self.__pool[middle] != self.__pool[middle+1]:
                self.__storage.append(middle)
            #will continue dividing and searching.

            self.__change(start, middle)
            self.__change(middle+1, end)

    def __route_distance(self, start, end):
        segment = 0
        for i in range(start, end):
            segment+=self.__distance(self.__arr[i].get_lat(), self.__arr[i].get_long(), self.__arr[i+1].get_lat(), self.__arr[i+1].get_long())
        return segment

    def __direction(self):#array of indexes
        result = []#holds all the information
        turn = ""
        rango = 20
        passed = []###
        turn_list = []
        meters_list = []

        result.append([])#2d array to hold addreses, distance, turning, index
        for i in range(0,len(self.__storage)-1):
            degree = 0
            if i == 0:
                degree = 180
            else:
                a = [self.__arr[self.__storage[i]-rango].get_lat(), self.__arr[self.__storage[i]-rango].get_long()]
                b = [self.__arr[self.__storage[i]].get_lat(), self.__arr[self.__storage[i]].get_long()]
                c = [self.__arr[self.__storage[i]+rango].get_lat(), self.__arr[self.__storage[i]+rango].get_long()]
                degree = self.__get_angle(a,b,c)

            if degree < 130 or degree > 240 or i == 0:
                if i == 0:
                    turn = "Start"
                if degree >240:
                    turn = "Right"
                elif degree <130:
                    turn = "Left"

            passed.append(self.__storage[i])
            turn_list.append(turn)

        size = len(passed)
        for i in range(0,size-1):
            temp = passed[i]
            temp1= passed[i+1]
            meters = self.__route_distance(temp, temp1)

            result.append([temp, turn_list[i], meters, self.__pool[temp], self.__arr[temp].get_lat(), self.__arr[temp].get_long()])

        ending = passed[size-1]
        result.append([ending, "End", 0, self.__pool[ending], self.__arr[ending].get_lat(), self.__arr[ending].get_long()])
        return result

    def __get_angle(self,a, b, c):
        angular = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))

        return angular + 360 if angular < 0 else angular

    def __distance(self,ini_lat, ini_lon, fin_lat, fin_lon):
    	dif_lat = radians(ini_lat) - radians(fin_lat)
    	dif_lon = radians(ini_lon) - radians(fin_lon)
    	earth_radio = 6371 #radius in km
    	distance = (sin(dif_lat/2))**2 + cos(radians(ini_lat)) * cos(radians(fin_lat)) * (sin(dif_lon/2))**2
    	distancia = earth_radio * asin(sqrt(distance)) * 2 * 1000 # multiply by 1000 to convert to 	distance in meters
    	return distancia


    def result(self,start,end):
        self.__add_point(0)
        self.__end = end#random for testing
        self.__change(start,end)
        # print(self.__pool)
        self.__add_point(self.__end)#add first and last points to
        list.sort(self.__storage)# indicate the start and the end
        # print(self.__storage)
        final = self.__direction()#put things everything together.

        return final
