import os
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_access_token(client_id, client_secret, tenant_id):
    url = 'https://login.microsoftonline.com/{0}/oauth2/v2.0/token'.format(tenant_id)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://management.azure.com/.default'
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    access_token = response.json()['access_token']
    return access_token

def get_subscriptions(access_token):
    url = 'https://management.azure.com/subscriptions?api-version=2021-01-01'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, verify=False)
    subscriptions = response.json()['value']
    return subscriptions

def get_recommendations(access_token, subscription_id):
    url = 'https://management.azure.com/subscriptions/{0}/providers/Microsoft.Advisor/recommendations?api-version=2021-01-01'.format(subscription_id)
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    recommendations = []
    while url:
        response = requests.get(url, headers=headers, verify=False)
        data = response.json()
        recommendations += data['value']
        url = data.get('nextLink', None)
    return recommendations

def get_recommendation_details(access_token, subscription_id, resource_id):
    url = 'https://management.azure.com{0}?api-version=2021-01-01'.format(resource_id)
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    extended_properties = data['properties']['extendedProperties']
    resource_metadata = data['properties']['metadata']
    return {'extended_properties': extended_properties, 'resource_metadata': resource_metadata}

def get_all_recommendations(access_token, subscriptions):
    all_recommendations = []
    for subscription in subscriptions:
        subscription_id = subscription['subscriptionId']
        recommendations = get_recommendations(access_token, subscription_id)
        for recommendation in recommendations:
            resource_id = recommendation['id']
            recommendation_details = get_recommendation_details(access_token, subscription_id, resource_id)
            recommendation.update(recommendation_details)
        all_recommendations += recommendations
    return all_recommendations

def main():
    client_id = os.environ['AZURE_CLIENT_ID']
    client_secret = os.environ['AZURE_CLIENT_SECRET']
    tenant_id = os.environ['AZURE_TENANT_ID']
    access_token = get_access_token(client_id, client_secret, tenant_id)
    subscriptions = get_subscriptions(access_token)
    recommendations = get_all_recommendations(access_token, subscriptions)
    with open('azure_recommendations.json', 'w') as f:
        json.dump(recommendations, f, indent=4)

if __name__ == '__main__':
    main()
