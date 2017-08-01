#Something that works for web service/database module
import json
import sys
import os
import requests
import pymongo
from pymongo import MongoClient

fw=open('results.txt','w')

places_appid="AIzaSyD8wnikJHxQUBzztfsD8RvkV_wJAgi1-d8"
weather_appid="f3ed13c42e7c876a64fd7841e7da9838"
lat=40.717028
lng=-73.992579

client=MongoClient()
places=client.database
hotels=places.collection
hotels.delete_many({})
search=requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(lat)+","+str(lng)+"&radius=100000&type=hotels&key="+places_appid)
results=json.loads(search.text)
found_hotels=results['results']
for place in found_hotels:
#insert_result=hotels.insert_many(found_hotels)

#cursor=hotels.find()#get the pointers to all hotels
#for place in cursor:
    lattitude=place['geometry']['location']['lat']
    longitude=place['geometry']['location']['lng']
    weather_url="http://api.openweathermap.org/data/2.5/weather?lat="+str(lattitude)+"&lon="+str(longitude)+"&units=Imperial&appid="+weather_appid
    weather_data=requests.get(weather_url)
    actual_weather=json.loads(weather_data.text)
    temperature=actual_weather['main']['temp']
    place['temperature']=temperature
    insert_result=hotels.insert_one(place)
#    hotels.update_one({'_id':place['_id']},{'$set':{'temperature':temperature}})
#    fw.write('Temperature at: '+place['name']+'is '+str(place['temperature'])+'\n')
    
fw.write('The number of hotels found is: '+str(hotels.count())+'\n')
high_rating_place=hotels.find().sort('rating',-1).limit(1)
high_temp=(hotels.find().sort('temperature',-1).limit(1))[0]['temperature']
low_temp=(hotels.find().sort('temperature',+1).limit(1))[0]['temperature']

fw.write('Highest rating place is: '+str(high_rating_place[0]['name'])+', and its rating is: '+str(high_rating_place[0]['rating'])+'\n')
high_temp_place=hotels.find({'temperature':high_temp})
for place in high_temp_place:
    fw.write('Highest temperature place is: '+str(place['name'])+', and temperature is: '+str(place['temperature'])+'\n')
low_temp_place=hotels.find({'temperature':low_temp})
for place in low_temp_place:
    fw.write('Lowest temperature place is: '+str(place['name'])+', and temperature is: '+str(place['temperature'])+'\n')
    
