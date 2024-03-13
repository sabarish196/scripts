import json

# Read the file and remove lines containing "No such file or directory"
with open('your_file.txt', 'r') as file:
    lines = [line.strip() for line in file if "No such file or directory" not in line]

# Create a dictionary to store server data
servers = {}

# Parse each line and convert to JSON format
for line in lines:
    server, groups = line.split(':')
    server = server.strip()
    groups = [group.strip() for group in groups.split(',')]
    servers[server] = groups

# Convert the dictionary to JSON
json_data = json.dumps(servers, indent=4)

# Write the JSON data to a file
with open('output.json', 'w') as json_file:
    json_file.write(json_data)
