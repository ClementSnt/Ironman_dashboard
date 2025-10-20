import numpy as np
import pandas as pd
import streamlit as st
import math
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ----------------------
# Import des données
# ----------------------
df = pd.read_csv(r'data/outputIM.csv', sep=";")
trimp = pd.read_csv(r"data/training_dashboard/Trimp_plan.csv", sep=";")



# ==========================================================
# 🔹 Préparation des données
# ==========================================================
IRONMAN_DATE = datetime(2026, 7, 5)

df["date"] = pd.to_datetime(df["date"])
df["week_sunday"] = df["date"] + pd.to_timedelta(6 - df["date"].dt.weekday, unit="d")
df["weeks_before_ironman"] = ((IRONMAN_DATE - df["week_sunday"]).dt.days // 7) * -1

# --- TRIMP hebdomadaire ---
df_trimp = (
    df.groupby("weeks_before_ironman", as_index=False)["TRIMP"]
    .sum()
    .rename(columns={"TRIMP": "TRIMP_actuals"})
)

trimp_plot = trimp.merge(
    df_trimp, how="left", left_on="semaine_num", right_on="weeks_before_ironman"
)

# --- Heures par activité ---
df_activities = (
    df[df["activity"] != "No_training"]
    .groupby(["weeks_before_ironman", "activity"], as_index=False)["duree_sec"]
    .sum()
)
df_activities["heures"] = df_activities["duree_sec"] / 3600

# ==========================================================
# 🔹 Interface Streamlit
# ==========================================================
st.set_page_config(page_title="Dashboard Ironman", layout="wide")
st.title("️Suivi d’entraînement – Ironman 70.3 🏊‍♂🚴‍♂️️🏃‍♂️")

# ==========================================================
# SECTION 1 – Charge TRIMP
# ==========================================================
st.subheader("Évolution du TRIMP hebdomadaire")

fig_trimp = go.Figure()

# Bande verte cible (min / max)
fig_trimp.add_trace(go.Scatter(
    x=trimp_plot["semaine_num"],
    y=trimp_plot["TRIMP_max"],
    line=dict(color="green", width=0),
    mode="lines",
    showlegend=False
))
fig_trimp.add_trace(go.Scatter(
    x=trimp_plot["semaine_num"],
    y=trimp_plot["TRIMP_min"],
    fill="tonexty",
    fillcolor="rgba(0,255,0,0.2)",
    line=dict(color="green", width=0),
    mode="lines",
    name="Zone cible"
))
# Planifié vs Réalisé
fig_trimp.add_trace(go.Scatter(
    x=trimp_plot["semaine_num"],
    y=trimp_plot["TRIMP"],
    mode="lines",
    name="Planifié",
    line=dict(color="limegreen", dash="dash")
))
fig_trimp.add_trace(go.Scatter(
    x=trimp_plot["semaine_num"],
    y=trimp_plot["TRIMP_actuals"],
    mode="lines+markers",
    name="Réalisé",
    line=dict(color="deepskyblue", width=3)
))

fig_trimp.add_vline(
    x=0,  # semaine 0 = date Ironman
    line=dict(color="red", width=2, dash="dot"),
    annotation_text="   IRON MAN",
    annotation_position="top right",
    annotation_font=dict(color="red")
)

fig_trimp.update_layout(
    template="plotly_dark",
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white"),
    xaxis_title="Semaines avant Ironman",
    yaxis_title="TRIMP",
)

st.plotly_chart(fig_trimp, use_container_width=True)

# ==========================================================
# SECTION 2 – Répartition par activité
# ==========================================================
st.subheader("Répartition des heures par activité")

activities = sorted(df_activities["activity"].unique())
selected_activities = st.multiselect(
    "Sélectionner les activités :", options=activities, default=activities
)

filtered = df_activities[df_activities["activity"].isin(selected_activities)].copy()
filtered["activity"] = filtered["activity"].replace("VirtualRide", "Ride")
filtered = filtered[filtered["weeks_before_ironman"] >= -43]

fig_bar = px.bar(
    filtered,
    x="weeks_before_ironman",
    y="heures",
    color="activity",
    barmode="stack",
    title="Heures d'entraînement par semaine et par activité",
    color_discrete_sequence=px.colors.qualitative.Prism
)

fig_bar.update_layout(
    template="plotly_dark",
    plot_bgcolor="#0e1117",
    paper_bgcolor="#0e1117",
    font=dict(color="white"),
    xaxis_title="Semaines avant Ironman",
    yaxis_title="Heures d'entraînement",
    legend_title_text="Activité",
)
st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================================
# SECTION 3 – Prédictions de performances
# ==========================================================
st.title("🔮 Prédictions de performances")

# ---------- Fonctions utilitaires ----------
def label_type_course(dist):
    if 4.5 <= dist <= 5.5: return "5km"
    if 9.5 <= dist <= 10.5: return "10km"
    if 20 <= dist <= 22.5: return "Semi"
    if 40 <= dist <= 43: return "Marathon"
    return None

def compute_vdot(dist_km, t_sec):
    v = dist_km * 1000 / t_sec
    t_min = t_sec / 60
    vo2 = -4.6 + 0.182258 * v * 60 + 0.000104 * (v * 60)**2
    pct = 0.8 + 0.1894393 * math.exp(-0.012778 * t_min) + 0.2989558 * math.exp(-0.1932605 * t_min)
    return vo2 / pct

def predict_time(dist_km, vdot):
    best_t, best_diff = None, 1e9
    for t in range(600, 20000):  # 10 min à 5h
        diff = abs(compute_vdot(dist_km, t) - vdot)
        if diff < best_diff:
            best_t, best_diff = t, diff
    return best_t

def get_zone3_speed(df, sports):
    subset = df[df["activity"].isin(sports)]
    subset = subset[subset["zone"] == "Z3"]
    if subset.empty:
        return None
    return (subset["vitesse_moy_kmh"] * subset["duree_sec"]).sum() / subset["duree_sec"].sum()

# ---------- Calculs Running ----------
df_run = df[df["activity"] == "Run"].copy()
df_run["type_course"] = df_run["distance_km"].apply(label_type_course)
df_run["vitesse_moy_kmh"] = df_run["distance_km"] / (df_run["duree_sec"] / 3600)
df_best = df_run.loc[df_run.groupby("type_course")["vitesse_moy_kmh"].idxmax()].dropna()

vdot_dict = {r["type_course"]: compute_vdot(r["distance_km"], r["duree_sec"]) for _, r in df_best.iterrows()}

targets = {"5km": 5, "10km": 10, "Semi": 21.1, "Marathon": 42.195}
preds = {}

for name, dist in targets.items():
    weights, values = [], []
    for k, d in targets.items():
        if k in vdot_dict:
            w = 1 / (abs(d - dist) + 1e-6)
            weights.append(w)
            values.append(vdot_dict[k] * w)
    agg_vdot = sum(values) / sum(weights) if weights else None
    preds[name] = {
        "vdot": round(agg_vdot, 2) if agg_vdot else None,
        "pred_time_sec": predict_time(dist, agg_vdot) if agg_vdot else None
    }

running_df = pd.DataFrame(preds).T
running_df["Temps prédit"] = running_df["pred_time_sec"].apply(
    lambda s: pd.to_datetime(s, unit="s").strftime("%H:%M:%S") if pd.notnull(s) else None
)

st.subheader("Running")
st.dataframe(running_df[["Temps prédit"]], hide_index=False)

# ---------- Calculs Triathlon ----------
bike_speed = get_zone3_speed(df, ["Ride", "VirtualRide"])
swim_speed = get_zone3_speed(df, ["Swim"])

malus_run = {"S": 0.07, "M": 0.10, "Half": 0.15}
malus_bike = {"S": 0.02, "M": 0.03, "Half": 0.05}

distances = {
    "S": {"swim": 0.75, "bike": 20, "run": 5},
    "M": {"swim": 1.5, "bike": 40, "run": 10},
    "Half": {"swim": 1.9, "bike": 90, "run": 21.1}
}

tri_results = []
for race, dist in distances.items():
    run_key = "5km" if dist["run"] <= 5.5 else "10km" if dist["run"] <= 10.5 else "Semi"
    run_time = running_df.loc[run_key, "pred_time_sec"]
    run_speed = dist["run"] / (run_time / 3600) if run_time else None

    run_sec = dist["run"] / run_speed * 3600 * (1 + malus_run[race])
    bike_sec = dist["bike"] / bike_speed * 3600 * (1 + malus_bike[race])
    swim_sec = dist["swim"] / swim_speed * 3600
    total = run_sec + bike_sec + swim_sec

    tri_results.append({
        "Format": race,
        "Natation": pd.to_datetime(swim_sec, unit="s").strftime("%H:%M:%S"),
        "Vélo": pd.to_datetime(bike_sec, unit="s").strftime("%H:%M:%S"),
        "Course": pd.to_datetime(run_sec, unit="s").strftime("%H:%M:%S"),
        "Total": pd.to_datetime(total, unit="s").strftime("%H:%M:%S")
    })

tri_df = pd.DataFrame(tri_results)
st.subheader("Triathlon")
st.dataframe(tri_df, hide_index=True)


# ---------------------------------------------------------
# Section 3 – Analyse des calories par activité
# ---------------------------------------------------------
st.title("🔥 Dépense énergétique par activité")

# Vérification des colonnes nécessaires
if all(col in df.columns for col in ["activity", "duree_sec", "calories"]):
    # Agrégation calories et durée par activité
    df_cal = (
        df[df["activity"] != "No_training"]
        .groupby("activity")[["duree_sec", "calories"]]
        .sum()
        .reset_index()
    )

    # Calcul des calories par minute
    df_cal["calories_par_min"] = df_cal["calories"] / (df_cal["duree_sec"] / 60)
    df_cal = df_cal.sort_values("calories_par_min", ascending=False)


    # ----- Treemap Chart -----
    st.subheader("Calories brûlées/min par activité (treemap)")
    import plotly.express as px

    fig_treemap = px.treemap(
        df_cal,
        path=["activity"],          # Chaque activité = un rectangle
        values="calories_par_min",  # Taille proportionnelle aux calories/min
        color="calories_par_min",   # Couleur selon la valeur
        color_continuous_scale="Teal",
        hover_data={"calories_par_min": True},
        custom_data=["calories_par_min"]
    )

    fig_treemap.update_traces(
        texttemplate="%{label}<br>%{customdata[0]:.1f} cal/min",
        textposition="middle center"
    )

    fig_treemap.update_layout(
        template="plotly_dark",
        font=dict(color="white"),
        height=700,  # augmente la hauteur pour mieux répartir les rectangles
        margin=dict(t=50, l=25, r=25, b=25)  # marges pour ne pas écraser le titre
    )

    st.plotly_chart(fig_treemap, use_container_width=True)

else:
    st.warning("Les colonnes 'activity', 'duree_sec' et 'calories' sont nécessaires pour cette analyse.")
