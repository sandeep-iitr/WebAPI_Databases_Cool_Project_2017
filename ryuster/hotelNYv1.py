#get data
import requests
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=40.7488811,-73.9748723&radius=100000&type=hotels&keyword=hotel&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
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
collection = db.test_collection5
collection.delete_many({})
data_id = collection.insert_many(data)
    

#Creating Index and Query
#collection.ensure_index([('rating',pymongo.ASCENDING)] )
collection.ensure_index([('rating',pymongo.DESCENDING)] )
cursor=collection.find().sort([("rating",-1)])
print('*******************************************************************************')
numhotel = 0
for doc in cursor:
    numhotel += 1
print('number of hotels in area',numhotel)
cursor=collection.find().sort([("rating",-1)]).limit(1)
for doc in cursor:
    print('best ranked hotel:', doc['name'])


#print best weather

cursor = collection.find()
maxtemp = 0
mintemp = 210
for doc in cursor:
    lat = doc['geometry']['location']['lat']
    lon = doc['geometry']['location']['lng']
    
    weatherurl="http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&units=Imperial&appid=f3ed13c42e7c876a64fd7841e7da9838"
    response = requests.get(weatherurl)
    
    rwdata = response.text
    rwjson = json.loads(rwdata)
    weatherdata = rwjson['main']

    tempH = weatherdata['temp']

    if tempH > maxtemp:
        maxtemp = tempH
        maxhotel = [doc['name']]
    if tempH == maxtemp:
        for a in maxhotel:
            if doc['name'] == a:        
                maxhotel.remove( doc['name'] )
        maxhotel.append( doc['name'] )
    if tempH < mintemp:
        mintemp = tempH
        minhotel = [doc['name']]
    if tempH == mintemp:
        for a in minhotel:
           if doc['name'] == a:
               minhotel.remove( doc['name'] )
        minhotel.append( doc['name'] )

print('**********************with highest temp',maxtemp,'*********************************')
for a in maxhotel:
    print(a)
print('**********************with lowest temp', mintemp,'*********************************')
for a in minhotel:
    print(a)

        







