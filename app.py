import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Seashells Intelligence System", layout="wide")

# --------------------------
# HEADER
# --------------------------
st.title("🌊 Seashells Logistics Pvt Ltd")
st.subheader("📊 AI-Powered Delivery Intelligence System")

# --------------------------
# FILE UPLOAD + VALIDATION
# --------------------------
st.sidebar.header("📁 Upload Data")

required_cols = ["Date", "City", "Courier", "Segment", "Orders", "On-Time %", "RTO %", "Complaints %"]

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

def validate_data(df):
    missing = [col for col in required_cols if col not in df.columns]
    return missing

def load_sample():
    return pd.DataFrame({
        "Date": pd.date_range(start="2023-10-01", periods=50),
        "City": np.random.choice(["Mumbai","Pune","Indore","Nagpur"],50),
        "Courier": np.random.choice(["QuickShip","ShipNow","FastEx"],50),
        "Segment": np.random.choice(["New","Repeat","High Value"],50),
        "Orders": np.random.randint(500,2000,50),
        "On-Time %": np.random.randint(50,90,50),
        "RTO %": np.random.randint(5,25,50),
        "Complaints %": np.random.randint(10,35,50)
    })

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    missing_cols = validate_data(df)

    if missing_cols:
        st.error(f"Missing columns: {missing_cols}")
        st.stop()
    df["Date"] = pd.to_datetime(df["Date"])
else:
    df = load_sample()

# --------------------------
# SESSION STATE FILTERS
# --------------------------
st.sidebar.header("🔎 Filters")

date_range = st.sidebar.date_input("Date Range",
                                  [df["Date"].min(), df["Date"].max()])

courier = st.sidebar.multiselect("Courier", df["Courier"].unique(), df["Courier"].unique())
segment = st.sidebar.multiselect("Segment", df["Segment"].unique(), df["Segment"].unique())
city = st.sidebar.multiselect("City", df["City"].unique(), df["City"].unique())

filtered = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1])) &
    (df["Courier"].isin(courier)) &
    (df["Segment"].isin(segment)) &
    (df["City"].isin(city))
]

# --------------------------
# KPI CARDS WITH TREND
# --------------------------
st.header("📊 Executive KPIs")

def calc_trend(series):
    return round(series.iloc[-1] - series.iloc[0], 2)

orders_trend = calc_trend(filtered["Orders"])
ontime_trend = calc_trend(filtered["On-Time %"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Orders", int(filtered["Orders"].sum()), delta=orders_trend)
col2.metric("On-Time %", round(filtered["On-Time %"].mean(),1), delta=ontime_trend)
col3.metric("RTO %", round(filtered["RTO %"].mean(),1))
col4.metric("Complaints %", round(filtered["Complaints %"].mean(),1))

# --------------------------
# AI INSIGHTS ENGINE
# --------------------------
st.header("🧠 Root Cause Insights")

if filtered["On-Time %"].mean() < 70:
    worst_courier = filtered.groupby("Courier")["On-Time %"].mean().idxmin()
    st.error(f"🚨 Low on-time performance driven by {worst_courier}")

if filtered["Complaints %"].mean() > 25:
    worst_city = filtered.groupby("City")["Complaints %"].mean().idxmax()
    st.warning(f"⚠️ Complaints highest in {worst_city}")

# --------------------------
# TREND ANALYSIS
# --------------------------
st.header("📈 Trends")

trend = filtered.groupby("Date").agg({
    "Orders":"sum",
    "On-Time %":"mean"
}).reset_index()

fig = px.line(trend, x="Date", y=["Orders","On-Time %"])
st.plotly_chart(fig, use_container_width=True)

# --------------------------
# FORECASTING (ML)
# --------------------------
st.header("🔮 Forecasting (Next 7 Days)")

trend["Day"] = np.arange(len(trend))
X = trend[["Day"]]
y = trend["Orders"]

model = LinearRegression().fit(X, y)

future_days = np.arange(len(trend), len(trend)+7).reshape(-1,1)
forecast = model.predict(future_days)

forecast_df = pd.DataFrame({
    "Day": future_days.flatten(),
    "Forecast Orders": forecast
})

fig2 = px.line(forecast_df, x="Day", y="Forecast Orders", title="Order Forecast")
st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# GEO HEATMAP
# --------------------------
st.header("🌍 City Performance Heatmap")

city_perf = filtered.groupby("City")["On-Time %"].mean().reset_index()

fig3 = px.scatter_geo(city_perf,
                      locations="City",
                      locationmode="country names",
                      size="On-Time %",
                      title="City Performance")

st.plotly_chart(fig3, use_container_width=True)

# --------------------------
# DRILL-DOWN
# --------------------------
st.header("🔍 Drill-Down")

selected_city = st.selectbox("Select City", filtered["City"].unique())

drill = filtered[filtered["City"] == selected_city]

fig4 = px.bar(drill, x="Courier", y="On-Time %", color="Courier")
st.plotly_chart(fig4, use_container_width=True)

# --------------------------
# COHORT ANALYSIS
# --------------------------
st.header("👥 Cohort Analysis")

cohort = filtered.groupby(["Segment","Courier"]).agg({
    "Orders":"sum"
}).reset_index()

fig5 = px.bar(cohort, x="Segment", y="Orders", color="Courier", barmode="group")
st.plotly_chart(fig5, use_container_width=True)

# --------------------------
# DOWNLOAD
# --------------------------
st.download_button("📥 Download Data",
                   filtered.to_csv(index=False),
                   "report.csv")
