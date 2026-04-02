🚗 GetAround — Delay Analysis & Pricing Prediction

📌 Project Overview

GetAround is a peer-to-peer car rental platform. Late vehicle returns create friction for subsequent rentals, leading to customer dissatisfaction and cancellations.

This project addresses two strategic challenges:

    Operational optimization — Analyzing late checkouts and simulating minimum delay thresholds to reduce conflicts between consecutive rentals.
    Pricing optimization — Serving a Machine Learning model via a production API to help owners set optimal daily rental prices.

🔗 Live Applications
Service	URL
📊 Delay Dashboard	https://huggingface.co/spaces/Dreipfelt/getaround-dashboard
💰 Pricing Demo	https://huggingface.co/spaces/Dreipfelt/Getaround-Pricing
🔌 API	https://dreipfelt-getaround-api.hf.space
📄 API Docs	https://dreipfelt-getaround-api.hf.space/docs
💻 GitHub	https://github.com/Data-Science-Designer-and-Developer/Project_GetAround

🎯 Business Objectives
1. Delay Management
Measure how often vehicles are returned late
Quantify impact on subsequent rentals
Simulate minimum delay thresholds (0 → 720 minutes)
Help Product team decide:
optimal buffer time
feature scope (all vehicles vs Connect only)
2. Pricing Optimisation
Train a regression model on vehicle characteristics
Serve predictions via REST API
Enable real-time pricing recommendations

🏗️ Architecture
                ┌────────────────────┐
                │  Delay Dashboard   │
                │   (Streamlit)      │
                └────────┬───────────┘
                         │
                         │
                ┌────────▼───────────┐
                │   Pricing Demo     │
                │   (Streamlit)      │
                └────────┬───────────┘
                         │ HTTP
                         ▼
                ┌────────────────────┐
                │   FastAPI API      │
                │   /predict         │
                └────────┬───────────┘
                         │
                         ▼
                ┌────────────────────┐
                │ ML Pipeline        │
                │ (Preprocessing +   │
                │  XGBoost model)    │
                └────────────────────┘

📊 Delay Dashboard

Interactive tool for Product Managers:

Visualise delay distributions
Compare Connect vs Mobile
Simulate trade-offs:
% blocked rentals (cost)
% problems solved (benefit)
Adjust threshold in real time

💰 Pricing Demo

User-facing interface to:

Select vehicle characteristics
Call the API /predict endpoint
Display estimated rental price

🤖 Machine Learning API
Model
Property	Value
Algorithm	XGBoost Regressor
Target	rental_price_per_day (€)
RMSE	16.60
MAE	10.50
R²	0.738
Features	13
Features
model_key, mileage, engine_power, fuel, paint_color, car_type,
private_parking_available, has_gps, has_air_conditioning,
automatic_car, has_getaround_connect, has_speed_regulator, winter_tires

🔌 API Endpoint
POST /predict
Example request
curl -X POST "https://dreipfelt-getaround-api.hf.space/predict" \
-H "Content-Type: application/json" \
-d '{
  "input": [[
    "Citroën",
    50000,
    120,GetAround is a peer-to-peer car rental platform. Late vehicle returns create friction for subsequent rentals, leading to customer dissatisfaction and cancellations.

This project addresses two strategic challenges:

    Operational optimization — Analyzing late checkouts and simulating minimum delay thresholds to reduce conflicts between consecutive rentals.
    Pricing optimization — Serving a Machine Learning model via a production API to help owners set optimal daily rental prices.

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
Example response
{
  "prediction": [124.52]
}

🗂️ Repository Structure
Project_GetAround/
├── api/                    # FastAPI application
│   ├── app.py
│   ├── pipeline.pkl
│   ├── feature_names.json
│   ├── model_metrics.json
│   └── requirements.txt
│
├── delay_dashboard/        # Delay analysis app
│   ├── app.py
│   └── requirements.txt
│
├── pricing_demo/           # Pricing demo app
│   ├── app.py
│   └── requirements.txt
│
├── notebooks/
│   ├── 01_EDA_delays.ipynb
│   └── 02_ML_pricing.ipynb
│
├── .gitignore
├── requirements-dev.txt
└── README.md

🛠️ Tech Stack
Category	Tools
Language	Python 3.10
Dashboard	Streamlit, Plotly
API	FastAPI, Uvicorn
ML	Scikit-learn, XGBoost
Deployment	Hugging Face Spaces
Version Control	Git, GitHub

⚙️ Local Setup
1. Clone the repo
git clone https://github.com/Data-Science-Designer-and-Developer/Project_GetAround.git
cd Project_GetAround
2. Run API
cd api
pip install -r requirements.txt
uvicorn app:app --reload

→ http://localhost:8000

3. Run Delay Dashboard
cd delay_dashboard
pip install -r requirements.txt
streamlit run app.py
4. Run Pricing Demo
cd pricing_demo
pip install -r requirements.txt
streamlit run app.py

🚀 Key Takeaways
Strong trade-off between operational constraints and customer experience
Machine Learning enables real-time pricing decisions
End-to-end pipeline:
Data → Model → API → Product interface

👤 Author
Frédéric
LinkedIn: https://www.linkedin.com/in/fr%C3%A9d%C3%A9ric-tellier-8a 
GitHub: https://github.com/Dreipfelt
CDSD Candidate — Data Scientist
Jedha Bootcamp