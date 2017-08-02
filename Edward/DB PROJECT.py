# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 10:32:25 2017

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
db = client.Edward
collection = db.places
collection2= db.temperature
collection.delete_many({})
collection.insert_many(data)

cursor=collection.find()
print("Number of hotels found: ", collection.count())
for doc in cursor:
    geometry=doc['geometry']
    location=geometry['location']
    lt=location['lat']
    ln=location['lng']
    url="http://api.openweathermap.org/data/2.5/weather?lat="+str(lt)+"&lon="+str(ln)+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    weatherresponse=requests.get(url)
    raw=weatherresponse.text
    newrawjson=json.loads(raw)
    want=newrawjson['main']['temp']
    name=doc['name']
    try:
        rating=doc['rating']
    except:
        rating = 0
    temp=want
    
    data2 = '{"Name" : "'+ name +'", "Rating" : '+ str(rating) +', "Temperature" : '+ str(temp)+'}'
    jk=json.loads(data2)
    collection2.insert_one(jk)
cursor2=collection2.find()
cursor2=collection2.find().sort([("Temperature",+1)])
print ("Lowest temperature:", str((cursor2[0]["Temperature"]))+",", (cursor2[0]["Name"]))
print ("Highest temperature:", str((cursor2[collection2.count()-1]["Temperature"]))+",", (cursor2[collection2.count()-1]["Name"]))
cursor=collection.find().sort([("rating",-1)]).limit(1)
for doc in cursor:
    print("Best hotel: ", doc['name'])