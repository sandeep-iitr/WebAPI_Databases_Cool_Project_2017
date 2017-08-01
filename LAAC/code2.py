import requests
url="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=34.0635363,-118.4455592&radius=2000&type=hotels&keyword=stay&key=%20AIzaSyCA7Ju4jwAoUxDu4GZbCZcwahHdz7OGQfc"
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
collection = db.test_collection2
data_id = collection.insert_many(data)
cursor = collection.find()
for doc in cursor:
	print(doc)


cursor = collection.find()
for doc in cursor:
	print(doc['geometry'])


collection.ensure_index([('rating',pymongo.DESCENDING)])

for doc in cursor:
	print(doc['name'])