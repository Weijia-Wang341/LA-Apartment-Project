import pandas as pd
import json
import requests

myurl='YOUR CLOUD'
df=pd.read_csv('apt_results.csv')
df.reset_index()
a=df.to_json(orient='records')
b=json.loads(a)
requests.put(myurl,json=b)
