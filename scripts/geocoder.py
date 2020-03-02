# -*- coding: utf-8 -*-
"""
script that acquires longitude and latitude data for foreign schools
"""
import pandas
from arcgis import GIS, geocoding

gis = GIS()
df = pandas.read_csv("../data/International_High_Schools.csv")
geocode = geocoding.geocode


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
    
    result = geocode(address = { 'SingleLine': addr})
    
    if len(result) > 0:
        df.at[i, 'LATITUDE'] = result[0]['location']['y']
        df.at[i, 'LONGITUDE'] = result[0]['location']['x']
        print("Added location for record ", i)
        
df.to_csv("../data/International_High_Schools.csv")
