import pandas as pd
import requests
import json
df=pd.read_csv("apt_results.csv")
#print(df.head())

for i,row in df.iterrows():
    apiAddress = str(df.at[i,'Address'])
    #print(apiAddress)

    parameters={
        "key": "YOUR KEY",
        "location" : apiAddress
    }
    response = requests.get("http://www.mapquestapi.com/geocoding/v1/address", params = parameters)
    #print(response)
    data = json.loads(response.text)['results']

    #data=response.text
    lat = (data[0]['locations'][0]['latLng']['lat'])
    lng = (data[0]['locations'][0]['latLng']['lng'])
    #print(lat,lng)
    df.at[i,'Lng'] = lng
    df.at[i,'Lat'] = lat

df.to_csv('apt_Geo.csv')
