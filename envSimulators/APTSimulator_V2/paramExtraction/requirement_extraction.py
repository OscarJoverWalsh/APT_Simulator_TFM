import csv
import re
import importlib

def is_library(word):
    try:
        importlib.import_module(word)
        return True
    except ImportError:
        return False

def extract_requirements(commands):
    requirements = set()
    for command in commands:
        matches = re.findall(r'\b([a-zA-Z0-9_-]+)\b', command)
        for match in matches:
            if is_library(match):
                requirements.add(match)
    return requirements

# Read commands from commands.txt file
filename = 'commands.txt'
commands = []
with open(filename, 'r') as f:
    commands = f.readlines()

# Extract requirements from commands
requirements = extract_requirements(commands)

# Create requirements.txt file
requirements_filename = 'requirements.txt'
with open(requirements_filename, 'w') as f:
    for requirement in requirements:
        f.write(requirement + '\n')

print("Requirements extracted and saved to requirements.txt.")
