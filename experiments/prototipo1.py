import time
from variables import *
start_time = time.time()#record time

turns = []
start = 0
end = len(calles)-1
print(end)
here = 0

turns.append([0, calles[0]])
#it returns a 2d list, one is the index and the other is the value
def change(list, star, end, saving):
    middle = int((start+end)/2)
    global counter
    global salida
    counter+=1
    #request 3
    if list[start] == list[middle] == list[end]:
        salida+=1
        return
        # 0 0 0 0 0 0 0 1 1 1 1 1 1 1
    if (list[start] == list[middle] and  list[middle] != list[end]):#right
        #request 1
        if list[middle] != list[middle+1]:
            saving.append([middle, list[middle]])
        else:
            #request 1
            medio1 = int(((middle+1+end)/2))
            if list[middle+1] == list[medio1] == list[end]:
                return
            else:
                change(list,middle, end, saving)
    # 0 0 0 0 0 0 0 1 1 1 1 1 1 1
    if (list[start] != list[middle] and  list[middle] == list[end]):#left

        # request 1
        if list[middle-1] != list[middle]:
            saving.append([middle-1, list[middle-1]])
        else:
            #request 1
            medio2 = int((start+middle-1)/2)
            if list[start] == list[medio2] == list[middle-1]:
                return
            else:
                change(list, start, middle, saving)

    if list[start] != list[middle] !=  list[end]:
        #0 0 0 0 0 0 1 1 1 1 1 2 2 2 2 2 2
        if list[middle] != list[middle+1]:
            saving.append([middle, list[middle]])
        change(list, start, middle, saving)

        if list[middle-1] != list[middle]:
            saving.append([middle-1, list[middle-1]])
        change(list,middle, end, saving)


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
# while i < len(turns):
#     if turns[i][0] == turns[i-1][0]:
#         turns.pop(i)
#         i-=1
#     i+=1
# # print(turns[1][0])
# for i in calles:
#     print(i)


for i in range(0, len(turns)-1):

    print(calles[turns[i][0]-1])
    print(calles[turns[i][0]])
    print(calles[turns[i][0]+1])
    print()

for i in turns:
    print("{}".format(i))

print("--- %s seconds ---" % (time.time() - start_time))
