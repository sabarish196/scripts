import requests
import json
import os

# Set the environment variables for your SPN credentials and subscription ID
TENANT_ID = os.environ.get('AZURE_TENANT_ID')
CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
SUBSCRIPTION_ID = os.environ.get('AZURE_SUBSCRIPTION_ID')

# Set the URL and headers for the API request
url = f"https://management.azure.com/subscriptions/{SUBSCRIPTION_ID}/providers/Microsoft.Advisor/recommendations?api-version=2017-04-19"
headers = {'Authorization': f'Bearer {access_token}',
           'Content-Type': 'application/json'}

# Disable SSL verification
requests.packages.urllib3.disable_warnings()

# Get the access token using the SPN credentials
data = {'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'resource': 'https://management.azure.com/'}
response = requests.post(f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token", data=data, verify=False)
access_token = json.loads(response.content.decode('utf-8'))['access_token']

# Get the recommendations and extract the extendedProperties and resource metadata fields
recommendations = []
response = requests.get(url, headers=headers, verify=False)
if response.status_code == 200:
    result = json.loads(response.content.decode('utf-8'))
    recommendations = result['value']
    while 'nextLink' in result:
        response = requests.get(result['nextLink'], headers=headers, verify=False)
        result = json.loads(response.content.decode('utf-8'))
        recommendations.extend(result['value'])

# Save the recommendations to a single file in JSON format
with open('azure_recommendations.json', 'w') as f:
    json.dump(recommendations, f, indent=4)
