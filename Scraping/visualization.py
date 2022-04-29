import pandas as pd
import folium
from folium.plugins import MarkerCluster
m=folium.Map(location=[34.02266241276261, -118.28518154983786],titles='OpenStreeMap',zoom_start=13)

#folium.Marker(location=[34.07911,-118.317042],popup='TEXT',icon=folium.Icon(color='blue')).add_to(m)
#folium.Marker(location=[34.101634,-118.324684],popup='TEXT1',icon=folium.Icon(color='red')).add_to(m)

df = pd.read_csv('apt_Geo.csv')

markerCluster = MarkerCluster().add_to(m)
for i,row in df.iterrows():
    lat = df.at[i,'Lat']
    lng = df.at[i,'Lng']
    price = df.at[i,'Price']

    popup=df.at[i,'Price'] + '<br>' + '<br>' + str(df.at[i,'Name']) + '<br>' + '<br>' + str(df.at[i,'Address'])

    folium.Marker(location=[lat, lng], popup=popup, icon=folium.Icon(color='blue')).add_to(markerCluster)



m.save('index.html')