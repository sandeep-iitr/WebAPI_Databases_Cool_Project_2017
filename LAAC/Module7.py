#get data
import requests
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7128, -74.0059&radius=10000&type=hotels&keyword=hotel&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
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



#   PART C
cursor = collection.find()

high = -10000
name = []
for doc in cursor:
    myLat = doc['geometry']['location']['lat']
    myLon = doc['geometry']['location']['lng']
    url="http://api.openweathermap.org/data/2.5/weather?lat="+str(myLat)+"&lon="+str(myLon)+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    response = requests.get(url)
    
    rawdata=response.text
    rawjson=json.loads(rawdata)
    data=rawjson['main']

    if(high < data['temp']):
        name = []
        high = data['temp']
        name.append(doc['name'])
    
    elif(high == data['temp']):
        name.append(doc['name'])
    

print("Highest Temp:", name, high)


#   PART D
cursor= collection.find()


low = 10000
name = []
for doc in cursor:
    myLat = doc['geometry']['location']['lat']
    myLon = doc['geometry']['location']['lng']
    url="http://api.openweathermap.org/data/2.5/weather?lat="+str(myLat)+"&lon="+str(myLon)+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    response = requests.get(url)
    
    rawdata=response.text
    rawjson=json.loads(rawdata)
    data=rawjson['main']

    if(low > data['temp']):
        name = []
        low = data['temp']
        name.append(doc['name'])
    
    elif(low == data['temp']):
        name.append(doc['name'])
    

print("Lowest Temp:", name, low)







