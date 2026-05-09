import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.impute import SimpleImputer

st.set_page_config(layout="wide")

st.title("📦 Seashells Logistics Pvt Ltd")
st.subheader("🚚 AI Storytelling Delivery Intelligence Dashboard")

# --------------------------
# FILE UPLOAD
# --------------------------
st.sidebar.header("📁 Upload All 6 Files")

orders_file = st.sidebar.file_uploader("Orders")
customers_file = st.sidebar.file_uploader("Customers")
nps_file = st.sidebar.file_uploader("NPS")
complaints_file = st.sidebar.file_uploader("Complaints")
hub_file = st.sidebar.file_uploader("Hub Performance")
courier_file = st.sidebar.file_uploader("Courier Performance")

def load(file):
    return pd.read_csv(file) if file else None

orders = load(orders_file)
customers = load(customers_file)
nps = load(nps_file)
complaints = load(complaints_file)
hub = load(hub_file)
courier = load(courier_file)

# --------------------------
# DATA SUMMARY
# --------------------------
st.header("📊 Dataset Summary")

def summary(df, name):
    if df is not None:
        st.subheader(name)
        st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        st.write("Missing Values:", df.isnull().sum().sum())
        st.dataframe(df.head(3))
    else:
        st.warning(f"{name} not uploaded")

summary(orders, "Orders")
summary(customers, "Customers")
summary(nps, "NPS")
summary(complaints, "Complaints")
summary(hub, "Hub")
summary(courier, "Courier")

# --------------------------
# DATA CLEANING BUTTON (ML IMPUTATION)
# --------------------------
st.header("⚙️ Data Cleaning")

if st.button("🔄 Revise Data (Fix Missing Values using ML)"):

    def impute(df):
        num_cols = df.select_dtypes(include=np.number).columns
        cat_cols = df.select_dtypes(exclude=np.number).columns

        if len(num_cols) > 0:
            df[num_cols] = SimpleImputer(strategy="mean").fit_transform(df[num_cols])
        if len(cat_cols) > 0:
            df[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df[cat_cols])
        return df

    if orders is not None:
        orders = impute(orders)
    if customers is not None:
        customers = impute(customers)
    if nps is not None:
        nps = impute(nps)
    if complaints is not None:
        complaints = impute(complaints)
    if hub is not None:
        hub = impute(hub)
    if courier is not None:
        courier = impute(courier)

    st.success("Data Cleaned Successfully ✅")

# --------------------------
# FEATURE ENGINEERING
# --------------------------
if orders is not None:
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["delivery_date"] = pd.to_datetime(orders["delivery_date"])
    orders["promised_date"] = pd.to_datetime(orders["promised_date"])

    orders["delay"] = (orders["delivery_date"] - orders["promised_date"]).dt.days
    orders["sla_breach"] = orders["delay"] > 0

# --------------------------
# STORY
# --------------------------
st.header("📖 Story")

st.image("https://images.unsplash.com/photo-1605902711622-cfb43c44367f")

if orders is not None and nps is not None:
    total_orders = len(orders)
    avg_nps = round(nps["score"].mean(),1)

    st.write(f"""
During festive months, the company handled **{total_orders} orders**.

However, customer satisfaction dropped to **NPS {avg_nps}**, indicating poor delivery experience.

Major issues emerged due to delays and operational inefficiencies.
""")

# --------------------------
# NPS ANALYSIS
# --------------------------
st.header("😊 NPS Analysis")

if nps is not None:
    nps["category"] = pd.cut(nps["score"],
                            bins=[-1,6,8,10],
                            labels=["Detractor","Passive","Promoter"])

    nps_score = (len(nps[nps["category"]=="Promoter"]) - len(nps[nps["category"]=="Detractor"])) / len(nps) * 100

    st.metric("Overall NPS", round(nps_score,1))

    fig = px.histogram(nps, x="score")
    st.plotly_chart(fig, use_container_width=True)

# --------------------------
# SEGMENT ANALYSIS
# --------------------------
if customers is not None and nps is not None:
    merged = pd.merge(nps, customers, on="customer_id")
    seg = merged.groupby("segment")["score"].mean().reset_index()

    st.subheader("NPS by Segment")
    fig = px.bar(seg, x="segment", y="score", color="segment")
    st.plotly_chart(fig)

# --------------------------
# COMPLAINT DRIVERS
# --------------------------
if complaints is not None:
    st.header("📞 Complaint Drivers")
    top_issue = complaints["issue_type"].value_counts().reset_index()

    fig = px.bar(top_issue, x="index", y="issue_type")
    st.plotly_chart(fig)

# --------------------------
# OPERATIONS
# --------------------------
st.header("🚚 Operations")

if hub is not None:
    hub["sla"] = hub["on_time_delivery"] / hub["total_orders"]
    fig = px.bar(hub, x="city", y="sla")
    st.plotly_chart(fig)

if courier is not None:
    fig = px.bar(courier, x="courier_partner", y="sla_breach_rate")
    st.plotly_chart(fig)

# --------------------------
# FUNNEL
# --------------------------
st.header("🔁 Funnel Analysis")

if orders is not None and complaints is not None and nps is not None:

    delayed = orders[orders["delay"] > 0]
    complaint_rate = len(complaints) / len(delayed) * 100

    detractors = nps[nps["score"] <= 6]
    detractor_rate = len(detractors) / len(complaints) * 100

    st.metric("% Delayed → Complaints", round(complaint_rate,1))
    st.metric("% Complaints → Detractors", round(detractor_rate,1))

# --------------------------
# ROOT CAUSE
# --------------------------
st.header("🔍 Root Causes")

st.write("""
Top Issues:
- Delivery delays
- Courier inefficiency
- Hub bottlenecks
- High failed attempts
""")

# --------------------------
# SOLUTIONS
# --------------------------
st.header("🛠️ Recommendations")

solutions = pd.DataFrame({
    "Solution":["Fleet Expansion","Better Routing","Courier Ranking","Hub Automation"],
    "Impact":[20,15,10,12]
})

fig = px.bar(solutions, x="Solution", y="Impact")
st.plotly_chart(fig)

# --------------------------
# FINAL DASHBOARD
# --------------------------
st.header("📊 Executive Dashboard")

col1, col2 = st.columns(2)

if orders is not None:
    fig1 = px.line(orders, x="order_date", y="delay")
    col1.plotly_chart(fig1)

if courier is not None:
    fig2 = px.bar(courier, x="courier_partner", y="sla_breach_rate")
    col2.plotly_chart(fig2)

st.success("🚀 Dashboard Ready for Leadership Review")
