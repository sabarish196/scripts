import os
import git

# Define the Git repository path
repo_path = "/path/to/your/repo"

# Define the README file name and keyword to search for
readme_file = "README.md"
keyword = "example"

# Change the working directory to the repository path
os.chdir(repo_path)

# Use the git module to get a list of subdirectories in the repository
repo = git.Repo(repo_path)
subdirs = [x[0] for x in os.walk(repo_path) if x[0] != repo_path]

# Loop through the subdirectories and read the contents of the README file
for subdir in subdirs:
    # Get the path to the README file in the current subdirectory
    readme_path = os.path.join(subdir, readme_file)
    
    # Check if the README file exists in the current subdirectory
    if os.path.exists(readme_path):
        # Read the contents of the README file
        with open(readme_path, "r") as f:
            readme_contents = f.read()
        
        # Check if the keyword is in the README file contents
        if keyword in readme_contents:
            print("The keyword '{}' was found in the README file in {}".format(keyword, subdir))
