import requests
import os
import dill
import time
import matplotlib.pyplot as plt
import pandas as pd
import API_return.py

"""
Data is imported from Yelp API: https://api.yelp.com/v3/businesses/search by passing latitude longitude information. 
The latitude longitude information is obtained from h3 by entering NYC (without Staten Islande) and creating hexagons 
of size 9 to generate hexagon centroid location information. The idea is to find the restaurants in each of these 
hexagons as the clustering basis for the ML model (previously ZIP code was considered, but this may be ambiguous and 
large in terms of area).

The data downloading function below to work around Yelps API limit. Yelp has a limit of a max of 5000 requests 
per day and 1000 requests using a continuous loop with offset. Due to this, H3 hexagons were selected such that 
each hexagon can request a smaller amount of data (under 1000 worst case). Using a hexagon size of ~400m, a total 
of ~6000 hexagon coorinates are obtained. These coordinates are split into three files to work around Yelp's daily 
limit and are used to import data into three .pkd files. The data is imported and stored in 1) A list of 2000 
locations with all restaurants in them and 2) A dictionary with the key as the coordinate number of that sublist 
and value as the restaurants in them, for each of the three files. Reason for doing 2 is to identify empty hexagons 
easily or hexagons (or coordinates) that are dense.
"""

#API key needs to be obtained by making an dev account at Yelp. The key is stored in another file that is imported.
API_key=API_return()

ENDPOINT='https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization':API_key}

#Hex-centers are obtained using h3 from another python file and saves latitude/longitude information of the hexs.
#These Hex's cover all of NYC except Staten Island
lat_long_full=pd.read_csv('hex-centers.csv',usecols=['0','1'])

#To work around Yelp's daily limit of 5000, the total hex location data is divided into 3 batches to be safe.
batch1=lat_long[:2000]
batch2=lat_long[2000:4000]
batch2=batch2.reset_index(drop=True)
batch3=lat_long[4000:]
batch3=batch3.reset_index(drop=True)

#Function to hit Yelp's API and obtain information for the "food" options in New York City based on the Hex data from
#each batch
def yelpapi_reader(lat_long,ENDPOINT,HEADERS):
    data_dict = {}
    empty_hex = []
    full_hex = []
    data_batch1 = []
    for k in range(len(lat_long)):
        lat = lat_long.loc[k][0]
        long = lat_long.loc[k][1]
        data_coll = []
        for i in range(19):
            j = i + 1

            PARAMETERS = {'categories': 'food',
                          'latitude': lat,
                          'longitude': long,
                          'limit': 50,
                          'offset': 50 * i,
                          'radius': 400
                          }

            response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
            data = response.json()
            data_coll.extend(data['businesses'])
            print(response.status_code, f"latlongset:{k}", f"request#{j}", "Number of businesses:",
                  i * 50 + len(data['businesses']))
            data_dict[k] = data_coll

            if len(data['businesses']) == 0 and i == 0:
                print(response.status_code, f"{lat},{long} IS EMPTY")
                empty_hex.append(k)
                break

            elif len(data['businesses']) != 50:
                print(response.status_code, f"No more locations in {lat},{long}")
                break

            if j == 20:
                full_hex.append(k)
                break
        data_batch1.extend(data_coll)
    return data_dict

#Obtaining data for each batch of latitude/longitude
data_batch1=yelpapi_reader(batch1)
data_batch2=yelpapi_reader(batch2)
data_batch3=yelpapi_reader(batch3)

#Saving the information for all food options in each batch of locations
dill.dump(data_batch1, open('allfood_latlong_batch1.pkd', 'wb'))
dill.dump(data_batch2, open('allfood_latlong_batch2.pkd', 'wb'))
dill.dump(data_batch3, open('allfood_latlong_batch3.pkd', 'wb'))

#Saving the information for all food options in each batch of locations in dictionary format
dill.dump(data_dict1, open('dict_latlong_batch1.pkd', 'wb'))
dill.dump(data_dict2, open('dict_latlong_batch2.pkd', 'wb'))
dill.dump(data_dict3, open('dict_latlong_batch3.pkd', 'wb'))
