import requests
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.771068,-73.975207&radius=10000&type=hotels&keyword=stay&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
response = requests.get(url)
print (response.text)

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
    print ("# of hotels:", len(doc))

cursor = collection.find()
for doc in cursor:
    #if 'geometry' in doc:
    if 'rating' in doc:
        print("Name:", doc['name'])
        print("Rating:", doc['rating'])
        url = "http://api.openweathermap.org/data/2.5/weather?lat="+str(doc['geometry']['location']['lat'])+"&lon="+str(doc['geometry']['location']['lng'])+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
        response = requests.get(url)
        rawdata = response.text
        rawjson = json.loads(rawdata)
        data = rawjson['main']
        print (data)
        
rate = collection.find().sort("rating",pymongo.DESCENDING).limit(1)
for x in rate:
    print ("Highest rating hotel:" , x["name"])

cursor = collection.find().sort([("temp_max",-1)]).limit(1)
for doc in cursor:
    print ("Hottest temp:", doc["name"])

cursor = collection.find().sort([("temp_max",1)]).limit(1)   
for doc in cursor:
    print ("Coolest temp:", doc["name"])
    


        