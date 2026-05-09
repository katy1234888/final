import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Sidebar navigation
slides = [
    "Title",
    "Executive Summary",
    "Volume & Satisfaction",
    "Customer Sentiment",
    "Segment Risk",
    "Complaint Drivers",
    "Geographic Performance",
    "Courier & Root Causes",
    "Impact Funnel",
    "Action Plan",
    "Financial Impact",
    "Implementation Roadmap",
    "Next Steps",
    "Monitoring Dashboard",
    "Interactive Dashboard"
]

choice = st.sidebar.radio("Navigate", slides)

# -------------------------
# Slide 1
# -------------------------
if choice == "Title":
    st.title("📦 Delivery Experience Decline During Festive Surge")
    st.subheader("End-to-End Customer & Operational Diagnostics")
    st.write("OCT – DEC · TIER-1 & TIER-2 CITIES")

# -------------------------
# Slide 2
# -------------------------
elif choice == "Executive Summary":
    st.header("EXECUTIVE SUMMARY")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("NPS", "-44")
    col2.metric("On-Time Delivery", "62%")
    col3.metric("SLA Breach", "38%")
    col4.metric("Complaint Rate", "27%")
    col5.metric("RTO Rate", "18%")

    st.write("Peak-demand inefficiencies hurt both experience and profitability.")

# -------------------------
# Slide 3
# -------------------------
elif choice == "Volume & Satisfaction":
    st.header("Demand Surged. Capacity Didn't")

    df = pd.DataFrame({
        "Month": ["Oct", "Nov", "Dec"],
        "Orders": [100, 140, 170]
    })

    fig = px.line(df, x="Month", y="Orders", title="Order Volume Trend")
    st.plotly_chart(fig, use_container_width=True)

    st.write("Demand surge without capacity planning caused cascading operational failure.")

# -------------------------
# Slide 4
# -------------------------
elif choice == "Customer Sentiment":
    st.header("Customer Sentiment")

    df = pd.DataFrame({
        "Type": ["Promoters", "Passives", "Detractors"],
        "Value": [22, 12, 66]
    })

    fig = px.pie(df, names="Type", values="Value", title="NPS Distribution")
    st.plotly_chart(fig, use_container_width=True)

    st.write("NPS = -44 → Majority customers are unhappy")

# -------------------------
# Slide 5
# -------------------------
elif choice == "Segment Risk":
    st.header("High-Value Customers Are Walking")

    df = pd.DataFrame({
        "Segment": ["New", "Repeat", "High Value"],
        "NPS": [-35, -42, -60]
    })

    fig = px.bar(df, x="Segment", y="NPS", title="NPS by Segment")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Slide 6
# -------------------------
elif choice == "Complaint Drivers":
    st.header("Late Delivery Dominates Complaints")

    df = pd.DataFrame({
        "Issue": ["Late Delivery", "Delivery Failure", "Damaged", "Others"],
        "Percent": [55, 25, 10, 10]
    })

    fig = px.bar(df, x="Issue", y="Percent", title="Complaint Breakdown")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Slide 7
# -------------------------
elif choice == "Geographic Performance":
    st.header("Tier-2 Cities Are Operationally Broken")

    df = pd.DataFrame({
        "City": ["Mumbai", "Pune", "Indore", "Nagpur"],
        "On-Time %": [78, 65, 55, 50]
    })

    fig = px.bar(df, x="City", y="On-Time %", title="City Performance")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Slide 8
# -------------------------
elif choice == "Courier & Root Causes":
    st.header("Courier Performance")

    df = pd.DataFrame({
        "Courier": ["QuickShip", "ShipNow", "FastEx"],
        "SLA Breach %": [32, 22, 15]
    })

    fig = px.bar(df, x="Courier", y="SLA Breach %", title="Courier Performance")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Slide 9
# -------------------------
elif choice == "Impact Funnel":
    st.header("Revenue Leakage Funnel")

    df = pd.DataFrame({
        "Stage": ["Orders", "Delayed", "Complaints", "Lost Repeat"],
        "Value": [100, 38, 27, 6]
    })

    fig = px.funnel(df, x="Value", y="Stage")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Slide 10
# -------------------------
elif choice == "Action Plan":
    st.header("Three Fixes. Measurable Impact")

    st.write("""
    - Reduce QuickShip Load → SLA 32% → 18%
    - Improve Communication → Complaints 27% → 18%
    - Pre-Call Delivery → RTO 18% → 12%
    """)

# -------------------------
# Slide 11
# -------------------------
elif choice == "Financial Impact":
    st.header("Projected ROI")

    df = pd.DataFrame({
        "Category": ["Revenue Recovery", "Cost Savings", "LTV Uplift"],
        "Value": [170000, 378000, 250000]
    })

    fig = px.bar(df, x="Category", y="Value", title="Financial Impact ($)")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Slide 12
# -------------------------
elif choice == "Implementation Roadmap":
    st.header("90-Day Plan")

    st.write("""
    Phase 1: Stabilization  
    Phase 2: Optimization  
    Phase 3: Scaling  
    """)

# -------------------------
# Slide 13
# -------------------------
elif choice == "Next Steps":
    st.header("Execution Plan")

    st.write("""
    1. Reduce QuickShip Load  
    2. Improve Communication  
    3. Pre-call Delivery  
    """)

# -------------------------
# Slide 14
# -------------------------
elif choice == "Monitoring Dashboard":
    st.header("Live KPI Monitoring")

    col1, col2, col3 = st.columns(3)
    col1.metric("SLA Breach", "32%")
    col2.metric("Complaint Rate", "27%")
    col3.metric("NPS", "-44")

# -------------------------
# FINAL DASHBOARD
# -------------------------
elif choice == "Interactive Dashboard":
    st.title("📊 Interactive Dashboard")

    # Filters
    city = st.selectbox("Select City", ["All", "Mumbai", "Pune", "Indore", "Nagpur"])

    df = pd.DataFrame({
        "City": ["Mumbai", "Pune", "Indore", "Nagpur"],
        "On-Time": [78, 65, 55, 50],
        "Complaints": [20, 25, 35, 40]
    })

    if city != "All":
        df = df[df["City"] == city]

    fig1 = px.bar(df, x="City", y="On-Time", title="On-Time Delivery")
    fig2 = px.bar(df, x="City", y="Complaints", title="Complaint Rate")

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

    st.write("Dynamic filtering simulates Power BI dashboard behavior.")
