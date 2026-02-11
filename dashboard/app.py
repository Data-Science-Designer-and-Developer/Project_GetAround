import pandas as pd
import streamlit as st
import plotly.express as px

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="GetAround Delay Analysis", layout="wide")

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    url = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"
    return pd.read_excel(url, engine="openpyxl")

df = load_data()

st.title("🚗 GetAround — Delay Analysis Dashboard")

# -----------------------------
# Controls
# -----------------------------
threshold = st.slider("Delay threshold (minutes)", 0, 180, 30, step=15)

scopes = st.multiselect(
    "Scope (checkin type)",
    options=df["checkin_type"].dropna().unique(),
    default=df["checkin_type"].dropna().unique()
)

df = df[df["checkin_type"].isin(scopes)]

# -----------------------------
# Feature engineering
# -----------------------------
df["late"] = df["delay_at_checkout_in_minutes"] > threshold
df["problem"] = df["delay_at_checkout_in_minutes"] > 0
df["solved"] = (
    (df["delay_at_checkout_in_minutes"] > 0) &
    (df["delay_at_checkout_in_minutes"] <= threshold)
)

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total rentals", len(df))
col2.metric("Late rentals (%)", f"{df['late'].mean()*100:.1f}%")
col3.metric("Problems solved (%)",
            f"{df['solved'].sum()/df['problem'].sum()*100:.1f}%")

# -----------------------------
# Distribution of delays
# -----------------------------
st.subheader("Distribution of checkout delays")
fig = px.histogram(
    df,
    x="delay_at_checkout_in_minutes",
    nbins=60,
    labels={"delay_at_checkout_in_minutes": "Delay (minutes)"}
)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Impact on next driver
# -----------------------------
st.subheader("Impact on next driver")

df_pairs = df.merge(
    df,
    left_on="rental_id",
    right_on="previous_ended_rental_id",
    suffixes=("_prev", "_next")
)

df_pairs["impact"] = df_pairs["delay_at_checkout_in_minutes_prev"] > 0

col1, col2, col3 = st.columns(3)
col1.metric("Rentals impacting next",
            df_pairs["impact"].sum())
col2.metric("Impact rate (%)",
            f"{df_pairs['impact'].mean()*100:.1f}%")
col3.metric("Avg delay suffered (min)",
            f"{df_pairs[df_pairs['impact']]['delay_at_checkout_in_minutes_prev'].mean():.1f}")

# -----------------------------
# Revenue impact (hypothesis)
# -----------------------------
st.subheader("Revenue impact (estimation)")

AVG_PRICE_PER_DAY = 50  # hypothesis documented
lost_revenue = df["late"].sum() * AVG_PRICE_PER_DAY
total_revenue = len(df) * AVG_PRICE_PER_DAY

st.metric(
    "Share of owner revenue affected (%)",
    f"{lost_revenue / total_revenue * 100:.1f}%"
)

st.caption(
    "Hypothesis: each blocked rental equals one rental day lost "
    f"({AVG_PRICE_PER_DAY}€/day)."
)
