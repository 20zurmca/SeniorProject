# -*- coding: utf-8 -*-
"""
script that acquires longitude and latitude data for foreign schools
"""
import pandas
import googlemaps

df = pandas.read_csv("../data/International_High_Schools.csv")
API_KEY = "" #your api key
gmaps = googlemaps.Client(key=API_KEY)

for i, row in df.iterrows():
    address = None
    if row['ADDRESS1']:
        address = row['ADDRESS1']
    else:
        address = row['ADDRESS2']
    
    ls = [row['INSTITUTION'],
          address,
          row['CITY'],
          row['PROVINCE'],
          row['ZIP'],
          row['COUNTRY']]
    
    addr = ' '.join(str(v) for v in ls)
    result = gmaps.geocode(addr)
    
    if len(result) > 0:
        df.at[i, 'LATITUDE'] = result[0]['geometry']['location']['lat']
        df.at[i, 'LONGITUDE'] = result[0]['geometry']['location']['lng']
        print("Added location for record ", i)
        
df.to_csv("../data/International_High_Schools.csv")
