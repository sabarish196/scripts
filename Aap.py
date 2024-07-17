import requests
import json

# Configuration
TOWER_URL = 'https://your-ansible-tower-url.com'
USERNAME = 'your_username'
PASSWORD = 'your_password'
DEV_PROJECT_NAME = 'dns-dev'
PROD_PROJECT_NAME = 'dns-prod'

# Headers for authentication
HEADERS = {
    'Content-Type': 'application/json'
}

# Disable SSL warnings (not recommended for production)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Get project ID
def get_project_id(project_name):
    response = requests.get(f'{TOWER_URL}/api/v2/projects/', headers=HEADERS, auth=(USERNAME, PASSWORD), verify=False)
    projects = response.json()['results']
    for project in projects:
        if project['name'] == project_name:
            return project['id']
    return None

# Get job templates for a project
def get_job_templates(project_id):
    response = requests.get(f'{TOWER_URL}/api/v2/job_templates/?project={project_id}', headers=HEADERS, auth=(USERNAME, PASSWORD), verify=False)
    return response.json()['results']

# Create job template in prod
def create_job_template(job_template, prod_project_id):
    # Copy the job template and modify the required fields
    new_job_template = job_template.copy()
    new_job_template['name'] = job_template['name'].replace('dev', 'prod')
    new_job_template['project'] = prod_project_id
    
    # Remove fields that should not be copied directly
    fields_to_remove = ['id', 'related', 'summary_fields', 'created', 'modified', 'last_job_run', 'last_job_failed', 'next_job_run', 'status', 'type', 'url']
    for field in fields_to_remove:
        new_job_template.pop(field, None)
    
    response = requests.post(f'{TOWER_URL}/api/v2/job_templates/', headers=HEADERS, auth=(USERNAME, PASSWORD), data=json.dumps(new_job_template), verify=False)
    return response.json()

# Main script
def main():
    dev_project_id = get_project_id(DEV_PROJECT_NAME)
    prod_project_id = get_project_id(PROD_PROJECT_NAME)
    
    if not dev_project_id or not prod_project_id:
        print("Invalid project names provided.")
        return

    job_templates = get_job_templates(dev_project_id)

    for jt in job_templates:
        result = create_job_template(jt, prod_project_id)
        print(f"Created job template: {result.get('name', 'Error creating job template')}")

if __name__ == '__main__':
    main()
