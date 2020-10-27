import googlemaps
import json
import time
start_time = time.time()

import configparser#import the key from secret file
config = configparser.ConfigParser()
config.read("credentials.ini")#stored keys outside respository.
#google version getting name. Uses googlemaps module. and the key is kept secret
location = [44.860538, -123.188995]#for testing


def get_name_google(lat, long):

    gmaps = googlemaps.Client(key=config["DEFAULT"]["key_google"])#personal API key
    result = gmaps.reverse_geocode((lat, long))#gets json

    for i in range(0, len(result)-1):
        for j in range(0, len(result[i]['address_components'])-1):
            if result[i]['address_components'][j]['types'] == ['route'] and result[i]['geometry']['location_type'] == 'GEOMETRIC_CENTER':
                address = result[i]['address_components'][j]["short_name"]
                break
                # print("Route:\n")
                # print(result[i]['address_components'][j]["short_name"])
                # print()
                # print('------------\n')
    return address


print(get_name_google(location[0], location[1]))

# {'bounds': {'northeast': {'lat': 44.7284721, 'lng': -123.3019064}, 'southwest': {'lat': 44.7199568, 'lng': -123.3051163}}, 'location': {'lat': 44.724232, 'lng': -123.3037171}, 'location_type': 'GEOMETRIC_CENTER', 'viewport': {'northeast': {'lat': 44.7284721, 'lng': -123.3019064}, 'southwest': {'lat': 44.7199568, 'lng': -123.3051163}}}
