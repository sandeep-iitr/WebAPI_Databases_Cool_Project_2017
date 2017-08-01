#get data
import requests
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=34.0635363,-118.4455592&radius=2000&type=hotels&keyword=stay&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
response = requests.get(url)
print(response.text)

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
collection = db.test_collection
data_id = collection.insert_many(data).insert

#Print All data
cursor=collection.find()
for doc in cursor: 
    print(doc)