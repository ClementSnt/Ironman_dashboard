# PARTIE 1 : RECUPERATION DE L'URL
# URL pour se connecter au compte Withings et récupérer le bon code
import urllib.parse

client_id = 'CLIENT_ID'
redirect_uri = 'http://localhost'
scope = 'user.metrics'  # pour poids, masse grasse, etc.

params = {
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': scope,
    'state': 'SECRET_INDICATOR'
}

auth_url = f"https://account.withings.com/oauth2_user/authorize2?{urllib.parse.urlencode(params)}"
# Cliquer sur l'url obtenu et se connecter via ses identifiants Withings
print(auth_url)




# PARTIE 2 : RECUPERATION DE L'ACCESS ET REFRESH TOKEN
import requests

code = "CODE OBTENU DANS L'ETAPE PRECEDENTE"
client_id = "CLIENT_ID"
client_secret = "SECRET"
redirect_uri = "http://localhost"

response = requests.post(
    "https://wbsapi.withings.net/v2/oauth2",
    data={
        'action': 'requesttoken',
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
)

data = response.json()

# Print des tokens initiaux pour la requête Withings_fetch.py
print("Access token :", data['body']['access_token'])
print("Refresh token:", data['body']['refresh_token'])
print("Expires in  :", data['body']['expires_in'], "secondes")
