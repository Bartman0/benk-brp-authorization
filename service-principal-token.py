import os
from azure.identity import ClientSecretCredential, DefaultAzureCredential

# Retrieve the IDs and secret to use with ServicePrincipalCredentials
tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]
scope = os.environ["AZURE_SCOPE"]

# credential = DefaultAzureCredential()
credential = ClientSecretCredential(
    tenant_id=tenant_id, client_id=client_id, client_secret=client_secret
)

print(credential.get_token(scope, tenant_id=tenant_id))
