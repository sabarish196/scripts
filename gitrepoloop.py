from github import Github

# Replace with your GitHub access token
access_token = "YOUR_ACCESS_TOKEN_HERE"

# Replace with the name of your organization
org_name = "YOUR_ORGANIZATION_NAME_HERE"

# Replace with the file name containing the repository names (one per line)
repo_file = "REPO_NAMES_FILE.txt"

# Replace with the slugs of the teams to add as admins to the repositories
team_slugs = ["TEAM_SLUG_1", "TEAM_SLUG_2", "TEAM_SLUG_3"]

# Create a GitHub instance using the access token
g = Github(access_token)

# Get the organization
org = g.get_organization(org_name)

# Open the file containing the repository names
with open(repo_file, "r") as f:
    repo_names = f.read().splitlines()

# Loop over each repository name in the file
for repo_name in repo_names:
    # Create the repository
    repo = org.create_repo(repo_name, private=True, has_issues=True, has_wiki=True)

    # Get the teams to add as admins to the repository
    teams = [org.get_team_by_slug(slug) for slug in team_slugs]

    # Add the teams as admins to the repository
    for team in teams:
        repo.add_to_collaborators(team, "admin")

    # Print the repository
    print(repo)
