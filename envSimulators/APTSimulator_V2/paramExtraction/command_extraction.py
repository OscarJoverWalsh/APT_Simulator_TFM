import csv
import json

with open("abilities.json") as f:
    data = json.load(f)

commands = []
param_req = []
desired_platform = 'linux'

for item in data:
    executors = item['executors']
    for executor in executors:
        platform = executor['platform']
        if platform == desired_platform:
            command = executor['command']
            if command is not None:
                commands.append(command)

print(commands)

# Write commands to file
filename = 'commands.txt'

with open(filename, 'w') as f:
    for command in commands:
        f.write(command + '\n')

print("File '{}' created successfully.".format(filename))
