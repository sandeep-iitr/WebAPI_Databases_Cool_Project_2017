import requests

url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.750580,-73.993584&radius=10000&type=hotels&keyword=hotel&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
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
collection = db.test_collection4
collection.delete_many({})
data_id = collection.insert_many(data)

#Creating Index and Query 
collection.ensure_index([('rating',pymongo.ASCENDING)] )
collection.ensure_index([('rating',pymongo.DESCENDING)] )
cursor=collection.find().sort([("rating",-1)])
hotel=cursor[0]
print('Best Rating: ' + hotel['name'])
temps=[]
print ("# of Hotels: " + str(collection.count()))
for doc in cursor: 
	geometry = doc['geometry']
	location = geometry['location']
	lat=location['lat']
	lon=location['lng']
	urlW = "http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lon)+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
	responseW = requests.get(urlW)
	rawdata=responseW.text
	rawjson=json.loads(rawdata)
	data=rawjson['main']['temp']
	temps.append(data)

hotels = collection.find().sort([("rating",-1)])
minimum = min(temps)
indices = [i for i, x in enumerate(temps) if x == minimum]
for hotel in indices:
	mt = hotels[hotel]
	print ("Low Temperature: " + mt['name'])
print(minimum)
maximum = max(temps)
print(maximum)
indices = [i for i, x in enumerate(temps) if x == maximum]
for hotel in indices:
	ht = hotels[hotel]
	print ("High Temperature: " + ht['name'])

	
	