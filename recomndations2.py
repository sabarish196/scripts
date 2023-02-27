from azure.identity import ClientSecretCredential
from azure.mgmt.subscription import SubscriptionClient

# Set the variables for your Service Principal credentials
tenant_id = "<your-tenant-id>"
client_id = "<your-client-id>"
client_secret = "<your-client-secret>"

# Create a ClientSecretCredential object with the Azure SDK and your Service Principal credentials
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Create a SubscriptionClient object with the Azure SDK and authenticated credential
subscription_client = SubscriptionClient(credential)

# Use the SubscriptionClient object to get a list of Azure subscriptions
subscriptions = subscription_client.subscriptions.list()

# Loop through the subscriptions and print their display names and subscription IDs
for subscription in subscriptions:
    print(f"Subscription Display Name: {subscription.display_name}")
    print(f"Subscription ID: {subscription.subscription_id}")
    print()
