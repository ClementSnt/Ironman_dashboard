# 🏊‍♂️ PERSONAL PERFORMANCE DASHBOARD – IRONMAN 70.3


Pour accéder au Dashboard => [Ici]([https://streamlit.io](https://ironmandashboard.streamlit.app/))
---

## 🎯 OBJECTIF

Ce projet vise à créer un outil personnel de suivi sportif pour ma préparation à un Ironman 70.3.  
Il permet de :

- Suivre l’évolution de la charge d'entraînement semaine par semaine (métrique utilisée => TRIMP)
- Comparer cette charge d’entraînement avec les recommandations en fonction des semaines avant l’Ironman  
- Prédire mes temps théoriques sur différentes courses (5 km, 10 km, semi-marathon, marathon, triathlon S M et Ironman 70.3 bien sûr)  
- Analyser les calories brûlées par activité  

---

## 📊 DONNÉES UTILISÉES

- **Strava API** : activités sportives (running, vélo, natation…) — intégration complète  
- **Données santé** : extraites via l'API withings mais non visibles dans le dashboard version publique car données trop personnelles. Le code est disponible cependant.

> Les fichiers CSV nécessaires sont inclus dans le repo dans le dossier `data/`.

---

## 🧩 FONCTIONNALITÉS

- **Visualisation de la charge d’entraînement (TRIMP)** vs zone cible  
- **Répartition des heures d’entraînement** par activité et semaine  
- **Prédiction des temps de course** (running et triathlon) => méthode utilisée est celle du VDOT + pondération selon les distances connues avec application de malus sur la partie vélo sur triathlon
- **Analyse des calories brûlées par activité** (treemap interactif)  
- **Interface interactive Streamlit** avec graphiques Plotly  

---

## 🧠 TECHNOLOGIES

- **Langage** : Python  
- **Librairies** : Pandas, NumPy, Plotly, Streamlit, math  
- **Visualisation** : Plotly (line plot, bar chart, treemap)  
- **Modélisation** : prédiction de temps sur base de VDOT et historique  

---

## 🏁 OBJECTIF FINAL

Un **outil personnel complet** pour suivre et optimiser ma préparation Ironman, visualiser ma charge et mes performances, et explorer les données de mes entraînements.

---

## 🔍 Résultats

Voici les variations que j'ai eu à l'occasion de mon premier triathlon M :

| Discipline  | Prédiction | Réel      | Écart     |
|------------|------------|-----------|-----------|
| Natation   | 30:33      | 27:56     | -2:37     |
| Vélo       | 1:23:15    | 1:28:00   | +4:45     |
| Course     | 51:36      | 51:12     | -0:24     |

