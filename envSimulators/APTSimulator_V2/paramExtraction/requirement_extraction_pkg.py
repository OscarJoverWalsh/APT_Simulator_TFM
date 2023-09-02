import csv
import re
import pkg_resources

def is_package(word):
    return any(dist.key == word for dist in pkg_resources.working_set)

def extract_requirements(commands):
    requirements = set()
    for command in commands:
        matches = re.findall(r'\b([a-zA-Z0-9_-]+)\b', command)
        for match in matches:
            if is_package(match):
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
requirements_filename = 'requirements:pkg.txt'
with open(requirements_filename, 'w') as f:
    for requirement in requirements:
        f.write(requirement + '\n')

print("Requirements extracted and saved to requirements.txt.")
