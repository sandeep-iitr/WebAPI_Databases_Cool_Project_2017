#get data
import requests
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=34.0635363,-118.4455592&radius=2000&type=hotels&keyword=stay&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
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
for doc in cursor:
    print(doc)
    print(doc['geometry'])

#Print only location from data
#cursor=collection.find()
#for doc in cursor:
    #print(doc['geometry'])

#Creating Index and Query
collection.ensure_index([('rating',pymongo.ASCENDING)] )
collection.ensure_index([('rating',pymongo.DESCENDING)] )
cursor=collection.find().sort([("rating",-1)])
for doc in cursor:
    print(doc['name'])
