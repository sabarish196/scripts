import requests
import json
import os

# Set Azure authentication credentials
TENANT_ID = os.environ['AZURE_TENANT_ID']
CLIENT_ID = os.environ['AZURE_CLIENT_ID']
CLIENT_SECRET = os.environ['AZURE_CLIENT_SECRET']

# Set Azure API endpoint URLs
SUBSCRIPTIONS_URL = 'https://management.azure.com/subscriptions?api-version=2022-01-01'
ADVISOR_RECOMMENDATIONS_URL = 'https://management.azure.com/subscriptions/{}/providers/Microsoft.Advisor/recommendations?api-version=2022-01-01'

# Disable SSL verification (not recommended for production)
requests.packages.urllib3.disable_warnings()

# Retrieve Azure access token using SPN credentials
auth_url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/token'
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'resource': 'https://management.azure.com/'
}
auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
response = requests.post(auth_url, data=auth_data, headers=auth_headers, verify=False)
access_token = response.json()['access_token']

# Retrieve Azure subscription IDs
subscriptions_headers = {'Authorization': f'Bearer {access_token}'}
subscriptions_response = requests.get(SUBSCRIPTIONS_URL, headers=subscriptions_headers, verify=False)
subscriptions = subscriptions_response.json()['value']

# Retrieve Azure Advisor recommendations for each subscription
advisor_recommendations = []
for subscription in subscriptions:
    subscription_id = subscription['subscriptionId']
    advisor_recommendations_headers = {'Authorization': f'Bearer {access_token}'}
    advisor_recommendations_url = ADVISOR_RECOMMENDATIONS_URL.format(subscription_id)
    advisor_recommendations_response = requests.get(advisor_recommendations_url, headers=advisor_recommendations_headers, verify=False)
    recommendations = advisor_recommendations_response.json()['value']
    for recommendation in recommendations:
        extended_properties = recommendation.get('extendedProperties', {})
        metadata = recommendation.get('metadata', {})
        advisor_recommendations.append({'subscriptionId': subscription_id, 'extendedProperties': extended_properties, 'metadata': metadata})

# Save Azure Advisor recommendations to a single file in JSON format
with open('azure_recommendations.json', 'w') as file:
    json.dump(advisor_recommendations, file)
