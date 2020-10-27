import gpxpy
from getgpx import get_points

file = open('09_27_20.gpx', 'r')
parseado = gpxpy.parse(file)
position = get_points(parseado)#array of objects that hold information like lat, long, elev, time.

with open("improved_results.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

list=[]
for i in content:
    if i != "":
        temp = (i.replace(']', ''))
        temp1 = (temp.replace('[', ''))
        temp2 = (temp1.replace(',', ''))
        # parte = (temp1.replace(',', ''))
        # print(parte)
        numero = temp2.split(" ")
        list.append(numero[0].strip())

for i in list:

    print("{},".format(i),end="")
# for i in list:
#     print("{0},{1}\n".format(position[i].get_lat(), position[i].get_long())
#
# for j in list:
#     print("{0}".format(j,','),end=" ")
