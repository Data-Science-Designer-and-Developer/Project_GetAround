import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

# 1️⃣ Charger le dataset
url = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv"
df = pd.read_csv(url)

# 2️⃣ Nettoyer les colonnes
df.columns = df.columns.str.strip()

# 3️⃣ Définir la cible (prix)
target_col = "rental_price_per_day"
y = df[target_col]

# 4️⃣ Sélectionner les features utiles (tout sauf IDs et target)
features = [c for c in df.columns if c not in ["Unnamed: 0", "model_key", target_col]]
X = df[features]

# Encoder les colonnes catégorielles
X = pd.get_dummies(X, drop_first=True)

# 5️⃣ Supprimer les lignes où la cible est manquante
mask = y.notna()
X = X[mask]
y = y[mask]

# 6️⃣ Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 7️⃣ Entraîner le modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8️⃣ Créer le dossier api si nécessaire
os.makedirs("api", exist_ok=True)

# 9️⃣ Sauvegarder le modèle
joblib.dump(model, "api/model.pkl")
print("Modèle de pricing entraîné et sauvegardé ✅")

from transformers import AutoModel
model = AutoModel.from_pretrained("./models/GetAround-Price-Optimisation")
