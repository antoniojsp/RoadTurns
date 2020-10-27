import time
from variables import *
start_time = time.time()#record time

turns = []
start = 0
end = len(calles)-1
here = 0

def change(list, start, end, saving,i):
    middle = int((start+end)/2)
    if start == middle:
        return
    i+=1
    print(here)
    if  list[middle-1] != list[middle]:
        saving.append([middle-1, list[middle-1]])
    if list[middle] != list[middle+1]:
        saving.append([middle, list[middle]])
    change(list,start, middle, saving,i)
    change(list, middle+1, end, saving,i)

#print index and value
# for i, j in zip(calles, range(0,len(calles))):
#     print("{0} {1}".format(j,i))
change(calles, start, end, turns,here)
#order
turns.sort(key=lambda x: x[0])#sort order
# print([i for i in turns])

# clean for repetition

i=0
while i < len(turns):
    if turns[i][0] == turns[i-1][0]:
        turns.pop(i)
        i-=1
    i+=1

for i in range(0, len(turns)-1):
    print (calles[turns[i][0]-1])
    print (calles[turns[i][0]])
    print (calles[turns[i][0]+1])
    print()

# print(len(calles))
for i in turns:
    print("{}".format(i))
print("--- %s seconds ---" % (time.time() - start_time))
