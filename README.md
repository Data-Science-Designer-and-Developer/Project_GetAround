# 🚗 GetAround — Delay Analysis & Pricing Prediction

---

## 📌 Project Overview

GetAround is a peer-to-peer car rental platform where late vehicle returns can disrupt subsequent bookings, leading to customer dissatisfaction and cancellations.

This project tackles two key product challenges:

* **Operational optimisation** — analysing checkout delays and simulating buffer thresholds
* **Pricing optimisation** — deploying a Machine Learning model via a production API

---

## 🔗 Live Applications

| Service            | Description                          | URL                                                                      |
| ------------------ | ------------------------------------ | ------------------------------------------------------------------------ |
| 📊 Delay Dashboard | Product analytics & delay simulation | https://huggingface.co/spaces/Dreipfelt/getaround-dashboard              |
| 💰 Pricing Demo    | UI for real-time price prediction    | *(add your HF Space URL here)*                                           |
| 🔌 API             | FastAPI prediction service           | https://dreipfelt-getaround-api.hf.space                                 |
| 📄 API Docs        | Interactive documentation            | https://dreipfelt-getaround-api.hf.space/docs                            |
| 💻 GitHub          | Source code repository               | https://github.com/Data-Science-Designer-and-Developer/Project_GetAround |

---

## 🎯 Business Objectives

### Delay Management

* Measure late returns
* Simulate threshold strategies
* Optimise trade-off between blocked rentals and solved issues

### Pricing Optimisation

* Predict rental price from vehicle features
* Serve model via API
* Enable real-time decision support

---

## 🤖 Machine Learning API

| Property           | Value                    |
| ------------------ | ------------------------ |
| Algorithm          | XGBoost Regressor        |
| Target             | rental_price_per_day (€) |
| RMSE               | 16.60                    |
| MAE                | 10.50                    |
| R²                 | 0.738                    |
| CV RMSE            | 16.86                    |
| CV RMSE std        | 1.27                     |
| Number of features | 13                       |

### Features

```text
model_key, mileage, engine_power, fuel, paint_color, car_type,
private_parking_available, has_gps, has_air_conditioning,
automatic_car, has_getaround_connect, has_speed_regulator, winter_tires
```

---

## 🔌 API Endpoint

### POST `/predict`

```bash
curl -X POST "https://dreipfelt-getaround-api.hf.space/predict" \
-H "Content-Type: application/json" \
-d '{
  "input": [[
    "Citroën",
    50000,
    120,
    "diesel",
    "black",
    "sedan",
    1,
    1,
    1,
    0,
    1,
    1,
    0
  ]]
}'
```

Response:

```json
{
  "prediction": [124.52]
}
```

---

## 🗂️ Repository Structure

```text
Project_GetAround/  
│  
├── api/                          # FastAPI application (model serving)  
│   ├── app.py                    # API endpoints (/predict)  
│   ├── Dockerfile                # HF deployment config  
│   ├── pipeline.pkl              # Trained ML pipeline  
│   ├── feature_names.json        # Input feature order  
│   ├── model_metrics.json        # Model performance metrics  
│   └── requirements.txt  
│  
├── delay_dashboard/              # Streamlit app (delay analysis)  
│   ├── app.py
│   └── requirements.txt
│  
├── pricing_demo/                 # Streamlit app (price prediction UI)  
│   ├── app.py  
│   └── requirements.txt  
│  
├── notebooks/                    # Data exploration & model training  
│   ├── 01_EDA_delays.ipynb  
│   └── 02_ML_pricing.ipynb  
│  
├── .gitignore  
├── requirements-dev.txt  
└── README.md  
```

---

## 🛠️ Tech Stack

| Category         | Tools                 |
| ---------------- | --------------------- |
| Language         | Python 3.10           |
| Dashboard        | Streamlit, Plotly     |
| API              | FastAPI, Uvicorn      |
| Machine Learning | Scikit-learn, XGBoost |
| Deployment       | Hugging Face Spaces   |
| Version Control  | Git, GitHub           |

---

## ⚙️ Local Setup

```bash
git clone https://github.com/Data-Science-Designer-and-Developer/Project_GetAround.git
cd Project_GetAround
```

### Run API

```bash
cd api
pip install -r requirements.txt
uvicorn app:app --reload
```

### Run dashboards

```bash
cd delay_dashboard
streamlit run app.py
```

```bash
cd pricing_demo
streamlit run app.py
```

---

## 👤 Author

Frédéric Tellier
CDSD Candidate — Data Scientist
Jedha Bootcamp

Frédéric Tellier
LinkedIn: https://www.linkedin.com/in/frédéric-tellier-8a9170283/
Portfolio: https://github.com/Dreipfelt

CDSD Certification Project — Bloc 5 - Data Science Designer & Developer (RNCP35288)