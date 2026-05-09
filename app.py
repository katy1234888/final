import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --------------------------
# CONFIG
# --------------------------
st.set_page_config(page_title="Seashells Logistics Dashboard", layout="wide")

st.title("📦 Seashells Logistics Pvt Ltd")
st.subheader("🚚 Festive Surge Delivery Experience Dashboard")

# --------------------------
# SIDEBAR UPLOADS
# --------------------------
st.sidebar.header("📁 Upload All Data Files")

orders_file = st.sidebar.file_uploader("Orders Data", type=["csv"])
nps_file = st.sidebar.file_uploader("NPS Data", type=["csv"])
complaints_file = st.sidebar.file_uploader("Complaints Data", type=["csv"])
delivery_file = st.sidebar.file_uploader("Delivery Data", type=["csv"])
courier_file = st.sidebar.file_uploader("Courier Data", type=["csv"])
city_file = st.sidebar.file_uploader("City Data", type=["csv"])

# --------------------------
# SAMPLE DATA (fallback)
# --------------------------
def sample_orders():
    return pd.DataFrame({
        "Date": pd.date_range(start="2023-10-01", periods=30),
        "Orders": np.random.randint(500, 2000, 30)
    })

def sample_nps():
    return pd.DataFrame({
        "Segment": ["New","Repeat","High Value"],
        "NPS": [-30,-40,-60]
    })

def sample_complaints():
    return pd.DataFrame({
        "Issue": ["Late","Failed","Damaged"],
        "Percent": [55,25,10]
    })

def sample_delivery():
    return pd.DataFrame({
        "City": ["Mumbai","Pune","Indore","Nagpur"],
        "On-Time %": [78,65,55,50],
        "RTO %": [10,15,20,25]
    })

def sample_courier():
    return pd.DataFrame({
        "Courier": ["QuickShip","ShipNow","FastEx"],
        "On-Time %": [60,75,85]
    })

def sample_city():
    return pd.DataFrame({
        "City": ["Mumbai","Pune","Indore","Nagpur"],
        "Complaints %": [20,25,30,35]
    })

# --------------------------
# LOAD FUNCTION
# --------------------------
def load_data(file, sample, name):
    if file:
        df = pd.read_csv(file)
        st.sidebar.success(f"{name} ✅")
        return df
    else:
        st.sidebar.warning(f"{name} sample used")
        return sample

orders_df = load_data(orders_file, sample_orders(), "Orders")
nps_df = load_data(nps_file, sample_nps(), "NPS")
complaints_df = load_data(complaints_file, sample_complaints(), "Complaints")
delivery_df = load_data(delivery_file, sample_delivery(), "Delivery")
courier_df = load_data(courier_file, sample_courier(), "Courier")
city_df = load_data(city_file, sample_city(), "City")

# --------------------------
# FILTERS
# --------------------------
st.sidebar.header("🎛️ Filters")

if "Date" in orders_df.columns:
    orders_df["Date"] = pd.to_datetime(orders_df["Date"])
    date_range = st.sidebar.date_input("Select Date Range", [])

if "Courier" in courier_df.columns:
    courier_filter = st.sidebar.multiselect("Select Courier", courier_df["Courier"].unique())

if "Segment" in nps_df.columns:
    segment_filter = st.sidebar.multiselect("Select Segment", nps_df["Segment"].unique())

# --------------------------
# STORY MODE
# --------------------------
st.header("📖 Story: What Went Wrong?")

st.image("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d", use_container_width=True)
st.write("During festive surge, orders increased sharply while delivery quality dropped.")

# --------------------------
# KPI METRICS
# --------------------------
st.header("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Orders Peak", f"{orders_df['Orders'].max()}")
col2.metric("Avg NPS", f"{nps_df['NPS'].mean():.1f}")
col3.metric("On-Time Avg", f"{delivery_df['On-Time %'].mean():.1f}%")
col4.metric("Top Complaint", complaints_df.sort_values("Percent", ascending=False).iloc[0]["Issue"])

# --------------------------
# ORDERS TREND
# --------------------------
st.header("📈 Orders Trend")

fig_orders = px.line(orders_df, x="Date", y="Orders")
st.plotly_chart(fig_orders, use_container_width=True)

# --------------------------
# NPS ANALYSIS
# --------------------------
st.header("😊 Customer Experience (NPS)")

fig_nps = px.bar(nps_df, x="Segment", y="NPS", color="Segment")
st.plotly_chart(fig_nps, use_container_width=True)

# --------------------------
# COMPLAINTS
# --------------------------
st.header("📞 Complaint Breakdown")

fig_comp = px.pie(complaints_df, names="Issue", values="Percent")
st.plotly_chart(fig_comp, use_container_width=True)

# --------------------------
# DELIVERY PERFORMANCE
# --------------------------
st.header("🚚 Delivery Performance by City")

fig_del = px.bar(delivery_df, x="City", y="On-Time %")
st.plotly_chart(fig_del, use_container_width=True)

# --------------------------
# COURIER PERFORMANCE
# --------------------------
st.header("🚛 Courier Performance")

fig_courier = px.bar(courier_df, x="Courier", y="On-Time %", color="Courier")
st.plotly_chart(fig_courier, use_container_width=True)

# --------------------------
# CITY COMPLAINTS
# --------------------------
st.header("🏙️ City-Level Complaints")

fig_city = px.bar(city_df, x="City", y="Complaints %", color="City")
st.plotly_chart(fig_city, use_container_width=True)

# --------------------------
# ROOT CAUSE ANALYSIS
# --------------------------
st.header("🔍 Root Cause Analysis")

st.write("""
Top Issues Identified:
- Late Deliveries → 55%
- Failed Deliveries → 25%
- Poor Courier Performance in Tier 2 cities
- Capacity mismatch during peak demand
""")

st.image("https://images.unsplash.com/photo-1605902711622-cfb43c44367f", use_container_width=True)

# --------------------------
# SOLUTIONS (WITH NUMBERS)
# --------------------------
st.header("🛠️ Solutions & Impact")

solutions = pd.DataFrame({
    "Solution": ["Add Fleet","Improve Routing","Courier Ranking","Hub Automation"],
    "Impact (%)": [20,15,10,12]
})

fig_sol = px.bar(solutions, x="Solution", y="Impact (%)")
st.plotly_chart(fig_sol, use_container_width=True)

st.write("""
Expected Improvements:
- On-Time Delivery: +20%
- Complaints: -30%
- NPS: +25 points
""")

# --------------------------
# FINAL EXEC DASHBOARD
# --------------------------
st.header("📊 Executive Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_orders, use_container_width=True)
    st.plotly_chart(fig_nps, use_container_width=True)

with col2:
    st.plotly_chart(fig_del, use_container_width=True)
    st.plotly_chart(fig_courier, use_container_width=True)

# --------------------------
# AI NARRATION STYLE
# --------------------------
st.header("🤖 AI Summary")

st.write("""
🚀 “During festive surge, order volume increased sharply.
However, delivery capacity failed to scale proportionally.

This led to:
- Drop in on-time deliveries
- Surge in complaints
- Significant NPS decline

Key drivers:
- Courier inefficiencies
- City-level bottlenecks
- Poor demand forecasting

Recommended actions:
- Expand fleet capacity
- Optimize routing
- Prioritize high-value customers
- Strengthen courier SLAs

Expected outcome:
A 20–30% improvement in delivery performance and customer satisfaction.”
""")
