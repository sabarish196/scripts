from azure.identity import DefaultAzureCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.advisor import AdvisorManagementClient
import requests

# Disable SSL verification
requests.packages.urllib3.disable_warnings()

# Set the variables for your Key Vault and Service Principal
keyvault_name = "<your-key-vault-name>"
spn_client_id = "<your-sp-client-id>"
spn_client_secret_name = "<your-sp-client-secret-name>"
spn_client_secret_version = "<your-sp-client-secret-version>"

# Create a DefaultAzureCredential object to access the Service Principal and client secret in Key Vault
credential = DefaultAzureCredential()

# Use the credential to authenticate and access the client secret stored in Key Vault
from azure.keyvault.secrets import SecretClient

secret_client = SecretClient(vault_url=f"https://{keyvault_name}.vault.azure.net", credential=credential)
spn_client_secret = secret_client.get_secret(spn_client_secret_name, spn_client_secret_version)

# Create a SubscriptionClient object with the Azure SDK and authenticated credential
subscription_client = SubscriptionClient(credential)

# Use the SubscriptionClient object to get a list of Azure subscriptions
subscriptions = subscription_client.subscriptions.list()

# Create an AdvisorManagementClient object with the Azure SDK and authenticated credential
advisor_client = AdvisorManagementClient(credential, base_url="https://management.azure.com")

# Loop through the subscriptions and get Advisor recommendations for each one
for subscription in subscriptions:
    print(f"Subscription Display Name: {subscription.display_name}")
    print(f"Subscription ID: {subscription.subscription_id}")
    print()

    # Use the AdvisorManagementClient object to get recommendations for the current subscription
    recommendations = advisor_client.recommendations.list_by_subscription(subscription_id=subscription.subscription_id)

    # Loop through the recommendations and print them
    for recommendation in recommendations:
        print(f"Recommendation ID: {recommendation.id}")
        print(f"Recommendation Name: {recommendation.name}")
        print(f"Recommendation Type: {recommendation.type}")
        print(f"Recommendation Severity: {recommendation.severity}")
        print(f"Recommendation Short Description: {recommendation.short_description}")
        print(f"Recommendation Long Description: {recommendation.long_description}")
        print()
