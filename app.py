import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Seashells Logistics AI Dashboard", layout="wide")

st.title("📦 Seashells Logistics Pvt Ltd")
st.subheader("🚚 AI-Powered Delivery Intelligence Dashboard")

# --------------------------
# FILE UPLOAD
# --------------------------
st.sidebar.header("📁 Upload All 6 Data Files")

orders_file = st.sidebar.file_uploader("Orders", type=["csv"])
nps_file = st.sidebar.file_uploader("NPS", type=["csv"])
hub_file = st.sidebar.file_uploader("Hub Performance", type=["csv"])
courier_file = st.sidebar.file_uploader("Courier Performance", type=["csv"])
customers_file = st.sidebar.file_uploader("Customers", type=["csv"])
complaints_file = st.sidebar.file_uploader("Complaints", type=["csv"])

# --------------------------
# LOAD FUNCTION
# --------------------------
def load_data(file):
    if file:
        return pd.read_csv(file)
    return None

orders = load_data(orders_file)
nps = load_data(nps_file)
hub = load_data(hub_file)
courier = load_data(courier_file)
customers = load_data(customers_file)
complaints = load_data(complaints_file)

# --------------------------
# DATA SUMMARY SECTION
# --------------------------
st.header("📊 Dataset Summary")

def summarize(df, name):
    if df is not None:
        st.subheader(f"📁 {name}")
        col1, col2, col3 = st.columns(3)

        col1.metric("Rows", df.shape[0])
        col2.metric("Columns", df.shape[1])
        col3.metric("Missing Values", df.isnull().sum().sum())

        st.dataframe(df.head(5))
    else:
        st.warning(f"{name} not uploaded")

summarize(orders, "Orders")
summarize(nps, "NPS")
summarize(hub, "Hub Performance")
summarize(courier, "Courier Performance")
summarize(customers, "Customers")
summarize(complaints, "Complaints")

# --------------------------
# DYNAMIC STORY
# --------------------------
st.header("📖 AI Storytelling (Data-Driven)")

if orders is not None and complaints is not None and nps is not None:

    # ---- Metrics ----
    total_orders = orders.shape[0]

    if "nps_score" in nps.columns:
        avg_nps = round(nps["nps_score"].mean(), 1)
    else:
        avg_nps = "N/A"

    if "issue" in complaints.columns:
        top_issue = complaints["issue"].value_counts().idxmax()
    else:
        top_issue = "Unknown"

    # ---- Story ----
    st.write(f"""
🚀 During the festive period, Seashells Logistics handled **{total_orders} orders**.

📉 Customer satisfaction dropped to **NPS: {avg_nps}**, indicating poor experience.

⚠️ The most common issue reported was **{top_issue}**, highlighting operational inefficiencies.

📦 This suggests that the system struggled to scale during peak demand, leading to delivery delays and failed orders.
""")

else:
    st.info("Upload Orders, NPS, and Complaints data to generate story")

# --------------------------
# VISUAL DASHBOARD
# --------------------------
st.header("📊 Interactive Dashboard")

# Orders Trend
if orders is not None:
    if "order_date" in orders.columns:
        orders["order_date"] = pd.to_datetime(orders["order_date"])
        fig = px.line(orders, x="order_date", title="Orders Trend")
        st.plotly_chart(fig, use_container_width=True)

# NPS
if nps is not None:
    if "customer_segment" in nps.columns and "nps_score" in nps.columns:
        fig = px.bar(nps, x="customer_segment", y="nps_score", color="customer_segment")
        st.plotly_chart(fig, use_container_width=True)

# Complaints
if complaints is not None:
    if "issue" in complaints.columns:
        fig = px.pie(complaints, names="issue")
        st.plotly_chart(fig, use_container_width=True)

# Courier Performance
if courier is not None:
    if "courier" in courier.columns and "on_time_delivery" in courier.columns:
        fig = px.bar(courier, x="courier", y="on_time_delivery")
        st.plotly_chart(fig, use_container_width=True)

# Hub Performance
if hub is not None:
    if "hub" in hub.columns and "delay" in hub.columns:
        fig = px.bar(hub, x="hub", y="delay")
        st.plotly_chart(fig, use_container_width=True)

# --------------------------
# ROOT CAUSE
# --------------------------
st.header("🔍 Root Cause Insights")

if complaints is not None:
    st.write("""
Key Problems Identified:
- High late deliveries
- Failed deliveries increasing
- Courier inefficiency
- Hub delays
""")

# --------------------------
# SOLUTIONS
# --------------------------
st.header("🛠️ Solutions")

st.write("""
Recommended Actions:
- Increase fleet capacity during peak
- Improve courier allocation
- Optimize delivery routing
- Add hub automation
""")

# --------------------------
# FINAL AI SUMMARY
# --------------------------
st.header("🤖 Executive Summary")

st.write("""
This dashboard highlights how operational inefficiencies during peak demand led to poor customer experience.

By improving logistics planning, courier performance, and hub efficiency, Seashells Logistics can significantly enhance delivery success and customer satisfaction.
""")
