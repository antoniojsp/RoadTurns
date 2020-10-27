#EXTRACT INFORMATION FROM TAMU. THRE IS TWO VERSIONS, GOOGLE AND TAMU.

import requests
import configparser
config = configparser.ConfigParser()
config.read("credentials.ini")#save key outside repository

#location = [44.587471,-123.260834]

def get_name_tamu(lat, long):
    endpoint = "https://geoservices.tamu.edu/Services/ReverseGeocoding/WebService/v04_01/Rest/"#service
    data = {'apiKey':config["DEFAULT"]["key_tamu"],#parameters
            'lat':lat,
            'lon':long,
            'format':'json',
            'notStore':'false',
            'version':'4.10'}

    respuesta = requests.get(url = endpoint, data = data)#request
    response = respuesta.json()#transform to json
    result = response['StreetAddresses'][0]['StreetAddress'].split()#only gets the address of the avenue or street
    # remove the addres number, leaving only the street or avenue name.
    result.pop(0)#remove house number
    return ' '.join(result)#transform list to string


#print(get_name_tamu(location[0],location[1]))
