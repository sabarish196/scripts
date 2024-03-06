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



from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def authenticate_to_key_vault(vault_url):
    try:
        # Authenticate using DefaultAzureCredential
        credential = DefaultAzureCredential()

        # Create a SecretClient using the provided vault_url and credential
        client = SecretClient(vault_url=vault_url, credential=credential)

        return client

    except Exception as e:
        print("Authentication Error:", e)
        return None

def get_secret_from_key_vault(client, secret_name):
    try:
        # Retrieve the secret by its name
        secret = client.get_secret(secret_name)

        # Access the secret's value
        secret_value = secret.value

        return secret_value

    except Exception as e:
        print("Error:", e)
        return None

# Example usage:
vault_url = "https://<your-vault-name>.vault.azure.net/"
client = authenticate_to_key_vault(vault_url)

if client:
    secret_name_1 = "<your-secret-name-1>"
    secret_value_1 = get_secret_from_key_vault(client, secret_name_1)

    if secret_value_1:
        print("Retrieved secret 1:", secret_value_1)
    else:
        print("Failed to retrieve secret 1.")

    # Fetch another secret
    secret_name_2 = "<your-secret-name-2>"
    secret_value_2 = get_secret_from_key_vault(client, secret_name_2)

    if secret_value_2:
        print("Retrieved secret 2:", secret_value_2)
    else:
        print("Failed to retrieve secret 2.")
else:
    print("Failed to authenticate to Key Vault.")


