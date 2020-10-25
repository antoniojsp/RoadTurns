from calculations import Mathematica
from multiprocessing.pool import ThreadPool#multi process
from google import get_name_google

#

class Route:

    def __init__(self, list):

        self.__arr = []  # The points from the gpx live here.
        for i in list:
            self.__arr.append(i)  # filling up __arr with the points from the gpx file

        self.__pool = [""]*len(list)  # cache, collisions will prevent requesting more data.
        self.__storage =[] # partial results go here.
        self.__end = 0
        self.__calculations = Mathematica()

    def __request(self, parts):  # extract points, get the name address and add the info into the pool array(cache)

        thpool = ThreadPool(processes=1)  # running concurrently
        interpolate = [""]*len(parts) # can request a list of requests.
        for i in parts:
            if self.__pool[i[1]] == "":  # if data is in cache, then no request is made. Pool value used.
                # print(i[1])
                async_result = thpool.apply_async(get_name_google,(self.__arr[i[1]].get_lat(), self.__arr[i[1]].get_long()))
                interpolate[i[0]] = async_result.get()  # holds more than one request.
                self.__pool[i[1]] = interpolate[i[0]]

    def __add_point(self, index):  # for the first and last point:
        self.__storage.append(index)

    def __change(self, start, end):  # look for changing point.
        middle = int((start+end)/2)
        parts1 = [[0,start],[1,middle],[2,end]]
        self.__request(parts1)
        # base case: when  the start, the middle and the end is the same.
        if self.__pool[start] == self.__pool[middle] and self.__pool[middle] == self.__pool[end]:
            return

        # Check what side of then array needs to be checked.
        if (self.__pool[start] == self.__pool[middle] and  self.__pool[middle] != self.__pool[end]) or (self.__pool[start] != self.__pool[middle] and  self.__pool[middle] == self.__pool[end]):
            parts2 = [[0,middle+1], [1,middle-1]]
            self.__request(parts2)

            #  checks if the next point from the middle is different, if it is, change detected and added.
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
            #  will continue dividing and searching.

            self.__change(start, middle)
            self.__change(middle+1, end)

    def __direction(self):  # array of indexes
        result = []  # holds all the information
        turn = ""
        rango = 20
        passed = []
        turn_list = []
        meters_list = []

        result.append([])  # 2d array to hold addresses, distance, turning, index
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

    def result(self,start,end):
        self.__add_point(0)
        self.__end = end  # random for testing
        self.__change(start,end)
        print(self.__pool)
        self.__add_point(self.__end)  # add first and last points to
        list.sort(self.__storage)  # indicate the start and the end
        final = self.__direction()  # put things everything together.

        return final
