import requests
import json
from requests.structures import CaseInsensitiveDict

ability_url = 'http://localhost:8888/api/v2/abilities'

headers = CaseInsensitiveDict()
headers["KEY"] = "ADMIN123"
headers["accept"] = "application/json"

response = requests.get(ability_url, headers = headers)

ability_json = response.json()

with open('abilities.json', 'w') as f:
    json.dump(ability_json, f, ensure_ascii=False, indent=4) 

elements = len(ability_json)

i = 0

f = open("all_unlocks.txt", "w")
while i < elements:
    for executor in ability_json[i]['executors']:
        for parser in executor['parsers']:
            source = parser['parserconfigs'][0]['source']
            f.write(source + "\n")
            
    i += 1

f.close