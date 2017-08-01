import math

#get data
import requests
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7128, -74.0059&radius=10000&type=hotels&keyword=hotel&key=AIzaSyBErt-5ajtNyZARRB2CeOlU3xGgNu0QLSQ"
response = requests.get(url)

#parse json
import json
rawdata=response.text
rawjson=json.loads(rawdata)
data=rawjson['results']

#insert into MongoDB
import pymongo
from pymongo import MongoClient
client = MongoClient()
db = client.test_database
collection.delete_many({})

collection = db.test_collection
data_id = collection.insert_many(data)



#   PART A 
total = 0
total = collection.count()
print("Amount of hotels:", total)



#   PART B
collection.ensure_index([('rating',pymongo.DESCENDING)])
cursor=collection.find().sort([("rating",-1)]).limit(1)

for doc in cursor: 
    print("Best Rated Hotel:", doc['name'])


myCollection.delete_many({})
myCollection = db.test_collection2


cursor = collection.find()
for doc in cursor:
    myLat = doc['geometry']['location']['lat']
    myLon = doc['geometry']['location']['lng']
    url="http://api.openweathermap.org/data/2.5/weather?lat="+str(myLat)+"&lon="+str(myLon)+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    response = requests.get(url)
    
    rawdata=response.text
    rawjson=json.loads(rawdata)
    data=rawjson['main']
    
    try:
        data = {"Name" : doc['name'], "Lat" : myLat, "Lon" : myLon, "Rating" : doc['rating'], "Temp" : data['temp']}

    except:
        data = {"Name" : doc['name'], "Lat" : myLat, "Lon" : myLon, "Rating" : 0, "Temp" : data['temp']}
        

    data_id = myCollection.insert_one(data)

cursor = myCollection.find()



#    PART C
myCollection.ensure_index([('Temp',pymongo.DESCENDING)])
cursor=myCollection.find().sort([("Temp",-1)])

high = -math.inf
name = []
for doc in cursor: 
    if(doc['Temp'] >= high):
        name.append(doc['Name'])
        high = doc['Temp']
    
    else:
        break

print("Highest Temperature:", high, name)





cursor = myCollection.find()

#    PART D
myCollection.ensure_index([('Temp',pymongo.ASCENDING)])
cursor=myCollection.find().sort([("Temp",-1)])

low = math.inf
name = []
for doc in cursor: 
    if(doc['Temp'] <= low):
        name.append(doc['Name'])
        low = doc['Temp']
    
    else:
        break

print("Lowest Temperature:", low, name)


