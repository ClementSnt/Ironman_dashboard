# API Withings

Ce dossier contient les scripts suivant :
- Withings_fetch.py : version finale que j'utilise pour récupérer mes données de l'API Withings
- Retrieve_tokens.py : que j'ai utilisé pour récupérer mes tokens pour la première fois (access et refresh)

## Ce que le script final fait :
- Authentification OAuth2 avec rafraîssement automatique des tokens
- Récupération par jour du poids, masse grasse, hydratation, masse musculaire en kg et en pourcentage
- Export en CSV


Il faut un compte developpeur (gratuit) pour pouvoir intérargir avec l'API : https://developer.withings.com
