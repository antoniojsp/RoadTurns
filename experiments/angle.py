import math
#function that calculate the angle of three points.

#  input 3 points (two rays and one vertex), output (degree form by the 2 rays and the vertex)
def get_angle(arm_a, vertex, arm_c):
    angular = math.degrees(math.atan2(arm_c[1]-vertex[1], arm_c[0]-vertex[0]) - math.atan2(arm_a[1]-vertex[1], arm_a[0]-vertex[0]))
    angle = angular + 360 if angular < 0 else angular
    return angle

def turning(list, center, range):
    try:
        a = [list[center - range].get_lat(), list[center - range].get_long()]
        b = [list[center].get_lat(), list[center].get_long()]
        c = [list[center + range].get_lat(), list[center + range].get_long()]
        grados = get_angle(a, b, c)
    except:
        grados = 0

    turn_direction = ""
    print(grados)
    if grados > 210:
        turn_direction = "Right"
    elif grados < 150:
        turn_direction = "Left"
    else:
        turn_direction = "Straight"

    return turn_direction

# 89 right
# a = [44.58741,-123.261917]
# b = [44.587433, -123.262444]
# c = [44.587746,-123.262482]

# #17 stright
# a = [44.587616, -123.256828]
# b = [44.587601, -123.257408]
# c = [44.58741, -123.261917]

# stright
a = [44.590939,-123.262029]
b = [44.590963,-123.260769]
c = [44.591028,-123.259405]


print(get_angle(a,b,c))