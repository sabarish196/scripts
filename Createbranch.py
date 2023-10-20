import requests

# Replace these variables with your GitHub organization, repository, and personal access token
org_name = 'your-organization'
repo_name = 'your-repo'
access_token = 'your-access-token'

# The tag name and the branch name to create the tag from
tag_name = 'v1.0.0'  # Replace with your desired tag name
branch_name = 'main'  # Replace with the branch you want to create the tag from

# Get the latest commit SHA of the branch
branch_url = f'https://api.github.com/repos/{org_name}/{repo_name}/branches/{branch_name}'
headers = {'Authorization': f'token {access_token}'}
response = requests.get(branch_url, headers=headers)

if response.status_code == 200:
    commit_sha = response.json()['commit']['sha']

    # Construct the URL to create the tag
    tag_url = f'https://api.github.com/repos/{org_name}/{repo_name}/git/tags'
    data = {
        'tag': tag_name,
        'object': commit_sha,
        'type': 'commit',
        'message': f'Creating tag {tag_name}'
    }

    # Make the API request to create the tag
    response = requests.post(tag_url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 201:
        print(f"Tag {tag_name} has been created from the {branch_name} branch in {org_name}/{repo_name}.")
    else:
        print(f"Failed to create the tag in {org_name}/{repo_name}.")
else:
    print(f"Failed to get the commit SHA for the {branch_name} branch in {org_name}/{repo_name}.")
