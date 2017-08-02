#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:48:43 2017

@author: jinalee
"""

import pymongo
from pymongo import MongoClient
import json
import requests



#i have changed my file




#hotel search
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.703749, -73.820798&radius=10000&type=hotels&keyword=hotel&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
response = requests.get(url)


rawdata=response.text
rawjson=json.loads(rawdata)
data=rawjson['results']

#making collection of hotels
client = MongoClient()
db = client.test_database
collection = db.test_collection
collection.delete_many({})
data_id = collection.insert_many(data)
cursor=collection.find()

#making a second collection to contain hotel name, rating, and weather data
collection2 = db.test_collection2
collection2.delete_many({})

#sets up a loop to find weather conditions for each hotel
for doc in cursor: 

    #weather api
    weatherurl="http://api.openweathermap.org/data/2.5/weather?lat="+str(doc["geometry"]["location"]["lat"])+"&lon="+str(doc["geometry"]["location"]["lng"])+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    weatherresponse = requests.get(weatherurl)
    
    rawdata = weatherresponse.text
    rawjson = json.loads(rawdata)
    data = rawjson['main']
    
    #data
    d = '{"Name" : "'  + doc["name"] + '", "Weather" : "'+ str(data["temp"])+'"}'
    if "rating" in doc:
        d = '{"Name" : "' + doc["name"] + '", "Rating" : "' + str(doc["rating"])+ '", "Weather" : "'+ str(data["temp"])+'"}'
    
    j = json.loads(d)
    data_id = collection2.insert_one(j).inserted_id
    
    
#hotels    
cursor = collection2.find()
print(collection2.count(), "hotels in the area:")
for doc in cursor:
    print(doc["Name"])
    
#ratings
cursor=collection2.find().sort([("Rating",-1)])
ratings = collection2.find().sort([("Rating",-1)]).limit(2)
    
print("\n")
print("2 highest rated hotel:")
for i in ratings:
    print(i["Name"])
    print("Rating:", i["Rating"])


#highest and lowest temperature
weather = collection2.find().sort([("Weather",-1)]).limit(1)
    
print("\n")
print("Hotels with the highest temperatures: ")
for i in cursor:
    j = weather[0]["Weather"]
    if j == i["Weather"]:
        print(i["Name"])
        print("Temperature:",j)
        
cursor = collection2.find()
weather2 = collection2.find().sort([("Weather",1)]).limit(1)
            
print("\n")
print("Hotels with the lowest temperatures: ")
for i in cursor:
    j = weather2[0]["Weather"]
    if j == i["Weather"]:
        print(i["Name"])
        print("Temperature:",j)
        









