import time
import requests
import pandas as pd
from datetime import datetime

# ⬇️ Renseigne tes tokens ici
access_token = "ACCESS_TOKEN"
refresh_token = "REFRESH_TOKEN"
expires_at = "TIMESTAMP"  # Timestamp Unix

# ⬇️ Paramètres fixes
client_id = "CLIENT_ID"
client_secret = "SECRET"
user_id = None  # sera rempli après première requête réussie

# ⏳ Fonction pour rafraîchir le token
def refresh_tokens(refresh_token):
    url = "https://wbsapi.withings.net/v2/oauth2"
    payload = {
        'action': 'requesttoken',
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    data = response.json()
    if data['status'] != 0:
        raise Exception(f"Erreur Withings (refresh) : {data}")
    return data['body']

# ✅ Vérifie expiration du token
current_time = int(time.time())
if current_time >= expires_at:
    print("🔁 Le token a expiré, on le rafraîchit...")
    new_tokens = refresh_tokens(refresh_token)
    access_token = new_tokens['access_token']
    refresh_token = new_tokens['refresh_token']
    expires_at = current_time + new_tokens['expires_in']
    
    expiration_human = datetime.fromtimestamp(expires_at).strftime("%Y-%m-%d %H:%M:%S")
    print("✅ Nouveaux tokens :")
    print("Access token :", access_token)
    print("Refresh token :", refresh_token)
    print("Expires in :", new_tokens['expires_in'], "secondes")
    print(f"📅 Expiration lisible : {expiration_human}")
    print(f"🧾 Ligne à copier-coller : expires_at = {expires_at}")
else:
    print("✅ Token encore valide")
    print("📅 Expiration :", datetime.fromtimestamp(expires_at).strftime("%Y-%m-%d %H:%M:%S"))

# 📦 Récupération des mesures (poids, masse grasse, etc.)
url = "https://wbsapi.withings.net/measure"
headers = {"Authorization": f"Bearer {access_token}"}
params = {
    "action": "getmeas",
    "meastypes": ",".join(map(str, [1, 5, 6, 8, 76, 77, 88])),  # types de mesures
    "category": 1,  # mesures de type "user"
    "startdate": int(time.time()) - 30 * 24 * 3600,  # 30 derniers jours
    "enddate": int(time.time()),
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

if data['status'] != 0:
    raise Exception(f"Erreur récupération données : {data}")

# 🧾 Préparation des données pour export CSV
rows = []
for group in data['body']['measuregrps']:
    date = datetime.fromtimestamp(group['date']).strftime("%Y-%m-%d %H:%M:%S")
    entry = {"date": date}
    for m in group['measures']:
        type_id = m['type']
        value = m['value'] * (10 ** m['unit'])
        label = {
            1: "poids_kg",
            5: "masse_musculaire_kg",
            6: "masse_grasse_pct",
            8: "hydratation_pct",
            76: "gras_visceral",
            77: "masse_osseuse_kg",
            88: "masse_maigre_kg",
        }.get(type_id, f"type_{type_id}")
        entry[label] = round(value, 2)
    rows.append(entry)

df = pd.DataFrame(rows).sort_values('date')
print("\n📊 Aperçu des données récupérées :")
print(df.head())

# 💾 Export en CSV
csv_filename = "withings_measures.csv"
df.to_csv(csv_filename, index=False)
print(f"\n✅ Export CSV terminé : '{csv_filename}'")
