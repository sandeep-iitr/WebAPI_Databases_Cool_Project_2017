#get data
import requests
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7498605,-73.9736444&radius=10000&type=hotels&keyword=hotel&key=%20AIzaSyBErt-5ajtNyZARRB2CeOlU3xGgNu0QLSQ"
response = requests.get(url)
#print(response.text)

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
collection = db.test_collection2
collection.delete_many({})
data_id = collection.insert_many(data)

#Print All data
cursor=collection.find()
#for doc in cursor:
    #print(doc)
    #print(doc['name'])
    #print(doc['geometry']['location'])

#Print only location from data
#cursor=collection.find()
#for doc in cursor:
    #print(doc['geometry'])

#Creating Index and Query
#collection.ensure_index([('rating',pymongo.ASCENDING)] )
collection.ensure_index([('rating',pymongo.DESCENDING)] )
cursor=collection.find().sort([("rating",-1)])

print("********************************************************************") 
#Prints out a list of hotels from descending order in a 10km radius around the UN Headquarters 
print("List of hotels:")
numcount = 0
for doc in cursor:
    print(doc['name'])
    numcount += 1
print("*******************************************************************")
print("Number of available hotels:",numcount)
    
#Prints out the best hotel 
cursor=collection.find().sort([("rating",-1)]).limit(1)
for doc in cursor:
    print("Best ranked hotel is:", doc['name'])

print("*******************************************************************") 
#Print out best weather and temperature for each hotel
cursor = collection.find()
print("List of temperatures for each hotel:") 

templist = [] 
d = {}

collection2 = db.test_collection3  
for doc in cursor:
    lat = doc['geometry']['location']['lat']
    lng = doc['geometry']['location']['lng']
    weatherurl = "http://api.openweathermap.org/data/2.5/weather?lat="+str(lat)+"&lon="+str(lng)+"&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    response = requests.get(weatherurl) 
    newresponse = response.text
    rwjson = json.loads(newresponse)
    temp = rwjson['main']['temp']
    #prints out name of hotel and its average temperature
    print(temp, doc['name'])
    templist.append(temp)
    templist.sort()
    d[doc['name']] = temp
#print(templist)
#print(d) 
import operator
sorted_d = sorted(d.items(),key=operator.itemgetter(1))
#print(sorted_d)

print("*******************************************************************")   
#prints out the hotel with the lowest temperature
min_temp = sorted_d[0]
print("Hotel with the lowest temperature:",min_temp[0],"@",min_temp[1],"°F")
#prints out the hotel with the highest temperature
max_temp = sorted_d[-1]
print("Hotel with the highest temperature:",max_temp[0],"@",max_temp[1],"°F") 




