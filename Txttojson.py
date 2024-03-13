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




import json

# Read the file and remove lines containing "No such file or directory"
with open('your_file.txt', 'r') as file:
    lines = [line.strip() for line in file if "No such file or directory" not in line]

# Create a dictionary to store server data
servers = {}

# Parse each line and consolidate into a nested dictionary
for line in lines:
    server, group_members = line.split(':', 1)
    server = server.strip()
    group, members_str = group_members.split(':', 1)
    group = group.strip()
    members = members_str.split(',')
    members = [member.strip() for member in members]
    if server in servers:
        if group in servers[server]:
            servers[server][group].extend(members)
        else:
            servers[server][group] = members
    else:
        servers[server] = {group: members}

# Convert the dictionary to JSON
json_data = json.dumps(servers, indent=4)

# Write the JSON data to a file
with open('output.json', 'w') as json_file:
    json_file.write(json_data)
