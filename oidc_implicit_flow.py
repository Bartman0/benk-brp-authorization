import os
import gnureadline as readline
import requests
import jwt
from urllib.parse import urlparse, parse_qs
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend


# Configuration
APPLICATION_ID = os.environ["AZURE_APPLICATION_ID"]
TENANT_ID = os.environ["AZURE_TENANT_ID"]
AUTH_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
KEYS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/keys?appid={APPLICATION_ID}"
CLIENT_ID = os.environ["AZURE_APPLICATION_ID"]
REDIRECT_URI = "https://mks-frontend-d0cpa7fnf0cubkhf.westeurope-01.azurewebsites.net/"

PEMSTART = "-----BEGIN CERTIFICATE-----\n"
PEMEND = "\n-----END CERTIFICATE-----\n"


# Step 0: Get application public keys
def get_public_keys():
    result = requests.get(KEYS_URL)
    return result.json()


# Step 1: Redirect to the Authorization Server
def initiate_auth():
    params = {
        "response_type": "id_token",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email offline_access",
        "nonce": 69,
        "response_mode": "fragment",
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
    print(query_params)
    id_token = query_params.get("id_token")[0]

    return id_token


# Step 3: Verify and Use the Access Token
def verify_id_token(id_token):
    # In a real scenario, you would validate the ID token with the authorization server.
    # Here we'll just print some information about the tokens.
    # print(f"ID Token raw: {id_token}")
    print("-" * 32)
    token = jwt.decode(id_token, options={"verify_signature": False})
    print(f"ID Token: {token}")
    print("-" * 32)
    print(f"App roles: {token['roles']}")


# Step 4: Get access token
def get_access_token():
    body = {
        "scope": f"{APPLICATION_ID}/.default",
        "client_id": os.environ["AZURE_CLIENT_ID"],
        "client_secret": os.environ["AZURE_CLIENT_SECRET"],
        "grant_type": "client_credentials",
    }

    token_url = f"{TOKEN_URL}"
    response = requests.post(token_url, data=body).json()
    return response["access_token"]


def get_key_id(access_token):
    header = jwt.get_unverified_header(access_token)
    return header["kid"], header["alg"]


def validate_access_token(access_token, key, algorithm):
    decoded = jwt.decode(
        access_token,
        key=key,
        algorithms=algorithm,
        audience=os.environ["AZURE_APPLICATION_ID"],
    )
    return decoded


def decode_token(token):
    print("-" * 32)
    header = jwt.get_unverified_header(token)
    for key in header.keys():
        print(f"{key}: {str(header[key])}")

    algorithm = jwt.get_unverified_header(token)["alg"]

    decoded = jwt.decode(
        token, algorithms=[algorithm], options={"verify_signature": False}
    )

    print("-" * 32)
    for key in decoded.keys():
        print(f"{key}: {str(decoded[key])}")
    print("-" * 32)


def get_public_key(public_keys, key_id):
    key = [key for key in public_keys["keys"] if key["kid"] == key_id][0]
    mspubkey = str(key["x5c"][0])
    cert_str = PEMSTART + mspubkey + PEMEND
    cert_obj = load_pem_x509_certificate(bytes(cert_str, "ascii"), default_backend())
    public_key = cert_obj.public_key()
    return public_key


# Main Execution
if __name__ == "__main__":
    public_keys = get_public_keys()
    auth_url = initiate_auth()
    id_token = handle_redirect()
    verify_id_token(id_token)
    access_token = get_access_token()
    print(access_token)
    decode_token(access_token)
    key_id, algorithm = get_key_id(access_token)
    public_key = get_public_key(public_keys, key_id)
    decoded = validate_access_token(access_token, public_key, algorithm)
    print(decoded)
