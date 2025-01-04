import os
import gnureadline as readline
import requests
import jwt
from urllib.parse import urlparse, parse_qs

# Configuration
TENANT_ID = os.environ["AZURE_TENANT_ID"]
AUTH_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
CLIENT_ID = os.environ["AZURE_APP_ID_2"]
REDIRECT_URI = (
    "http://localhost:3000"  # This should match your redirect URI in the OIDC provider
)


# Step 1: Redirect to the Authorization Server
def initiate_auth():
    params = {
        "response_type": "id_token",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "nonce": 69,
    }

    auth_url = f"{AUTH_URL}?{requests.compat.urlencode(params)}"

    print(f"Please visit the following URL to authenticate: {auth_url}")
    return auth_url


# Step 2: Handle the Redirect and Extract the Access Token
def handle_redirect():
    # After authenticating, the browser will redirect back to REDIRECT_URI with an authorization code
    # We need to simulate this for demonstration purposes. In a real scenario, you would capture this from your server.

    # For demonstration, we'll manually provide the URL received after authentication
    redirected_url = input("Please enter the URL you were redirected to: ")

    parsed_url = urlparse(redirected_url)
    query_params = parse_qs(parsed_url.fragment)

    id_token = query_params.get("id_token")[0]

    return id_token


# Step 3: Verify and Use the Access Token
def verify_access_token(id_token):
    # In a real scenario, you would validate the ID token with the authorization server.
    # Here we'll just print some information about the tokens.
    # print(f"ID Token raw: {id_token}")
    print("-" * 32)
    token = jwt.decode(id_token, options={"verify_signature": False})
    print(f"ID Token: {token}")
    print("-" * 32)
    print(f"App roles: {token['roles']}")


# Main Execution
if __name__ == "__main__":
    auth_url = initiate_auth()
    id_token = handle_redirect()
    verify_access_token(id_token)
