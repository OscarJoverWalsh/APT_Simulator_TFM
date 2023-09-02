import csv
import json

platform = 'windows'

# Load the JSON data
with open("abilities.json") as f:
    data = json.load(f)

# Filter and extract the desired elements
filtered_data = [
    {
        "description": ability["description"],
        "buckets": ability["buckets"],
        "additional_info": ability["additional_info"],
        "privilege": ability["privilege"],
        "technique_name": ability["technique_name"],
        "requirements": ability["requirements"],
        "singleton": ability["singleton"],
        "executors": [executor for executor in ability["executors"] if executor["platform"] == "linux"],
        "delete_payload": ability["delete_payload"],
        "access": ability["access"],
        "name": ability["name"],
        "tactic": ability["tactic"],
        "plugin": ability["plugin"],
        "ability_id": ability["ability_id"],
        "technique_id": ability["technique_id"],
        "repeatable": ability["repeatable"]
    }
    for ability in data
    if any(executor["platform"] == platform for executor in ability["executors"])
]

# Store the filtered data
with open("BBDD_" + platform + ".json", "w") as f:
    json.dump(filtered_data, f, indent=4)

with open("BBDD_" + platform + ".json") as f:
    data = json.load(f)

param_req = []

for item in data:
    ability_id = item['ability_id']
    name = item['name']
    tactic = item['tactic']
    technique_id = item['technique_id']
    
    platforms = []
    executors_sources = []
    executors = item['executors']
    for executor in executors:
        platform2 = executor['platform']
        platforms.append(platform2)
        parsers = executor['parsers']
        for parser in parsers:
            parser_configs = parser['parserconfigs']
            for parser_config in parser_configs:
                source = parser_config['source']
                executors_sources.append(source)
    
    requirements_sources = []
    requirements = item['requirements']
    for requirement in requirements:
        relationship_match = requirement['relationship_match']
        for match in relationship_match:
            source = match['source']
            requirements_sources.append(source)
    
    param_req.append({
        'ability_id': ability_id,
        'name': name,
        'tactic': tactic,
        'technique_id': technique_id,
        'platforms': platforms,
        'executors_sources': executors_sources,
        'requirements_sources': requirements_sources
    })

# Print param_req in the terminal
for item in param_req:
    print(item)

# Write param_req to CSV
keys = ['ability_id', 'name', 'tactic', 'technique_id', 'platforms', 'executors_sources', 'requirements_sources']
filename = 'param_req_' + platform.upper() + '.csv'
print(filename)
with open(filename, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(param_req)

print("CSV file '{}' created successfully.".format(filename))