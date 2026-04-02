import os
import json
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict

# =========================================================
# Paths
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PIPELINE_PATH = os.path.join(BASE_DIR, "pipeline.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "feature_names.json")
METRICS_PATH = os.path.join(BASE_DIR, "model_metrics.json")

# =========================================================
# Load artefacts
# =========================================================
pipeline = joblib.load(PIPELINE_PATH)

with open(FEATURES_PATH, "r", encoding="utf-8") as f:
    feature_names = json.load(f)

if os.path.exists(METRICS_PATH):
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        model_metrics = json.load(f)
else:
    model_metrics = {}

# =========================================================
# FastAPI app
# =========================================================
app = FastAPI(
    title="GetAround Pricing API",
    description="Predicts the optimal rental price per day for a car",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# =========================================================
# Input schema
# =========================================================
class PredictInput(BaseModel):
    input: list[list]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
            }
        }
    )

# =========================================================
# Helpers
# =========================================================
def metric_value(name: str, digits: int = 2) -> str:
    value = model_metrics.get(name)
    if value is None:
        return "N/A"
    try:
        return f"{float(value):.{digits}f}"
    except Exception:
        return "N/A"


def get_model_name() -> str:
    try:
        return pipeline.named_steps["model"].__class__.__name__
    except Exception:
        return "Unknown"


# =========================================================
# Routes
# =========================================================
@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h1>🚗 GetAround Pricing API</h1>
            <p>API is running.</p>
            <a href="/docs">📄 Go to Documentation</a>
        </body>
    </html>
    """


@app.post("/predict")
def predict(data: PredictInput):
    X = pd.DataFrame(data.input, columns=feature_names)
    predictions = pipeline.predict(X)
    return {"prediction": [round(float(p), 2) for p in predictions]}


@app.get("/docs", response_class=HTMLResponse)
def documentation():
    algo_name = get_model_name()

    rmse = metric_value("RMSE")
    mae = metric_value("MAE")
    r2 = metric_value("R²", 3)
    cv_rmse = metric_value("CV_RMSE_mean")
    cv_std = metric_value("CV_RMSE_std")

    feature_rows = "".join([
        f"<tr><td>{i+1}</td><td>{feature}</td></tr>"
        for i, feature in enumerate(feature_names)
    ])

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GetAround Pricing API Documentation</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f5f7fa; color: #333; }}
            header {{ background: #1a1a2e; color: white; padding: 40px; text-align: center; }}
            header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
            header p {{ color: #ccc; font-size: 1.05em; }}
            .container {{ max-width: 900px; margin: 40px auto; padding: 0 20px; }}
            .endpoint {{ background: white; border-radius: 12px; padding: 30px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
            .endpoint h2 {{ font-size: 1.4em; margin-bottom: 15px; display: flex; align-items: center; gap: 12px; }}
            .badge {{ padding: 5px 14px; border-radius: 20px; font-size: 0.85em; font-weight: bold; }}
            .post {{ background: #d4edda; color: #155724; }}
            .get  {{ background: #cce5ff; color: #004085; }}
            .url  {{ background: #1a1a2e; color: #00d4aa; padding: 12px 18px; border-radius: 8px; font-family: monospace; margin: 15px 0; }}
            .section-title {{ font-weight: bold; margin: 20px 0 8px; color: #555; text-transform: uppercase; font-size: 0.85em; letter-spacing: 1px; }}
            pre {{ background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 15px; font-family: monospace; font-size: 0.9em; overflow-x: auto; }}
            .param-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            .param-table th {{ background: #f1f3f5; padding: 10px; text-align: left; font-size: 0.85em; color: #555; }}
            .param-table td {{ padding: 10px; border-bottom: 1px solid #f1f3f5; font-size: 0.9em; }}
            footer {{ text-align: center; padding: 30px; color: #888; font-size: 0.9em; }}
        </style>
    </head>
    <body>

    <header>
        <h1>🚗 GetAround Pricing API</h1>
        <p>Predict the optimal rental price per day for a car</p>
    </header>

    <div class="container">

        <div class="endpoint">
            <h2><span class="badge post">POST</span>/predict</h2>
            <p>Returns a predicted rental price per day based on the car's characteristics.</p>
            <div class="url">/predict</div>

            <div class="section-title">Expected input features</div>
            <table class="param-table">
                <tr><th>#</th><th>Feature</th></tr>
                {feature_rows}
            </table>

            <div class="section-title">Request example</div>
            <pre>{{
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
}}</pre>

            <div class="section-title">Response example</div>
            <pre>{{
  "prediction": [124.52]
}}</pre>
        </div>

        <div class="endpoint">
            <h2><span class="badge get">GET</span>/</h2>
            <p>Health check endpoint.</p>
            <div class="url">/</div>
        </div>

        <div class="endpoint">
            <h2><span class="badge get">GET</span>/docs</h2>
            <p>Custom API documentation page.</p>
            <div class="url">/docs</div>
        </div>

        <div class="endpoint">
            <h2>🤖 Model Information</h2>
            <table class="param-table">
                <tr><th>Property</th><th>Value</th></tr>
                <tr><td>Algorithm</td><td>{algo_name}</td></tr>
                <tr><td>Target</td><td>rental_price_per_day (€)</td></tr>
                <tr><td>RMSE</td><td>{rmse}</td></tr>
                <tr><td>MAE</td><td>{mae}</td></tr>
                <tr><td>R²</td><td>{r2}</td></tr>
                <tr><td>CV RMSE</td><td>{cv_rmse}</td></tr>
                <tr><td>CV RMSE std</td><td>{cv_std}</td></tr>
                <tr><td>Number of features</td><td>{len(feature_names)}</td></tr>
            </table>
        </div>

    </div>

    <footer>GetAround Pricing API — Built with FastAPI</footer>
    </body>
    </html>
    """