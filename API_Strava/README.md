# API Strava

## Ce dossier contient les scripts suivant :
- Strava_fetch.py : version finale que j'utilise pour récupérer mes données de l'API STRAVA
- Retrieve_tokens.py : que j'ai utilisé pour récupérer mes tokens pour la première fois (access et refresh)

## Ce que le script final fait :
- Authentification OAuth2 avec rafraîssement automatique des tokens
- Récupération des activités sportives réalisées (type, temps, distance, vitesse, fréquence cardiaque moyenne et calories dépensées)
- Export en CSV

Pour pouvoir intéragir avec l'API il faut avoir créé une application https://www.strava.com/settings/api (Client_ID et secret)
