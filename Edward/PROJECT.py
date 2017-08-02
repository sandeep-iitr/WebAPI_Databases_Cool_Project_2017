# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 15:55:05 2017

@author: EE113D
"""
import requests
url= "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7828687,-73.9675438&radius=10000&type=hotels&keyword=hotel&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
response = requests.get(url)

import json
rawdata=response.text
rawjson=json.loads(rawdata)
data=rawjson['results']

import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.test_database
collection = db.test_collection
collection.delete_many({})
data_id = collection.insert_many(data)

cursor=collection.find()
print("Number of hotels found: ", collection.count())
lst=[]
for doc in cursor:
    geometry=doc['geometry']
    location=geometry['location']
    lt=location['lat']
    ln=location['lng']
    url="http://api.openweathermap.org/data/2.5/weather?lat="+str(lt)+"&lon="+str(ln)+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    weatherresponse=requests.get(url)
    raw=weatherresponse.text
    newrawjson=json.loads(raw)
    want=newrawjson['main']['temp'], (doc['name'])
    try:
        rating=doc['rating']
    except:
        rating = 0
    lst.append(want)
lst.sort()
print ("Hotel with lowest temperature: ", lst[0])
print ("Hotel with highest temperature: ", lst[collection.count()-1])
collection.create_index([('rating',pymongo.DESCENDING)] )
cursor=collection.find().sort([("rating",-1)]).limit(1)
for doc in cursor:
    print("Best hotel: ", doc['name'])
    
