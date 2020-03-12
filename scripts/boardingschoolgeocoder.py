# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:41:05 2020

@author: czurm
"""

"""
script that acquires longitude and latitude data for boarding schools
"""
import pandas
import googlemaps

df = pandas.read_csv("../data/boardingschools.csv")
API_KEY = ""
gmaps = googlemaps.Client(key=API_KEY)

for i, row in df.iterrows():

    addr = row['school_name']
    result = gmaps.geocode(addr)
    
    if len(result) > 0:
        df.at[i, 'ADDRESS'] = result[0]["formatted_address"]
        df.at[i, 'LATITUDE'] = result[0]['geometry']['location']['lat']
        df.at[i, 'LONGITUDE'] = result[0]['geometry']['location']['lng']
        print("Added location for record ", i)
        
df.to_csv("../data/boardingschools.csv")