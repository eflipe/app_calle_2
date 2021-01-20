import requests
import os


# 'at': '{},{}'.format(latitude,longitude),
# at=[-34.6131, -58.3772]
def api_here(latitude, longitude):

    URL = os.environ.get("URL_HERE")
    api_key = os.environ.get("API_KEY_HERE") # Acquire from developer.here.com

    location = "Buenos Aires"
    at = '{},{}'.format(latitude, longitude)
    PARAMS = {'apikey':api_key, 'at':at}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    latitude = data['items'][0]['position']['lat']
    longitude = data['items'][0]['position']['lng']
    address = data['items'][0]['address']['label']
    street = data['items'][0]['address']['street']
    city = data['items'][0]['address']['city']
    # district = data['items'][0]['address']['district']

    # print(latitude)
    # print(longitude)
    print("ADDRESS API HERE", address)
    print("STREET", street)
    # print(district)
    return [api_key, latitude, longitude, address, city, street]
