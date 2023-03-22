from github import Github

# Replace with your GitHub access token
access_token = "YOUR_ACCESS_TOKEN_HERE"

# Replace with the name of your organization
org_name = "YOUR_ORGANIZATION_NAME_HERE"

# Replace with the name of your repository
repo_name = "YOUR_REPOSITORY_NAME_HERE"

# Create a GitHub instance using the access token
g = Github(access_token)

# Get the organization
org = g.get_organization(org_name)

# Create the repository
repo = org.create_repo(repo_name, private=True, has_issues=True, has_wiki=True)

# Get the three teams that you want to add as admins to the repository
team1 = org.get_team_by_slug("TEAM_SLUG_1")
team2 = org.get_team_by_slug("TEAM_SLUG_2")
team3 = org.get_team_by_slug("TEAM_SLUG_3")

# Add the teams as admins to the repository
repo.add_to_collaborators(team1, "admin")
repo.add_to_collaborators(team2, "admin")
repo.add_to_collaborators(team3, "admin")

# Print the repository
print(repo)
