import requests
import json

# Set the variables for your Service Principal credentials
tenant_id = "<your-tenant-id>"
client_id = "<your-client-id>"
client_secret = "<your-client-secret>"

# Disable SSL verification for all requests
requests.packages.urllib3.disable_warnings()

# Set the headers for the API call
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

# Set the data for the API call
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "resource": "https://management.azure.com/"
}

# Make a POST request to the Azure OAuth2 token endpoint to get an access token
response = requests.post(f"https://login.microsoftonline.com/{tenant_id}/oauth2/token", headers=headers, data=data, verify=False)

# Check if the request was successful and get the access token
if response.status_code == 200:
    access_token = json.loads(response.content)["access_token"]
else:
    print("Error getting access token")

# Set the headers for the API call
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Get the list of subscriptions
response = requests.get("https://management.azure.com/subscriptions?api-version=2019-06-01", headers=headers, verify=False)

# Check if the request was successful and get the list of subscriptions
if response.status_code == 200:
    subscriptions = json.loads(response.content)["value"]
else:
    print("Error getting subscriptions")

# Get the Azure recommendations for each subscription
recommendations = []
for subscription in subscriptions:
    subscription_id = subscription["subscriptionId"]
    response = requests.get(f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Advisor/recommendations?api-version=2017-04-19", headers=headers, verify=False)

    if response.status_code == 200:
        subscription_recommendations = json.loads(response.content)["value"]
        recommendations.extend(subscription_recommendations)

# Print the list of recommendations as JSON
print(json.dumps(recommendations))
