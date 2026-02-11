# app.py
import os
import subprocess
import streamlit as st
import pandas as pd
import joblib

# ────────────── 1️⃣ Lancement automatique du modèle ──────────────
MODEL_PATH = "api/model.pkl"
if not os.path.exists(MODEL_PATH):
    st.info("Le modèle n'existe pas, lancement de l'entraînement...")
    subprocess.run(["python", "api/train_model.py"], check=True)
    st.success("Modèle entraîné et sauvegardé ✅")

# ────────────── 2️⃣ Charger le modèle ──────────────
model_path = MODEL_PATH
model = joblib.load(model_path)

# ────────────── 3️⃣ Définir les colonnes/features utilisées ──────────────
features = [
    'mileage', 'engine_power', 'fuel', 'paint_color', 'car_type',
    'private_parking_available', 'has_gps', 'has_air_conditioning',
    'automatic_car', 'has_getaround_connect', 'has_speed_regulator', 'winter_tires'
]

categorical_options = {
    'fuel': ['diesel', 'gasoline', 'electric', 'hybrid'],
    'paint_color': ['white', 'black', 'grey', 'blue', 'red', 'green'],
    'car_type': ['sedan', 'suv', 'convertible', 'coupe', 'van']
}

st.title("GetAround Pricing Prediction 🚗")

# ────────────── 4️⃣ Collecte des inputs utilisateur ──────────────
input_data = {}
for col in features:
    if col in categorical_options:
        input_data[col] = st.selectbox(f"{col}", categorical_options[col])
    elif col in ["private_parking_available", "has_gps", "has_air_conditioning", "automatic_car",
                 "has_getaround_connect", "has_speed_regulator", "winter_tires"]:
        input_data[col] = st.checkbox(col)
    else:
        input_data[col] = st.number_input(col, min_value=0, value=0)

df_input = pd.DataFrame([input_data])
df_input = pd.get_dummies(df_input)
for c in model.feature_names_in_:
    if c not in df_input.columns:
        df_input[c] = 0
df_input = df_input[model.feature_names_in_]

# ────────────── 5️⃣ Faire la prédiction ──────────────
if st.button("Prédire le prix"):
    prediction = model.predict(df_input)[0]
    st.success(f"Prix estimé par jour : {prediction:.2f} €")