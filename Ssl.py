import ssl
import socket
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

# Define your Azure Key Vault URL and your SPN credentials
key_vault_url = "https://your-key-vault-name.vault.azure.net/"
client_id = "your-client-id"
client_secret = "your-client-secret"
tenant_id = "your-tenant-id"

# Define a function to retrieve SSL certificate from the server
def fetch_ssl_certificate(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert(binary_form=True)
    return cert

# Fetch SSL certificate from the server
ssl_cert = fetch_ssl_certificate("your-key-vault-name.vault.azure.net")

# Create a temporary SSL context with the retrieved certificate
temp_ssl_context = ssl.create_default_context()
temp_ssl_context.load_verify_locations(cadata=ssl_cert)

# Authenticate using SPN credentials
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Connect to Key Vault with SSL certificate
secret_client = SecretClient(vault_url=key_vault_url, credential=credential, transport=temp_ssl_context)

# Retrieve secret values
secret_name = "your-secret-name"
retrieved_secret = secret_client.get_secret(secret_name)

print("Retrieved secret value:", retrieved_secret.value)
