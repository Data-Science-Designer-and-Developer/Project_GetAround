from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, field_validator
import joblib
import json
import numpy as np
import pandas as pd
import os

# ── Load model and feature names ─────────────────────────────────────────────
try:
    pipeline = joblib.load("pipeline.pkl")
except FileNotFoundError:
    raise RuntimeError(
        "Model file 'pipeline.pkl' not found. "
        "Make sure it is present in the working directory."
    )

try:
    with open("feature_names.json", "r") as f:
        feature_names = json.load(f)
except FileNotFoundError:
    raise RuntimeError(
        "Feature names file 'feature_names.json' not found."
    )

N_FEATURES = len(feature_names)

# ── App — Swagger UI is disabled to avoid conflict with our custom /docs ──────
app = FastAPI(
    title="GetAround Pricing API",
    description="Predicts the optimal rental price per day for a car.",
    version="1.0.0",
    docs_url="/swagger",   # Swagger UI still accessible at /swagger
    redoc_url="/redoc",
)


# ── Input schema ──────────────────────────────────────────────────────────────
class PredictInput(BaseModel):
    """
    Accepts a list of observations. Each observation must be a list of
    exactly N_FEATURES numeric values (floats or ints), in the same order
    as feature_names.json.
    """
    input: list[list[float]]

    @field_validator("input")
    @classmethod
    def check_feature_count(cls, v):
        for i, row in enumerate(v):
            if len(row) != N_FEATURES:
                raise ValueError(
                    f"Row {i} has {len(row)} features, expected {N_FEATURES}."
                )
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "input": [
                    [150000, 120, 1, 1, 1, 0, 1, 1, 0]
                ]
            }
        }
    }


# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🚗 GetAround Pricing API</h1>
            <p>API is running!</p>
            <a href="/docs">📄 Go to Documentation</a> &nbsp;|&nbsp;
            <a href="/swagger">⚙️ Swagger UI</a>
        </body>
    </html>
    """


# ── /predict ──────────────────────────────────────────────────────────────────
@app.post("/predict")
def predict(data: PredictInput):
    """
    Returns predicted rental price per day (€) for one or more cars.

    - **input**: list of observations; each observation is a list of numeric
      feature values in the order defined by feature_names.json.
    """
    X = pd.DataFrame(data.input, columns=feature_names)
    predictions = pipeline.predict(X)
    return {"prediction": [round(float(p), 2) for p in predictions]}


# ── /docs — custom HTML documentation ─────────────────────────────────────────
@app.get("/docs", response_class=HTMLResponse)
def documentation():
    # Build the feature rows dynamically from feature_names.json
    feature_rows = "\n".join(
        f"<tr><td>{i + 1}</td><td>{name}</td><td>float</td><td>—</td></tr>"
        for i, name in enumerate(feature_names)
    )

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GetAround API Documentation</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f7fa; color: #333; }}
            header {{ background: #1a1a2e; color: white; padding: 40px; text-align: center; }}
            header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
            header p {{ color: #aaa; font-size: 1.1em; }}
            .container {{ max-width: 900px; margin: 40px auto; padding: 0 20px; }}
            .endpoint {{ background: white; border-radius: 12px; padding: 30px;
                         margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
            .endpoint h2 {{ font-size: 1.4em; margin-bottom: 15px;
                            display: flex; align-items: center; gap: 12px; }}
            .badge {{ padding: 5px 14px; border-radius: 20px; font-size: 0.85em; font-weight: bold; }}
            .post {{ background: #d4edda; color: #155724; }}
            .get  {{ background: #cce5ff; color: #004085; }}
            .url  {{ background: #1a1a2e; color: #00d4aa; padding: 12px 18px;
                     border-radius: 8px; font-family: monospace; margin: 15px 0; }}
            .section-title {{ font-weight: bold; margin: 20px 0 8px; color: #555;
                               text-transform: uppercase; font-size: 0.85em; letter-spacing: 1px; }}
            pre {{ background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px;
                   padding: 15px; font-family: monospace; font-size: 0.9em; overflow-x: auto; }}
            .param-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            .param-table th {{ background: #f1f3f5; padding: 10px; text-align: left;
                                font-size: 0.85em; color: #555; }}
            .param-table td {{ padding: 10px; border-bottom: 1px solid #f1f3f5; font-size: 0.9em; }}
            .tag {{ background: #e9ecef; padding: 2px 8px; border-radius: 4px;
                    font-family: monospace; font-size: 0.85em; }}
            .note {{ margin-top: 12px; color: #666; font-size: 0.9em; font-style: italic; }}
            footer {{ text-align: center; padding: 30px; color: #aaa; font-size: 0.9em; }}
        </style>
    </head>
    <body>

    <header>
        <h1>🚗 GetAround Pricing API</h1>
        <p>Predict the optimal rental price per day for any car</p>
    </header>

    <div class="container">

        <!-- POST /predict -->
        <div class="endpoint">
            <h2><span class="badge post">POST</span>/predict</h2>
            <p>Returns predicted rental price(s) per day based on car characteristics.</p>
            <div class="url">/predict</div>

            <div class="section-title">Input</div>
            <p>JSON body with key <span class="tag">input</span> —
               a list of observations (one list per car).</p>

            <table class="param-table">
                <tr><th>#</th><th>Feature</th><th>Type</th><th>Notes</th></tr>
                {feature_rows}
            </table>

            <div class="section-title">Request example</div>
            <pre>curl -X POST "https://Dreipfelt-getaround-api.hf.space/predict" \\
     -H "Content-Type: application/json" \\
     -d '{{"input": [[150000, 120, 1, 1, 1, 0, 1, 1, 0]]}}'</pre>

            <div class="section-title">Response example</div>
            <pre>{{"prediction": [89.5]}}</pre>
        </div>

        <!-- GET / -->
        <div class="endpoint">
            <h2><span class="badge get">GET</span>/</h2>
            <p>Health check — confirms the API is running.</p>
            <div class="url">/</div>
        </div>

        <!-- GET /docs -->
        <div class="endpoint">
            <h2><span class="badge get">GET</span>/docs</h2>
            <p>This documentation page.</p>
            <div class="url">/docs</div>
        </div>

        <!-- GET /swagger -->
        <div class="endpoint">
            <h2><span class="badge get">GET</span>/swagger</h2>
            <p>Interactive Swagger UI — test the API directly in your browser.</p>
            <div class="url">/swagger</div>
        </div>

        <!-- Model info -->
        <div class="endpoint">
            <h2>🤖 Model Information</h2>
            <table class="param-table">
                <tr><th>Property</th><th>Value</th></tr>
                <tr><td>Algorithm</td><td>XGBoost Regressor (sklearn Pipeline)</td></tr>
                <tr><td>Target variable</td><td>rental_price_per_day (€)</td></tr>
                <tr><td>Number of features</td><td>{N_FEATURES}</td></tr>
                <tr><td>R²</td><td>0.68</td></tr>
                <tr><td>RMSE</td><td>XX € &nbsp;← à remplacer depuis ton notebook</td></tr>
            </table>
            <p class="note">
                Model trained on the GetAround pricing dataset. Features include mileage,
                engine power, fuel type, car type, colour, and available options.
                The pipeline includes preprocessing (scaling + encoding) and the regressor.
            </p>
        </div>

        <!-- RGPD -->
        <div class="endpoint">
            <h2>🔒 Data & Privacy (RGPD)</h2>
            <p>This API processes only technical car characteristics (mileage, engine power,
               equipment options). No personal data (name, email, location) is collected
               or stored. Input data is used solely for real-time inference and is not
               persisted after the response is returned. The service is hosted on
               Hugging Face Spaces (EU infrastructure). It is therefore compliant with
               the GDPR / RGPD framework.</p>
        </div>

    </div>
    <footer>GetAround Pricing API — Built with FastAPI 🚀</footer>
    </body>
    </html>
    """
