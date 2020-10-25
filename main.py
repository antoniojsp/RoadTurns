# from google import get_name_google
from getgpx import get_points
# from distance import distance
# from multiprocessing.pool import ThreadPool#multi process
import gpxpy
import time
# import threading
from searcher import *
from getgpx import *

from multiprocessing import Process#to run concurrently.

start_time = time.time()#record time
#get the points from the gpx file
file = open('09_27_20.gpx', 'r')#for testing, it won't be here for final version
parseado = gpxpy.parse(file)
list = get_points(parseado) #array of objects that hold information like lat, long, elev, time.
points = Route(list)
print(len(list))
# resultado = points.result(0, 100)


thpool = ThreadPool(processes=1)#running concurrently

async_result = thpool.apply_async(points.result,(0,250))
lista1 = async_result.get()#holds more than one request.

async_result = thpool.apply_async(points.result,(251,500))
lista2 = async_result.get()#holds more than one request.

for i in lista1:
    print(i)

for j in lista2:
    print(j)
# lista3 = lista1 + lista2
#
# lista3.sort()
# print(lista3)

print("--- %s seconds ---" % (time.time() - start_time))
