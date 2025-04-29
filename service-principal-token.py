import os
import jwt
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

token = credential.get_token(scope, tenant_id=tenant_id).token
token_decoded = jwt.decode(token, options={"verify_signature": False})
# print(token_decoded)
print(token_decoded["roles"])
