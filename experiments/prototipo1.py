import time
from variables import *
start_time = time.time()  # record time

turns = []
start = 0
end = len(calles)-1
# it returns a 2d list, one is the index and the other is the value


def change(points_list, start, end, saving):
    middle = int((start+end)/2)
    global counter
    global salida
    counter+=1
    #  request 3
    # if points_list[start] == points_list[middle] == points_list[end]:
    #     salida+=1
    #     return
    if points_list[start] == points_list[middle] and points_list[middle] != points_list[end]:  # right
        # request 1
        if points_list[middle] != points_list[middle+1]:
            saving.append([middle, points_list[middle]])
        else:
            # request 1
            medio1 = int(((middle+end)/2))
            if points_list[middle] == points_list[medio1] == points_list[end]:
                return  # base case, prevents to make more requests.
            else:
                change(points_list, middle, end, saving)
    # 0 0 0 0 0     0 0 1 1 1 1 1 1 1
    if points_list[start] != points_list[middle] and points_list[middle] == points_list[end]:  # left
        # request 1
        if points_list[middle-1] != points_list[middle]:
            saving.append([middle-1, points_list[middle-1]])
        else:
            # request 1
            medio2 = int((start+middle)/2)
            if points_list[start] == points_list[medio2] == points_list[middle]:
                return
            else:
                change(points_list, start, middle, saving)

    if points_list[start] != points_list[middle] != points_list[end]:
        # 0 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 2
        if points_list[middle] != points_list[middle+1]:
            saving.append([middle, points_list[middle]])

        if points_list[middle-1] != points_list[middle]:
            saving.append([middle-1, points_list[middle-1]])
        change(points_list, start, middle, saving)
        change(points_list,middle, end, saving)


turns.append([end, calles[end]])

#print index and value
# for i, j in zip(calles, range(0,len(calles))):
#     print("{0} {1}".format(j,i))

counter = 0
salida = 0
change(calles, start, end, turns)
print("entrada ", str(counter))
print("salida ", str(salida))
turns.sort(key=lambda x: x[0])#sort order

i=0
while i < len(turns):
    if turns[i][0] == turns[i-1][0]:
        turns.pop(i)
        i-=1
    i+=1



for i in range(0, len(turns)-1):

    print(calles[turns[i][0]-1])
    print(calles[turns[i][0]])
    print(calles[turns[i][0]+1])
    print()

for i in turns:
    print("{}".format(i))

print("--- %s seconds ---" % (time.time() - start_time))
