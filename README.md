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

## 📅 Project Timeline

| Stage                   | Description                                           | Estimated Duration |
| ----------------------- | ----------------------------------------------------- | ------------------ |
| 1. Data Exploration     | EDA on delays and pricing                             | ~3h                |
| 2. Business Analysis    | Threshold simulations, revenue impact, visualisations | ~3h                |
| 3. Dashboard            | Streamlit development and deployment                  | ~3h                |
| 4. Machine Learning     | Feature engineering, XGBoost training and evaluation  | ~5h                |
| 5. FastAPI API          | Development of the /predict endpoint, Dockerfile      | ~3h                |
| 6. HF Spaces Deployment | Configuration, testing, production release            | ~2h                |
| **Total**               |                                                       | **~19h**           |


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
## 📈 Business Recommendation

### 1. Delay Management Strategy

The analysis highlights a clear trade-off between **operational efficiency** and **customer experience**:

* Increasing the minimum buffer between rentals reduces conflicts
* However, it also increases the number of **blocked bookings (lost revenue)**

👉 **Recommendation:**

* Set a **default buffer around 60–90 minutes**
* This range provides a strong balance:

  * significant reduction in conflicts
  * limited impact on booking volume

👉 **Scope recommendation:**

* Apply stricter thresholds to **Connect vehicles**
* Keep more flexibility for **Mobile check-ins**

**Why:**
Connect vehicles show more predictable behaviour, making stricter rules more effective with lower operational risk.

---

### 2. Pricing Strategy

The Machine Learning model enables **data-driven pricing decisions**:

* Price is strongly influenced by:

  * vehicle type
  * engine power
  * equipment (GPS, AC, etc.)
* Significant price variability exists for similar vehicles

👉 **Recommendation:**

* Use the model as a **price recommendation tool for owners**
* Integrate it directly into the platform to:

  * standardise pricing
  * reduce underpricing / overpricing
  * improve marketplace consistency

---

### 3. Product Impact

By combining both solutions, GetAround can:

* Reduce customer friction and cancellations
* Improve fleet utilisation
* Increase owner revenue through better pricing
* Enable **data-driven product decisions**

---

### 4. Next Steps

To maximise impact, the following improvements are recommended:

* Introduce **dynamic buffer thresholds** (adaptive to context: location, demand, vehicle type)
* Monitor **A/B test performance** of different delay strategies
* Continuously retrain the pricing model with fresh data
* Integrate both tools into a unified internal product dashboard

---

### 5. Key Takeaway

This project demonstrates how combining **product analytics** and **machine learning** can directly support strategic decisions and improve both **user experience** and **business performance**.

## 🎯 Executive Summary

GetAround is losing customers due to late returns between consecutive bookings. This project addresses two concrete product questions:

What minimum buffer time should be enforced between two bookings to reduce conflicts without significantly impacting revenue? → Analysis of 2017 data shows that a 60 to 90-minute buffer significantly reduces problematic cases while limiting the impact on revenue.
How can owners optimise their listed prices? → An XGBoost model (R² = 0.74) predicts the optimal daily price based on vehicle characteristics, with a median error of approximately €10 per day.

Both tools are deployed in production and accessible via the links below.

## 🔒 GDPR Compliance

This project is carried out in an educational context using datasets provided by GetAround to Jedha Bootcamp.

**Nature of the data:** The datasets used (`get_around_delay_analysis.xlsx`, `get_around_pricing_project.csv`) are **pseudonymised**: no names, email addresses, phone numbers, or direct identifiers of drivers or owners are included. Rental identifiers (`rental_id`, `car_id`) are technical keys with no link to identifiable individuals.

**Legal basis for processing:** Internal analysis for service improvement purposes (legitimate interest — Art. 6(1)(f) GDPR). The data is not collected במסגרת this project but reused for analytical purposes.

**Storage:** The deployed API does not store any data transmitted through `/predict` requests. No personal data is retained on the server side.

**Data subject rights:** GetAround users have rights of access, rectification, and erasure directly with GetAround (the data controller). This project does not act as a data controller.


## 👤 Author

Frédéric Tellier  
CDSD Candidate — Data Scientist  
Jedha Bootcamp  

LinkedIn: https://www.linkedin.com/in/frédéric-tellier-8a9170283/  
Portfolio: https://github.com/Dreipfelt  

CDSD Certification Project — Bloc 5 - Data Science Designer & Developer (RNCP35288)  