# 🚗 GetAround — Delay Analysis & Pricing Prediction
> Certification CDSD — Data Science & Deployment Project — Jedha Bootcamp

---

## 📌 Project Overview

GetAround is a peer-to-peer car rental platform. Late vehicle returns create friction
for subsequent rentals, leading to customer dissatisfaction and cancellations.

This project addresses two strategic challenges:

- **Operational optimization** — Analyzing late checkouts and simulating minimum delay
  thresholds to reduce conflicts between consecutive rentals.
- **Pricing optimization** — Serving a Machine Learning model via a production API to
  help owners set optimal daily rental prices.

---

## 🔗 Production Links

| Service | URL |
|---------|-----|
| 📊 Dashboard | https://huggingface.co/spaces/Dreipfelt/getaround-dashboard |
| 🔌 API | https://Dreipfelt-getaround-api.hf.space |
| 📄 API Docs | https://Dreipfelt-getaround-api.hf.space/docs |
| ⚙️ Swagger UI | https://Dreipfelt-getaround-api.hf.space/swagger |
| 💻 GitHub | https://github.com/Data-Science-Designer-and-Developer/Project_GetAround |

---

## 🎯 Business Objectives

### Delay Management

- Measure how often drivers return cars late
- Quantify the impact on subsequent rentals
- Simulate different minimum delay thresholds (0 to 720 minutes)
- Help Product Management choose:
  - an optimal delay **threshold**
  - an appropriate **scope** (all cars vs Connect only)

### Pricing Optimization

- Train a ML model on car characteristics
- Serve predictions via a REST API
- Allow real-time price prediction through a `/predict` endpoint

---

## 📊 Dashboard

The interactive dashboard allows Product Managers to:

- Visualize the distribution of late checkouts
- Compare Connect vs Mobile check-in types
- Simulate the trade-off between blocked rentals and resolved issues
- Filter by scope and threshold in real time
- Get a live price prediction from the API

🔗 https://huggingface.co/spaces/Dreipfelt/getaround-dashboard

---

## 🤖 Machine Learning API

### Model

| Property | Value |
|----------|-------|
| Algorithm | XGBoost Regressor (sklearn Pipeline) |
| Target | rental_price_per_day (€) |
| R² | ~0.68 |
| RMSE | XX € ← à remplacer depuis le notebook |
| Features | 28 (mileage, engine_power, fuel, color, car_type, options…) |

> **Baseline context:** a naive model predicting the dataset mean achieves R² = 0.
> Our model's R² of 0.68 represents a substantial improvement over this baseline,
> explaining 68% of price variance from car characteristics alone.

### Endpoint `/predict`

- **Method**: POST
- **Input**: JSON with key `input` — list of lists (one per car)
- **Validation**: each row must contain exactly the number of features defined in
  `feature_names.json`; the API returns a `422` error with a descriptive message
  if the input is malformed.

```bash
curl -X POST "https://Dreipfelt-getaround-api.hf.space/predict" \
     -H "Content-Type: application/json" \
     -d '{"input": [[150000, 120, 1, 1, 1, 0, 1, 1, 0]]}'
```

**Response:**
```json
{"prediction": [104.75]}
```

📄 Full documentation: https://Dreipfelt-getaround-api.hf.space/docs  
⚙️ Swagger UI: https://Dreipfelt-getaround-api.hf.space/swagger

---

## 🗂️ Repository Structure

```
Project_GetAround/
├── api/                        # FastAPI application
│   ├── app.py                  # API endpoints
│   ├── Dockerfile              # Docker configuration
│   └── feature_names.json      # Model feature names
│
├── dashboard/                  # Streamlit dashboard
│   ├── app.py                  # Dashboard application
│   └── requirements.txt
│
├── notebooks/                  # Jupyter notebooks
│   ├── 01_EDA_delays.ipynb     # Delay analysis
│   └── 02_ML_pricing.ipynb     # ML model training
│
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| Language | Python 3.10 |
| Dashboard | Streamlit, Plotly |
| API | FastAPI, Uvicorn |
| ML | Scikit-learn, XGBoost Regressor |
| Deployment | Hugging Face Spaces, Docker |
| Version Control | Git, GitHub |

---

## 🔒 Data & Privacy (RGPD / GDPR)

The datasets used in this project (`get_around_delay_analysis.xlsx` and the pricing
dataset) contain **no personal data**: rental IDs are anonymous identifiers, and no
name, email, phone number, or precise location is present.

The API processes only technical car characteristics (mileage, engine power, equipment
options) submitted by the user. This data is used for real-time inference only and is
**not stored or logged** after the response is returned.

The service is hosted on **Hugging Face Spaces** (EU infrastructure), consistent with
RGPD requirements. No third-party analytics or tracking is used.

---

## ⚙️ Local Setup

```bash
# Clone the repo
git clone https://github.com/Data-Science-Designer-and-Developer/Project_GetAround.git
cd Project_GetAround

# Install dependencies
pip install -r dashboard/requirements.txt

# Run the dashboard
streamlit run dashboard/app.py

# Run the API
cd api
uvicorn app:app --reload
# API available at http://localhost:8000
# Swagger UI at http://localhost:8000/swagger
# Custom docs at http://localhost:8000/docs
```

---

## 👤 Author

**Frédéric**  
CDSD Candidate — Data Scientist  
Jedha Bootcamp
