# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 09:15:04 2017

@author: ttieu
"""

#get data
import requests
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.705311,-74.2581937&radius=10000&type=hotels&keyword=stay&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
response = requests.get(url)
#print(response.text)

#parse json
import json
rawdata=response.text
rawjson=json.loads(rawdata)
data=rawjson['results']

#num of hotels
if len(data)!=1:
    print("Here are", len(data), "hotels under a 10,000 km radius near you:")
    print("(Listed by rating")
else:
    print("Here is one hotel near you:")

#insert into MongoDB
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.test_database
collection = db.test_collection
collection.delete_many({})
data_id = collection.insert_many(data)
    
#Prints Hotel by rating

    
#Finding Highest Temperature
hotel_temp={}
cursor=collection.find().sort([("rating",-1)])

count=1
for doc in cursor:
    lat=doc['geometry']['location']['lat']
    lng=doc['geometry']['location']['lng']
    url="http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lng)+"2&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    temp = requests.get(url)
    #print(temp.text)
    temp_data=json.loads(temp.text)
    
    hotel_temp[str(doc['name'])]=temp_data['main']['temp']
    print(count,")",doc['name'],":", temp_data['main']['temp'])
    count=count+1
    
#Get hotel with highest TEMP
print(" ")
highest_temp=0
for i in hotel_temp:
    if hotel_temp[str(i)]>highest_temp:
        highest_temp=hotel_temp[str(i)]
        highest_hotel=i

print("Hotel with HIGHEST TEMPERATURE is", highest_hotel,"at", highest_temp, "degrees")
    
#Get hotel with highest TEMP
print(" ")
coolest_temp=100
for i in hotel_temp:
    if hotel_temp[str(i)]<coolest_temp:
        coolest_temp=hotel_temp[str(i)]
        coolest_hotel=i
        
print("Hotel with COOLEST TEMPERATURE is", coolest_hotel,"at", coolest_temp, "degrees")
    