import requests
import json
import pyodbc

def get_access_token():
    # Define the Azure AD tenant ID and the client ID and secret for the app that has permission to access the Advisor API
    tenant_id = 'your_tenant_id'
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'

    # Build the URL for the token endpoint
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/token'

    # Define the request parameters for the token endpoint
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'resource': 'https://management.azure.com/'
    }

    # Send a POST request to the token endpoint to get an access token
    response = requests.post(url, data=data)

    # Parse the JSON response and return the access token
    access_token = json.loads(response.content)['access_token']
    return access_token

def get_advisor_recommendations(subscription_id, access_token):
    # Build the URL for the Advisor API to get recommendations for the subscription
    url = f'https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Advisor/recommendations?api-version=2017-04-19'

    # Define the request headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Send a GET request to the Advisor API to get recommendations for the subscription
    response = requests.get(url, headers=headers)

    # Parse the JSON response and return the recommendations
    recommendations = json.loads(response.content)['value']
    return recommendations

def upload_recommendations_to_sql_server(server, database, username, password, recommendations):
    # Establish a connection to the SQL Server
    conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    try:
        # Build the SQL INSERT statement for each recommendation
        for recommendation in recommendations:
            insert_query = f"INSERT INTO AdvisorRecommendations (SubscriptionId, ResourceId, RecommendationId, Category, Impact, Risk, Problem, Solution) VALUES ('{recommendation['subscriptionId']}', '{recommendation['properties']['resourceId']}', '{recommendation['id']}', '{recommendation['properties']['category']}', '{recommendation['properties']['impact']}', '{recommendation['properties']['risk']}', '{recommendation['properties']['problem']}', '{recommendation['properties']['solution']}')"

            # Execute the INSERT statement
            cursor.execute(insert_query)

        # Commit the transaction after all inserts are done
        conn.commit()
    except:
        # Rollback the transaction if there is an error
        conn.rollback()
        raise
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()

# Get an access token to authenticate with the Advisor API
access_token = get_access_token()

# Get a list of all subscriptions
url = 'https://management.azure.com/subscriptions?api-version=2021-04-01'
headers = {
    'Authorization': f'Bearer {access_token}'
}
response = requests.get(url, headers=headers)
subscriptions = json.loads(response.content)['value']

# Iterate through each subscription and get Advisor recommendations
for subscription in subscriptions:
    recommendations = get_advisor_recommendations
