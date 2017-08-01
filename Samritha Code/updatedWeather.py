import requests

url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.750580,-73.993584&radius=10000&type=hotels&keyword=hotel&key=AIzaSyBErt-5ajtNyZARRB2CeOlU3xGgNu0QLSQ"
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
collection = db.test_collection1
collection.delete_many({})
data_id = collection.insert_many(data)

tempColl = db.test_collection2
tempColl.delete_many({})

#Creating Index and Query 
cursor=collection.find().sort([("rating",-1)])

for doc in cursor: 
	geometry = doc['geometry']
	location = geometry['location']
	try:
		doc['rating']
	except:
		doc['rating'] = 0
	lat=location['lat']
	lon=location['lng']
	urlW = "http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lon)+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
	responseW = requests.get(urlW)
	rawdata=responseW.text
	rawjson=json.loads(rawdata) 
	data=rawjson['main']['temp']
	#Create New Collection
	tempData = '{"Name" :"'+ doc["name"]+'", "rating" :' + str(doc["rating"]) + ', "Temp" :' + str(data)+ '}'
	j = json.loads(tempData)
	data_id = tempColl.insert_one(j).inserted_id

csr=tempColl.find().sort([("rating",-1)])
hotel=csr[0]
print('Best Rating: '+ hotel['Name'])
print ("# of Hotels: " + str(tempColl.count()))

csr=tempColl.find().sort([("Temp",-1)])
maxTemp = csr[0]['Temp']

csr=tempColl.find().sort([("Temp",+1)])
minTemp = csr[0]['Temp']

for hotel in csr:
	if hotel["Temp"] == maxTemp:
		print("High Temperature: " + str(hotel["Temp"]) + ", " + hotel["Name"])
	if hotel["Temp"] == minTemp: 
		print("Low Temperature: " + str(hotel["Temp"]) + ", " + hotel["Name"])

