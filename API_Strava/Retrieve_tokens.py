# PARTIE 1 : RECUPERATION DU CODE
# SE CONNECTER A L'URL SUIVANTE EN METTANT SON CLIENT_ID : https://www.strava.com/oauth/authorize?client_id=CLIENTID123&response_type=code&redirect_uri=http://localhost&scope=activity:read&approval_prompt=auto

# PARTIE 2 : UTILISER LE CODE DANS LE SCRIPT SUIVANT POUR RECUPERER LES TOKENS
!pip install stravalib
from stravalib.client import Client

CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
REDIRECT_URI = 'http://localhost'

client = Client()

code = input("mettre le code ").strip()

token_response = client.exchange_code_for_token(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    code=code
)

print("Access Token :", token_response['access_token'])
print("Refresh Token :", token_response['refresh_token'])
print("Expires at (timestamp) :", token_response['expires_at'])
