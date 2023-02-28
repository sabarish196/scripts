import requests
import json
import os

# Set environment variables for SPN credentials
tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]

# Set the API endpoint
api_endpoint = "https://management.azure.com/subscriptions?api-version=2020-01-01"

# Disable SSL verification
verify_ssl = False

# Set the output file path
output_file_path = "output.json"

# Create an empty list to store recommendations
all_recommendations = []

# Set the headers
headers = {
    "Content-Type": "application/json",
}

# Authenticate using SPN credentials
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "resource": "https://management.azure.com/",
}

response = requests.post(
    "https://login.microsoftonline.com/{}/oauth2/token".format(tenant_id),
    data=data,
    headers=headers,
    verify=verify_ssl,
)

access_token = response.json()["access_token"]
headers["Authorization"] = "Bearer " + access_token

# Loop through each subscription to get recommendations
while api_endpoint:
    # Get the subscriptions and convert response to JSON
    response = requests.get(api_endpoint, headers=headers, verify=verify_ssl)
    subscriptions = response.json()

    # Loop through each subscription and get recommendations
    for subscription in subscriptions["value"]:
        # Set the API endpoint for recommendations
        recommendations_api_endpoint = (
            f"https://management.azure.com/subscriptions/{subscription['subscriptionId']}/providers/Microsoft.Advisor/recommendations?api-version=2017-04-19"
        )

        # Loop through each page of recommendations
        next_link = recommendations_api_endpoint
        while next_link:
            # Get the recommendations and convert response to JSON
            response = requests.get(next_link, headers=headers, verify=verify_ssl)
            recommendations = response.json()

            # Loop through each recommendation and get the extendedProperties and resourceMetadata fields
            for recommendation in recommendations["value"]:
                recommendation_properties = recommendation["properties"]
                extended_properties = recommendation_properties.get("extendedProperties", {})
                resource_metadata = recommendation_properties.get("resourceMetadata", {})
                recommendation_dict = {
                    "subscriptionId": subscription["subscriptionId"],
                    "extendedProperties": extended_properties,
                    "resourceMetadata": resource_metadata,
                }
                all_recommendations.append(recommendation_dict)

            # Check if there is a next page of recommendations
            next_link = recommendations.get("nextLink")

    # Check if there are more subscriptions
    api_endpoint = subscriptions.get("nextLink")

# Write all recommendations to output file
with open(output_file_path, "w") as f:
    json.dump(all_recommendations, f)
