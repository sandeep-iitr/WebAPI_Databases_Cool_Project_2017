import pymongo
from pymongo import MongoClient
import json

client = MongoClient()
db = client.test_database
collection = db.test_collection

collection.delete_many({})
data = '{"Name" : "Sandeep", "City" : "Los Angeles"}'
j = json.loads(data)
data_id = collection.insert_one(j).inserted_id
collection.find_one()

cursor = collection.find()


print(doc)