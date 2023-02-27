import requests
import json
import os

# Set the SPN credentials
tenant_id = '<your tenant ID>'
client_id = '<your client ID>'
client_secret = '<your client secret>'

# Set the Azure endpoint for recommendations API
endpoint = 'https://management.azure.com/providers/Microsoft.Advisor/recommendations?api-version=2021-01-01'

# Disable SSL verification
verify_ssl = False

# Initialize headers with content type and authorization token
headers = {'Content-Type': 'application/json'}
auth_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': 'https://management.azure.com/'
}
auth_response = requests.post(auth_url, data=auth_data).json()
access_token = auth_response['access_token']
headers['Authorization'] = 'Bearer ' + access_token

# Initialize an empty list to store recommendations
recommendations = []

# Send a GET request to the Azure endpoint to retrieve recommendations
while endpoint:
    response = requests.get(endpoint, headers=headers, verify=verify_ssl)
    response_json = response.json()
    if response_json.get('value'):
        recommendations.extend(response_json['value'])
    endpoint = response_json.get('nextLink')

# Filter the recommendations to include only the desired fields
filtered_recommendations = []
for recommendation in recommendations:
    filtered_recommendation = {
        'id': recommendation['id'],
        'type': recommendation['type'],
        'name': recommendation['name'],
        'extendedProperties': recommendation['properties']['extendedProperties'],
        'resourceMetadata': recommendation['properties']['metadata']['resourceMetadata']
    }
    filtered_recommendations.append(filtered_recommendation)

# Write the recommendations to a file in JSON format
output_file = 'recommendations.json'
with open(output_file, 'w') as f:
    json.dump(filtered_recommendations, f, indent=4)
