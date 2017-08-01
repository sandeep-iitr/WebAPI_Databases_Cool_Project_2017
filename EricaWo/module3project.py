import requests
url= "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.6512004,-74.1513888&radius=10000&type=hotels&keyword=stay&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
response = requests.get(url)
print(response.text)

import json
rawdata = response.text
rawjson = json.loads(rawdata)
data = rawjson['results']

import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.test_database
collection = db.test_collection
collection.delete_many({})
data_id = collection.insert_many(data)

cursor = collection.find()
for doc in cursor:
    print (doc)
    print ("Count of total hotels:", len(doc))

cursor = collection.find()
for doc in cursor:
    if 'rating' in doc:
     url= "http://api.openweathermap.org/data/2.5/weather?lat="+str(doc['geometry']['location']['lat'])+"&lon="+str(doc['geometry']['location']['lng'])+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
     response = requests.get(url)
     rawdata = response.text
     rawjson = json.loads(rawdata)
     data = rawjson['main']
     print(data)

cursor=collection.find().sort([("rating",-1)]).limit(1)
for rating in cursor:
    print(rating)

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

cursor=collection.find().sort([("temp_max",-1)]).limit(1)
for doc in cursor:
    print ("The hottest hotel is", doc["name"])
    
cursor=collection.find().sort([("temp_min",+1)]).limit(1)
for doc in cursor:
    print ("The coolest hotel is", doc["name"])
    
def order(item):
    return item[0]

"""
cursor = collection.find().sort([("main",-1)])
hot=collection.find().sort("main",pymongo.ASCENDING).limit(1)
for x in cursor:
    print ("The hottest hotel is", x["name"])

cursor = collection.find().sort([("main", 1)])
cool=collection.find().sort("main",pymongo.DESCENDING).limit(1)
for x in cursor:
    print ("The coolest hotel is", x["name"])
    
    
print (sorted(temp,key=order))
print ("The hottest hotel is" , temp[0][0])
print ("The coolest hotel is" , temp[-1][0])

collection.ensure_index([('rating',pymongo.ASCENDING)] )
collection.ensure_index([('rating',pymongo.DESCENDING)] )
"""
