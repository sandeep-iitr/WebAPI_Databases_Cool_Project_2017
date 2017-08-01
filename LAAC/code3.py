cursor = collection2.find()
for doc in cursor:
	print(doc['geometry'])

	collection2.ensure_index([('rating', pymongo.ASCENDING)])

collection2.ensure_index([('rating',pymongo.DESCENDING)])

for doc in cursor:
	print(doc['name'])