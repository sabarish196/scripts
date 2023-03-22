import requests
import json

# Replace with your GitHub access token
access_token = "YOUR_ACCESS_TOKEN_HERE"

# Replace with the name of your organization
org_name = "YOUR_ORGANIZATION_NAME_HERE"

# Replace with the name of your repository
repo_name = "YOUR_REPOSITORY_NAME_HERE"

# Replace with the slugs of the teams to add as admins to the repository
team_slugs = ["TEAM_SLUG_1", "TEAM_SLUG_2", "TEAM_SLUG_3"]

# Set the API endpoint for creating repositories
url = f"https://api.github.com/orgs/{org_name}/repos"

# Set the headers for the API request
headers = {
    "Authorization": f"token {access_token}",
    "Accept": "application/vnd.github.v3+json"
}

# Set the data for the API request
data = {
    "name": repo_name,
    "private": True,
    "has_issues": True,
    "has_wiki": True
}

# Send the API request to create the repository
response = requests.post(url, headers=headers, data=json.dumps(data))

# Get the JSON response from the API request
repo_data = response.json()

# Get the URL of the repository
repo_url = repo_data["html_url"]

# Get the teams to add as admins to the repository
teams = []
for slug in team_slugs:
    url = f"https://api.github.com/orgs/{org_name}/teams/{slug}"
    response = requests.get(url, headers=headers)
    team_data = response.json()
    teams.append(team_data["id"])

# Loop over the teams and add them as admins to the repository
for team_id in teams:
    url = f"https://api.github.com/teams/{team_id}/repos/{org_name}/{repo_name}"
    response = requests.put(url, headers=headers, data=json.dumps({"permission": "admin"}))

# Print the repository URL
print(f"Repository created: {repo_url}")
