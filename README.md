🚗 Getaround — Delay Analysis & Pricing Prediction

Certification CDSD — Data Science & Deployment Project

📌 Project Overview

Getaround is a peer-to-peer car rental platform where late vehicle returns can create strong friction for subsequent rentals.
This project addresses two strategic challenges:

Operational optimization — evaluating the impact of introducing a minimum delay between rentals to reduce late checkout conflicts.

Pricing optimization — exposing a Machine Learning model through an online API to help owners set optimal rental prices.

The project combines data analysis, interactive dashboards, machine learning, and API deployment.

🎯 Business Objectives
Delay Management

Measure how often drivers return cars late.

Quantify the impact on subsequent rentals.

Simulate different minimum delay thresholds.

Help Product Management choose:

an optimal delay threshold

an appropriate scope (all cars vs Connect only).

Pricing Optimization

Serve a trained Machine Learning model via an online API.

Allow real-time price prediction through a /predict endpoint.

Provide a simple UI to interact with the model.

🧱 Project Structure
Project_GetAround/  
│
├── dashboards/  
│   ├── app_delay.py            # Streamlit dashboard — Delay analysis  
│   └── app_pricing.py          # Streamlit dashboard — Pricing prediction  
│
├── api/  
│   ├── main.py                 # FastAPI app  
│   ├── model.pkl               # Trained ML model  
│   └── requirements.txt  
│
├── notebooks/  
│   ├── 01_delay_analysis.ipynb  
│   └── 02_pricing_model.ipynb  
│
├── README.md  
└── requirements.txt  

📊 Dashboard 1 — Delay Analysis
Purpose

Help Product Managers evaluate the trade-off between:

reducing late checkout conflicts

preserving rental revenue

Features

Threshold selection (0–180 minutes)

Scope selection (check-in types)

Key KPIs:

% of late checkouts

number of impacted rentals

Delay distribution visualization

Business impact summary

Technology

Streamlit

Pandas

Plotly

Run locally
streamlit run dashboards/app_delay.py

💰 Dashboard 2 — Pricing Prediction
Purpose

Provide an interface to interact with the pricing prediction API.

Features

Manual input of 11 numerical features

API call to /predict

Real-time price prediction display

Input validation and error handling

Run locally
streamlit run dashboards/app_pricing.py

🤖 Machine Learning API
Endpoint: /predict

Method: POST

Input:

{
  "input": [[7.0, 0.27, 0.36, 20.7, 0.045, 45.0, 170.0, 1.001, 3.0, 0.45, 8.8]]
}


Output:

{
  "prediction": [6]
}

Documentation

A full API documentation is available at:

/docs

🌐 Deployment

API: Hosted on Hugging Face Spaces

Dashboards: Run locally or deployable via Streamlit Cloud / Hugging Face

Example API URL
https://<username>-<space-name>.hf.space/predict

🛠️ Installation
git clone https://github.com/<your-username>/Project_GetAround.git  
cd Project_GetAround  
python -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  

🧠 Key Takeaways

Data-driven product decision support

Clear separation between analysis, ML, and deployment

Robust handling of user inputs and API failures

Production-oriented mindset aligned with CDSD expectations

👤 Author

Frédéric
CDSD Candidate — Data Scientist
Project completed as part of the Jedha CDSD certification.
