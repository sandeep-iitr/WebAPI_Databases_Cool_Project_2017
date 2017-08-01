import json
data = '{"Name" : "Samritha", "City" : "Mountain View", "Age" : 17, "id" : 20}'
j = json.loads(data)
print(j['Name'], j['Age'])