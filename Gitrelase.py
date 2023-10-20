import requests

# Replace with your GitHub organization and personal access token
org_name = 'your-organization'
access_token = 'your-access-token'

# Fetch all repositories in the organization
url = f'https://api.github.com/orgs/{org_name}/repos'
headers = {'Authorization': f'token {access_token}'}
response = requests.get(url, headers=headers)
repositories = response.json()

# Iterate through repositories and filter by name ending with '-tfc'
for repo in repositories:
    repo_name = repo['name']
    if repo_name.endswith('-tfc'):
        print(f'Repo with -tfc: {repo_name}')
        
    # Check if the repository has no releases
    releases_url = f'https://api.github.com/repos/{org_name}/{repo_name}/releases'
    response = requests.get(releases_url, headers=headers)
    releases = response.json()
    if not releases:
        print(f'Repo with no releases: {repo_name}')
