import googlemaps
import json
import time
# start_time = time.time()

import configparser#import the key from secret file
config = configparser.ConfigParser()
config.read("credentials.ini")#stored keys outside respository.
#google version getting name. Uses googlemaps module. and the key is kept secret
# location = [44.848629,-123.237274]#for testing

#WORKING
def get_name_google(lat, long):
    gmaps = googlemaps.Client(key=config["DEFAULT"]["key_google"])#personal API key
    result = gmaps.reverse_geocode((lat, long))#gets json

    for i in range(0, len(result)-1):
        for j in range(0, len(result[i]['address_components'])-1):
            #the Geometric_center is the tag that indicates the exact point, so we avoid problems with houses that are in front of 2 different streets.
            if result[i]['address_components'][j]['types'] == ['route'] and result[i]['geometry']['location_type'] == 'GEOMETRIC_CENTER':
                address = result[i]['address_components'][j]["short_name"]
                break
    return address


# print(get_name_google(location[0], location[1]))
# print(get_name_google(location[0],location[1]))
# print("--- %s seconds ---" % (time.time() - start_time))
