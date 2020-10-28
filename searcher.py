from calculations import Mathematica
from multiprocessing.pool import ThreadPool  # multi process
from google import get_name_google


class Route:

    def __init__(self, coord_list):

        self.__arr_gpx = []  # The points from the gpx live here.
        for i in coord_list:
            self.__arr_gpx.append(i)  # filling up __arr_gpx with the points from the gpx file

        self.__pool = [""]*len(coord_list)  # cache, collisions will prevent requesting more data.
        self.__storage = []  # partial results go here.
        self.__end = 0  # useful for testing (allows to check just partially)
        self.__calc = Mathematica()  # for calculations (route_distance, angles)

        self.__a = 0  # count requests TEMPORAL

    def __request(self, parts):  # extract points(by index), get the name address and add the info into the pool array(cache)

        thpool = ThreadPool(processes=1)  # running concurrently
        points_requested = [""]*len(parts) # can request a list of requests.
        for i in parts:
            if self.__pool[i[1]] == "":  # if data is in cache, then no request is made. Pool value used.
                self.__a += 1  # to calculate number of calls
                async_result = thpool.apply_async(get_name_google,(self.__arr_gpx[i[1]].get_lat(), self.__arr_gpx[i[1]].get_long()))
                points_requested[i[0]] = async_result.get()  # holds more than one request.
                self.__pool[i[1]] = points_requested[i[0]]

    def __add_point(self, index):  # for the first and last point:
        self.__storage.append(index)

    def __search_turning(self, start, end):  # look for changing point.
        middle = int((start+end)/2)
        parts_all = [[0, start], [1, middle], [2, end]]  # contains the points that are gonna be requested/checked
        self.__request(parts_all)

        if self.__pool[start] == self.__pool[middle] and self.__pool[middle] != self.__pool[end]:
            parts_right = [[0, middle+1]]  # get the middle point + 1 to test
            self.__request(parts_right)

            if self.__pool[middle] != self.__pool[middle+1]:
                self.__storage.append(middle)
            elif self.__pool[middle+1] != self.__pool[end]:
                medio1 = int(((middle + 1 + end) / 2))
                parts_right_medio = [[0, medio1 + 1]]
                self.__request(parts_right_medio)
                if self.__pool[middle + 1] == self.__pool[medio1] == self.__pool[end]:
                    return
                else:
                    self.__search_turning(middle + 1, end)

        elif self.__pool[start] != self.__pool[middle] and self.__pool[middle] == self.__pool[end]:
            parts_left = [[0,middle-1]]
            self.__request(parts_left)

            if self.__pool[middle-1] != self.__pool[middle]:
                self.__storage.append(middle - 1)
            elif self.__pool[start] != self.__pool[middle - 1]:
                medio2 = int(((start + middle - 1) / 2))
                parts_left_medio = [[0, medio2]]
                self.__request(parts_left_medio)
                if self.__pool[start] == self.__pool[medio2] == self.__pool[middle - 1]:
                    return
                else:
                    self.__search_turning(start, middle - 1)

        else:
            # 0 0 0 0 0 1 1 1 1 2 2 2 2
            parts_different = [[0, middle + 1], [1, middle - 1]]
            self.__request(parts_different)

            if self.__pool[middle - 1] != self.__pool[middle]:
                self.__storage.append(middle - 1)

            if self.__pool[middle] != self.__pool[middle + 1]:
                self.__storage.append(middle)
            #  will continue dividing and searching.

            if self.__pool[start] != self.__pool[middle]:
                self.__search_turning(start, middle)

            if self.__pool[middle] != self.__pool[end]:
                self.__search_turning(middle + 1, end)

    def __direction(self):  # array of indexes
        result = []  # holds all the information
        rango = 5  # range of search for change in direction of the route.
        corners = []
        turn_list = []

        # turn_list.append("Start")
        # result.append()  # 2d array to hold addresses, distance, turning, index

        print(self.__storage)

        for i in range(0, len(self.__storage)-1):

            degree = 0
            degree = self.__calc.turning(self.__arr_gpx, self.__storage[i], rango)

            if degree == "Right" or degree == "Left" or i == 0:
                corners.append(self.__storage[i])
                turn_list.append(degree)

        # AQUI SEGUIR
        print(corners)
        size = len(corners)
        print(size)
        for i in range(0, size-1):
            coord_index_start = corners[i]
            coord_index_end = corners[i+1]
            meters = self.__calc.route_distance(self.__arr_gpx, coord_index_start, coord_index_end)

            if self.__pool[coord_index_start+1] == "":
                street_name = get_name_google(self.__arr_gpx[coord_index_start+1].get_lat(), self.__arr_gpx[coord_index_start+1].get_long())
            else:
                street_name = self.__pool[coord_index_start+1]

            result.append([coord_index_start+1, turn_list[i], meters, street_name, self.__arr_gpx[coord_index_start+1].get_lat(), self.__arr_gpx[coord_index_start+1].get_long()])

        ending = corners[size-1]
        result.append([ending, "End", 0, self.__pool[ending], self.__arr_gpx[ending].get_lat(), self.__arr_gpx[ending].get_long()])

        return result

    def result(self, start, end):
        self.__add_point(0) # maybe remove
        self.__end = end  # random for testing
        self.__search_turning(start, end)
        print(self.__pool)
        print(self.__a)
        self.__add_point(self.__end)  # add first and last points to MAYBE REMOVE
        list.sort(self.__storage)  # indicate the start and the end

        i = 1
        while i < len(self.__storage):  # remove repetitive elements next to each other
            if self.__storage[i] == self.__storage[i - 1]:
                self.__storage.pop(i)
                i -= 1
            i += 1

        final = self.__direction()  # put things everything together.

        return final
