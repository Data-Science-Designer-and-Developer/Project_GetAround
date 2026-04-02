import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

st.set_page_config(
    page_title="GetAround Dashboard",
    page_icon="🚗",
    layout="wide"
)

DELAY_DATA_URL = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx"
PRICING_DATA_URL = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv"
API_URL = "https://dreipfelt-getaround-api.hf.space/predict"


@st.cache_data
def load_delay_data():
    return pd.read_excel(DELAY_DATA_URL)


@st.cache_data
def load_pricing_reference_data():
    df = pd.read_csv(PRICING_DATA_URL)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
    return df


df = load_delay_data()
df_pricing = load_pricing_reference_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/GetAround_logo.svg/1200px-GetAround_logo.svg.png",
    width=200,
)
st.sidebar.title("⚙️ Settings")

scope = st.sidebar.radio(
    "Feature scope",
    options=["All vehicles", "Connect only", "Mobile only"],
    index=0,
)
threshold = st.sidebar.slider(
    "Minimum time between 2 rentals (minutes)",
    min_value=0,
    max_value=720,
    value=60,
    step=15,
    key="threshold_slider",
)

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Reading guide**")
st.sidebar.markdown("Adjust the scope and threshold to see the real-time impact.")

# ── Filter data by scope ──────────────────────────────────────────────────────
if scope == "Connect only":
    df_filtered = df[df["checkin_type"] == "connect"].copy()
elif scope == "Mobile only":
    df_filtered = df[df["checkin_type"] == "mobile"].copy()
else:
    df_filtered = df.copy()

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.title("🚗 GetAround — Analysis of checkout delays")
st.markdown(
    "**Objective:** Help the Product Manager decide on the threshold and scope "
    "of the minimum delay feature."
)
st.markdown("---")

total_rentals = len(df_filtered)
late_mask = df_filtered["delay_at_checkout_in_minutes"] > 0
total_late = int(late_mask.sum())

n_with_delay_info = int(df_filtered["delay_at_checkout_in_minutes"].notna().sum())
pct_late = (total_late / n_with_delay_info * 100) if n_with_delay_info > 0 else 0.0

if total_rentals > 0:
    blocked = df_filtered[
        df_filtered["time_delta_with_previous_rental_in_minutes"] < threshold
    ]
    pct_blocked = len(blocked) / total_rentals * 100
else:
    blocked = df_filtered.iloc[0:0]
    pct_blocked = 0.0

median_delay = (
    df_filtered.loc[late_mask, "delay_at_checkout_in_minutes"].median()
    if late_mask.any()
    else 0.0
)

col1, col2, col3, col4 = st.columns(4)
col1.metric(label="📦 Total rentals", value=f"{total_rentals:,}")
col2.metric(
    label="⏰ Late returns",
    value=f"{total_late:,}",
    delta=f"{pct_late:.1f}% of known delays",
    delta_color="inverse",
)
col3.metric(label="⏱️ Median delay", value=f"{median_delay:.0f} min")
col4.metric(
    label="🚫 Blocked rentals",
    value=f"{len(blocked):,}",
    delta=f"{pct_blocked:.1f}% of total",
    delta_color="inverse",
)

# ── Delay analysis ────────────────────────────────────────────────────────────
st.markdown("---")
st.header("📊 Analysis of delays")

col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Distribution of delays")
    late_data = df_filtered.loc[
        df_filtered["delay_at_checkout_in_minutes"] > 0,
        "delay_at_checkout_in_minutes",
    ].dropna()

    late_data_capped = late_data[late_data <= 720]

    fig1 = px.histogram(
        late_data_capped,
        nbins=40,
        color_discrete_sequence=["#FF6B6B"],
        labels={"value": "Delay (minutes)", "count": "Number of rentals"},
    )

    if not late_data.empty:
        median_val = late_data.median()
        fig1.add_vline(
            x=median_val,
            line_color="red",
            line_width=2
        )
        fig1.add_annotation(
            x=median_val,
            y=1.08,
            xref="x",
            yref="paper",
            text=f"Median: {median_val:.0f} min",
            showarrow=False,
            font=dict(color="red", size=12),
            bgcolor="rgba(255,255,255,0.85)"
        )

    fig1.add_vline(
        x=threshold,
        line_color="#1a6fd4",
        line_dash="dash",
        line_width=2
    )
    fig1.add_annotation(
        x=threshold,
        y=1.16,
        xref="x",
        yref="paper",
        text=f"Threshold: {threshold} min",
        showarrow=False,
        font=dict(color="#1a6fd4", size=12),
        bgcolor="rgba(255,255,255,0.85)"
    )

    fig1.update_layout(
        showlegend=False,
        height=350,
        margin=dict(t=90)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.subheader("Delays: Connect vs Mobile")

    compare = (
        df.groupby("checkin_type")
        .apply(
            lambda x: pd.Series(
                {
                    "Total": len(x),
                    "Late": int((x["delay_at_checkout_in_minutes"] > 0).sum()),
                    "Late %": (
                        (x["delay_at_checkout_in_minutes"] > 0).sum()
                        / x["delay_at_checkout_in_minutes"].notna().sum()
                        * 100
                    )
                    if x["delay_at_checkout_in_minutes"].notna().sum() > 0
                    else 0,
                }
            )
        )
        .reset_index()
    )

    fig2 = px.bar(
        compare,
        x="checkin_type",
        y="Late %",
        color="checkin_type",
        color_discrete_map={"connect": "#4ECDC4", "mobile": "#FF6B6B"},
        labels={"checkin_type": "Check-in type", "Late %": "% late"},
        text="Late %",
    )

    max_late_pct = compare["Late %"].max() if not compare.empty else 0

    fig2.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False
    )
    fig2.update_layout(
        showlegend=False,
        height=350,
        yaxis=dict(range=[0, max(10, max_late_pct * 1.25)], title="% late"),
        margin=dict(t=50)
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Threshold simulation ──────────────────────────────────────────────────────
st.markdown("---")
st.header("🎯 Impact of the chosen threshold")

thresholds_range = list(range(0, 721, 15))

df_with_prev = df_filtered[df_filtered["previous_ended_rental_id"].notna()].copy()
df_prev_info = df[["rental_id", "delay_at_checkout_in_minutes"]].rename(
    columns={
        "rental_id": "previous_ended_rental_id",
        "delay_at_checkout_in_minutes": "prev_delay",
    }
)
df_merged = df_with_prev.merge(df_prev_info, on="previous_ended_rental_id", how="left")
df_merged["was_impacted"] = (
    df_merged["prev_delay"] > df_merged["time_delta_with_previous_rental_in_minutes"]
)
total_problems = int(df_merged["was_impacted"].sum())

sim_results = []
for t in thresholds_range:
    blocked_count = int(
        (df_filtered["time_delta_with_previous_rental_in_minutes"] < t).sum()
    )
    solved_count = int(
        (
            (df_merged["was_impacted"])
            & (df_merged["time_delta_with_previous_rental_in_minutes"] < t)
        ).sum()
    )
    sim_results.append(
        {
            "Threshold (min)": t,
            "Blocked rentals": blocked_count,
            "% blocked": blocked_count / total_rentals * 100 if total_rentals > 0 else 0,
            "Problems solved": solved_count,
            "% problems solved": (
                solved_count / total_problems * 100 if total_problems > 0 else 0
            ),
        }
    )

df_sim = pd.DataFrame(sim_results)

fig3 = go.Figure()
fig3.add_trace(
    go.Scatter(
        x=df_sim["Threshold (min)"],
        y=df_sim["% blocked"],
        name="% blocked rentals (cost)",
        line=dict(color="#FF6B6B", width=2),
        fill="tozeroy",
        fillcolor="rgba(255,107,107,0.1)",
    )
)
fig3.add_trace(
    go.Scatter(
        x=df_sim["Threshold (min)"],
        y=df_sim["% problems solved"],
        name="% problems solved (benefit)",
        line=dict(color="#4ECDC4", width=2),
        fill="tozeroy",
        fillcolor="rgba(78,205,196,0.1)",
    )
)
fig3.add_vline(
    x=threshold,
    line_color="#FFE66D",
    line_width=3,
    line_dash="dash",
    annotation_text=f"Current threshold: {threshold} min",
)
fig3.update_layout(
    title="Trade-off: Blocked Rentals vs. Resolved Issues",
    xaxis_title="Threshold (minutes)",
    yaxis_title="Percentage (%)",
    hovermode="x unified",
    height=400,
)
st.plotly_chart(fig3, use_container_width=True)

current_rows = df_sim[df_sim["Threshold (min)"] == threshold]
if current_rows.empty:
    current_rows = df_sim.iloc[[(df_sim["Threshold (min)"] - threshold).abs().argmin()]]
current = current_rows.iloc[0]

st.info(
    f"""
**📊 For a threshold of {threshold} minutes:**
- 🚫 Blocked rentals: **{current['Blocked rentals']:.0f}** ({current['% blocked']:.1f}%)
- ✅ Problems resolved: **{current['Problems solved']:.0f}** ({current['% problems solved']:.1f}% of problematic cases)
"""
)

# ── Revenue impact ────────────────────────────────────────────────────────────
st.markdown("---")
st.header("💰 Impact on revenue")

col_r1, col_r2 = st.columns(2)

with col_r1:
    st.subheader("Blocked rentals by scope and threshold")
    scope_results = []
    for scope_type in ["connect", "mobile"]:
        df_scope = df[df["checkin_type"] == scope_type]
        n_scope = len(df_scope)
        for t in [30, 60, 120, 180, 240]:
            blocked_rev = int(
                (df_scope["time_delta_with_previous_rental_in_minutes"] < t).sum()
            )
            scope_results.append(
                {
                    "Scope": scope_type,
                    "Threshold": f"{t}min",
                    "Blocked": blocked_rev,
                    "% blocked": blocked_rev / n_scope * 100 if n_scope > 0 else 0,
                }
            )
    df_scope_results = pd.DataFrame(scope_results)
    fig4 = px.bar(
        df_scope_results,
        x="Threshold",
        y="% blocked",
        color="Scope",
        barmode="group",
        color_discrete_map={"connect": "#4ECDC4", "mobile": "#FF6B6B"},
    )
    fig4.update_layout(height=350)
    st.plotly_chart(fig4, use_container_width=True)

with col_r2:
    st.subheader("Connect vs Mobile Distribution")
    type_counts = df["checkin_type"].value_counts()
    fig5 = px.pie(
        values=type_counts.values,
        names=type_counts.index,
        color_discrete_map={"connect": "#4ECDC4", "mobile": "#FF6B6B"},
    )
    fig5.update_layout(height=350)
    st.plotly_chart(fig5, use_container_width=True)

# ── Raw data ──────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("🔍 View raw data"):
    st.dataframe(df_filtered.head(100))
    st.caption(f"Showing first 100 rows out of {len(df_filtered)} total")

# ── Price prediction ──────────────────────────────────────────────────────────
st.markdown("---")
st.header("💰 Optimal Price — Prediction")
st.markdown(
    "Enter the car characteristics below to get a suggested daily rental price."
)

model_options = sorted(df_pricing["model_key"].dropna().astype(str).unique().tolist())
fuel_options = sorted(df_pricing["fuel"].dropna().astype(str).unique().tolist())
paint_options = sorted(df_pricing["paint_color"].dropna().astype(str).unique().tolist())
car_type_options = sorted(df_pricing["car_type"].dropna().astype(str).unique().tolist())

col_p0, col_p1, col_p2 = st.columns(3)

with col_p0:
    model_key = st.selectbox("Vehicle brand / model", model_options)
    fuel = st.selectbox("Fuel", fuel_options)
    paint_color = st.selectbox("Paint colour", paint_options)

with col_p1:
    car_type = st.selectbox("Car type", car_type_options)
    mileage = st.number_input("Mileage (km)", min_value=0, value=50000, step=1000)
    engine_power = st.number_input("Engine power (hp)", min_value=0, value=120, step=10)

with col_p2:
    private_parking_available = st.checkbox("Private parking available", value=True)
    has_gps = st.checkbox("GPS", value=True)
    has_air_conditioning = st.checkbox("Air conditioning", value=True)
    automatic_car = st.checkbox("Automatic gearbox", value=False)
    has_getaround_connect = st.checkbox("GetAround Connect", value=True)
    has_speed_regulator = st.checkbox("Speed regulator", value=True)
    winter_tires = st.checkbox("Winter tires", value=False)

if st.button("🔮 Predict price"):
    features = [[
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
        int(winter_tires),
    ]]

    try:
        response = requests.post(
            API_URL,
            json={"input": features},
            timeout=10,
        )
        response.raise_for_status()
        price = response.json()["prediction"][0]
        st.success(f"💶 Suggested price: **{price:.2f} €/day**")
    except requests.exceptions.Timeout:
        st.error("⏱️ The API did not respond in time. Please try again.")
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ API error: {e}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")