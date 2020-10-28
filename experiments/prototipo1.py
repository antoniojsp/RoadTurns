import time
from variables import *
start_time = time.time()  # record time

turns = []
end = len(calles)-1
# it returns a 2d list, one is the index and the other is the value


def change(points_list, start, end, saving):
    middle = int((start+end)/2)  # request 3
    global counter
    global request
    request += 3
    counter += 1
    # 0 0 0 0 0 0 0 0 1 1 1 1 1 1 2 2
    if points_list[start] == points_list[middle] and points_list[middle] != points_list[end]:  # right
        # request 1
        request += 1 #middle + 1
        if points_list[middle] != points_list[middle+1]:
            saving.append([middle, points_list[middle]])
        # request 1
        elif points_list[middle+1] != points_list[end]:
            request += 1  #
            medio1 = int(((middle+1+end)/2))
            if points_list[middle+1] == points_list[medio1] == points_list[end]:
                return  # base case, prevents to make more requests.
            else:
                change(points_list, middle+1, end, saving)

    # 0 0 0 0 0 0 0 1 1 1 1 1 1 1
    elif points_list[start] != points_list[middle] and points_list[middle] == points_list[end]:  # left
        # request 1
        request += 1
        if points_list[middle-1] != points_list[middle]:
            saving.append([middle-1, points_list[middle-1]])
        # request 1
        elif points_list[start] != points_list[middle-1]:
            request += 1
            medio2 = int((start+middle-1)/2)
            if points_list[start] == points_list[medio2] == points_list[middle-1]:
                return
            else:
                change(points_list, start, middle-1, saving)

    # if points_list[start] != points_list[middle] != points_list[end]:
    else:
        # 0 0 0 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 2
        request += 1
        if points_list[middle] != points_list[middle+1]:
            saving.append([middle, points_list[middle]])
        request += 1
        if points_list[middle-1] != points_list[middle]:
            saving.append([middle-1, points_list[middle-1]])

        if points_list[start] != points_list[middle]:
            change(points_list, start, middle, saving)
        if points_list[middle] != points_list[end]:
            change(points_list,middle, end, saving)


turns.append([end, calles[end]])

# print index and value
# for i, j in zip(calles, range(0,len(calles))):
#     print("{0} {1}".format(j,i))
request = 0
counter = 0
change(calles, 0, end, turns)
print("Number of calls ", str(counter))
print("Number of request ", str(request))

turns.sort(key=lambda x: x[0])  # sort order

# i=0
# while i < len(turns): # remove repetitive elements next to each other
#     if turns[i][0] == turns[i-1][0]:
#         turns.pop(i)
#         i -= 1
#     i += 1

for i in range(0, len(turns)-1):

    print(calles[turns[i][0]-1])
    print(calles[turns[i][0]])
    print(calles[turns[i][0]+1])
    print()

for i in turns:
    print("{}".format(i))

print("--- %s seconds ---" % (time.time() - start_time))
