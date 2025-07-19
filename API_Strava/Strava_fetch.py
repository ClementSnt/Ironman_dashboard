from stravalib.client import Client
import time
import json
import pandas as pd
from google.colab import files

# === 🔐 Renseigne ici tes identifiants ===
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'

# === 🧠 Tokens stockés manuellement dans la cellule ===
token_data = {
    "access_token": "ACCESS_TOKEN",
    "refresh_token": "REFRESH_TOKEN",
    "expires_at": "TIMESTAMP"
}

# === 🔁 Fonction d'authentification avec rafraîchissement conditionnel ===
def get_authenticated_client(token_data):
    now = int(time.time())

    if now >= token_data['expires_at']:
        print("⏳ Token expiré, on le rafraîchit...")
        client = Client()
        refreshed = client.refresh_access_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            refresh_token=token_data['refresh_token']
        )
        token_data.update({
            'access_token': refreshed['access_token'],
            'refresh_token': refreshed['refresh_token'],
            'expires_at': refreshed['expires_at']
        })

        # 🔁 Affiche les nouveaux tokens à copier-coller
        print("\n🔁 Token rafraîchi ! Copie-colle ceci dans ta cellule `token_data` :")
        print(json.dumps(token_data, indent=4))
    else:
        print("✅ Token encore valide, pas de refresh nécessaire.")

    client = Client()
    client.access_token = token_data['access_token']
    return client

# === 🚴 Connexion à l'API Strava ===
client = get_authenticated_client(token_data)

# === 📥 Récupération des 10 dernières activités ===
activities = client.get_activities(limit=1)

for summary in activities:
    print("–––")
    print(f"Nom         : {summary.name}")
    print(f"Date        : {summary.start_date_local}")
    print(f"Type        : {summary.type}")

    distance_km = float(summary.distance) / 1000 if summary.distance else None
    print(f"Distance    : {distance_km:.2f} km" if distance_km else "Distance    : Non dispo")

    duration_s = int(summary.moving_time) if summary.moving_time else None
    print(f"Durée       : {duration_s} sec" if duration_s else "Durée       : Non dispo")

    avg_speed_kmh = float(summary.average_speed) * 3.6 if summary.average_speed else None
    print(f"Vitesse moy : {avg_speed_kmh:.2f} km/h" if avg_speed_kmh else "Vitesse moy : Non dispo")

    if hasattr(summary, 'average_heartrate') and summary.average_heartrate:
        print(f"FC Moyenne  : {summary.average_heartrate:.0f} bpm")
    else:
        print("FC Moyenne  : Non dispo")

    detailed = client.get_activity(summary.id)
    if hasattr(detailed, 'calories') and detailed.calories:
        print(f"Calories    : {detailed.calories:.0f}")
    else:
        print("Calories    : Non dispo")


# === 🧾 Liste d'activités à exporter ===
activity_list = []

for summary in activities:
    detailed = client.get_activity(summary.id)

    activity_data = {
        'nom': summary.name,
        'date': summary.start_date_local,
        'type': summary.type,
        'distance_km': float(summary.distance) / 1000 if summary.distance else None,
        'duree_sec': int(summary.moving_time) if summary.moving_time else None,
        'vitesse_moy_kmh': float(summary.average_speed) * 3.6 if summary.average_speed else None,
        'fc_moyenne': summary.average_heartrate if hasattr(summary, 'average_heartrate') else None,
        'calories': detailed.calories if hasattr(detailed, 'calories') else None
    }

    activity_list.append(activity_data)

# === 💾 Export vers CSV ===
df = pd.DataFrame(activity_list)
df.to_csv('strava_activities.csv', index=False)

print("\n✅ Export CSV terminé : 'strava_activities.csv'")
