import streamlit as st
import requests

st.set_page_config(page_title="GetAround Pricing Demo", page_icon="💰")

st.title("💰 GetAround — Price Prediction Demo")

# =========================
# INPUTS
# =========================

st.header("Vehicle characteristics")

col1, col2 = st.columns(2)

with col1:
    model_key = st.selectbox(
    "Vehicle brand / model",
    ["Citroën", "Peugeot", "BMW", "Renault", "Audi", "Nissan", "Mitsubishi", "Mercedes", "Volkswagen", "Toyota", "SEAT", "Subaru", "Opel", "Ferrari", "Porsche"]
)
    mileage = st.number_input("Mileage (km)", 0, 300000, 50000)
    engine_power = st.number_input("Engine power (hp)", 0, 300, 120)

with col2:
    fuel = st.selectbox("Fuel", ["diesel", "petrol", "hybrid", "electric"])
    paint_color = st.selectbox("Color", ["black", "white", "grey", "blue", "red"])
    car_type = st.selectbox("Car type", ["sedan", "SUV", "convertible", "coupe"])

st.header("Equipment")

col3, col4 = st.columns(2)

with col3:
    private_parking_available = st.checkbox("Private parking")
    has_gps = st.checkbox("GPS")
    has_air_conditioning = st.checkbox("Air conditioning")

with col4:
    automatic_car = st.checkbox("Automatic car")
    has_getaround_connect = st.checkbox("Getaround Connect")
    has_speed_regulator = st.checkbox("Speed regulator")
    winter_tires = st.checkbox("Winter tires")

# =========================
# API CALL
# =========================

API_URL = "https://Dreipfelt-getaround-api.hf.space/predict"

if st.button("Predict price"):

    payload = {
        "input": [[
            model_key,
            mileage,
            engine_power,
            fuel,
            paint_color,
            car_type,
            int(private_parking_available),
            int(has_gps),
            int(has_air_conditioning),
            int(automatic_car),
            int(has_getaround_connect),
            int(has_speed_regulator),
            int(winter_tires)
        ]]
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            prediction = response.json()["prediction"][0]
            st.success(f"💶 Estimated price: {prediction} €/day")
        else:
            st.error(f"API error: {response.status_code}")

    except Exception as e:
        st.error(f"Connection error: {e}")