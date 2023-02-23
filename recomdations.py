# Import necessary libraries
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt advisor import AdvisorManagementClient
from azure.mgmt advisor.models import *

# Set the Azure Key Vault details
key_vault_name = "<your-key-vault-name>"
key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
key_vault_secret_name = "<your-secret-name>"
credential = DefaultAzureCredential()

# Get the SPN credentials from the Azure Key Vault
secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)
client_secret = secret_client.get_secret(key_vault_secret_name).value

# Authenticate with the Azure Subscription using the SPN credentials
subscription_client = SubscriptionClient(credential=DefaultAzureCredential(client_id="<your-client-id>", client_secret=client_secret, tenant_id="<your-tenant-id>"))

# Get the list of subscriptions associated with the SPN credentials
subscription_list = subscription_client.subscriptions.list()

# Iterate through the subscription list and get Azure recommendations for each subscription
for subscription in subscription_list:
    print(f"Subscription ID: {subscription.subscription_id}")
    
    # Authenticate with the Advisor Management API using the SPN credentials
    advisor_client = AdvisorManagementClient(credential=DefaultAzureCredential(client_id="<your-client-id>", client_secret=client_secret, tenant_id="<your-tenant-id>"), subscription_id=subscription.subscription_id)

    # Get the list of Azure recommendations for the subscription
    recommendations = advisor_client.recommendations.list()
    
    # Iterate through the recommendations and print the details
    for recommendation in recommendations:
        print(f"Recommendation ID: {recommendation.id}")
        print(f"Recommendation Name: {recommendation.name}")
        print(f"Recommendation Impact: {recommendation.impact}")
        print(f"Recommendation Category: {recommendation.category}")
