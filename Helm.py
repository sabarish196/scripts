import yaml
import git

# Function to modify the YAML file
def modify_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

        # Look for *-values.yaml
        for key, value in data.items():
            if key.endswith('-values.yaml'):
                # Comment the line envFromConfigMaps:
                if 'envFromConfigMaps' in value:
                    value['envFromConfigMaps'] = '# ' + value['envFromConfigMaps']

                # Add a new line with enabelenvFromSecrets:
                value['enabelenvFromSecrets'] = 'new line here'

                # Look for requests.cpu and change its value to 50m
                if 'requests' in value and 'cpu' in value['requests']:
                    value['requests']['cpu'] = '50m'

    # Write the modified data back to the file
    with open(file_path, 'w') as file:
        yaml.dump(data, file)

# Create a new branch named helmupdate
repo = git.Repo('.')
new_branch = repo.create_head('helmupdate')
repo.head.reference = new_branch
repo.head.reset(index=True, working_tree=True)

# Modify the YAML files in the repository
yaml_files = ['file1-values.yaml', 'file2-values.yaml']  # Add all relevant file names here
for file in yaml_files:
    modify_yaml(file)

# Commit changes
repo.index.add(yaml_files)
repo.index.commit("Modified YAML files as per requirements")

# Push changes to remote
origin = repo.remote('origin')
origin.push(new_branch)
