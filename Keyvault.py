from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

# Define your Azure Key Vault URL and your SPN credentials
key_vault_url = "https://your-key-vault-name.vault.azure.net/"
client_id = "your-client-id"
client_secret = "your-client-secret"
tenant_id = "your-tenant-id"

# Authenticate using SPN credentials
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Connect to Key Vault
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

# Retrieve secret values
secret_name = "your-secret-name"
retrieved_secret = secret_client.get_secret(secret_name)

print("Retrieved secret value:", retrieved_secret.value)
