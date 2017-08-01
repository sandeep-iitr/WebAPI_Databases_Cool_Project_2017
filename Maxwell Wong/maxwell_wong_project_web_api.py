# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 09:09:54 2017

@author: Maxwell
"""

import requests
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.705311,-74.2581937&radius=10000&type=hotels&keyword=stay&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
response=requests.get(url)
#print (response.text)

import json
rawdata=response.text
rawjson=json.loads(rawdata)
data=rawjson["results"]
if len(data)>1:
    print ("There are" , len(data) , "hotels near you")
else:
    print ("There is" , len(data) , "hotel near you")

import pymongo
from pymongo import MongoClient
client=MongoClient()
db=client.test_database
collection=db.test_collection
collection.delete_many({})
data_id=collection.insert_many(data)

cursor=collection.find()

collection.create_index([("rating",pymongo.DESCENDING)])
cursor=collection.find().sort("rating",pymongo.DESCENDING)

temp=[]
locations={}
for doc in cursor:
    print (doc["name"])
    latitude=(doc["geometry"]["location"]["lat"])
    longitude=(doc["geometry"]["location"]["lng"])
    weather_url="http://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&units=imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    weather=requests.get(weather_url)
    weather_data=weather.text
    weather_json=json.loads(weather_data)
    #temp.append(weather_json["main"]["temp"])
    #ocations[doc["name"]]=weather_json["main"]["temp"]
    storage=(doc['name'],weather_json['main']['temp'])
    temp.append(storage)

rate=collection.find().sort("rating",pymongo.DESCENDING).limit(1)
for x in rate:
    print ("The highest rating hotel is" , x["name"])
    

def order(item):
    return item[0]
#print (sorted(temp,key=order))
print ("The hottest hotel is" , temp[0][0])
print ("The coolest hotel is" , temp[-1][0])





        
    