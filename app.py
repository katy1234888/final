import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from gtts import gTTS
import tempfile

st.set_page_config(page_title="Seashells Intelligence System", layout="wide")

# --------------------------
# HEADER
# --------------------------
st.title("🌊 Seashells Logistics Pvt Ltd")
st.subheader("📊 AI-Powered Delivery Intelligence System")

# --------------------------
# STORY MODE CONTROL
# --------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

steps = ["Problem", "Impact", "Diagnosis", "Insights", "Forecast", "Solution"]

col1, col2 = st.columns([8,1])
with col2:
    if st.button("➡️ Next"):
        st.session_state.step = (st.session_state.step + 1) % len(steps)

current_step = steps[st.session_state.step]
st.markdown(f"## 🎬 Story Mode: {current_step}")

# --------------------------
# FILE UPLOAD
# --------------------------
st.sidebar.header("📁 Upload Data")

required_cols = ["Date", "City", "Courier", "Segment", "Orders", "On-Time %", "RTO %", "Complaints %"]

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

def load_sample():
    return pd.DataFrame({
        "Date": pd.date_range(start="2023-10-01", periods=60),
        "City": np.random.choice(["Mumbai","Pune","Indore","Nagpur"],60),
        "Courier": np.random.choice(["QuickShip","ShipNow","FastEx"],60),
        "Segment": np.random.choice(["New","Repeat","High Value"],60),
        "Orders": np.random.randint(500,2000,60),
        "On-Time %": np.random.randint(50,90,60),
        "RTO %": np.random.randint(5,25,60),
        "Complaints %": np.random.randint(10,35,60)
    })

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()
    df["Date"] = pd.to_datetime(df["Date"])
else:
    df = load_sample()

# --------------------------
# FILTERS
# --------------------------
st.sidebar.header("🔎 Filters")

date_range = st.sidebar.date_input("Date Range", [df["Date"].min(), df["Date"].max()])
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
# AI NARRATION
# --------------------------
def generate_narration(step, df):
    if step == "Problem":
        return "During the festive surge, order volumes increased sharply, overwhelming logistics capacity."
    elif step == "Impact":
        return f"On-time delivery dropped to {round(df['On-Time %'].mean(),1)} percent, while complaints increased significantly."
    elif step == "Diagnosis":
        worst_city = df.groupby("City")["On-Time %"].mean().idxmin()
        return f"The biggest operational failures are concentrated in {worst_city}."
    elif step == "Insights":
        worst_courier = df.groupby("Courier")["On-Time %"].mean().idxmin()
        return f"{worst_courier} is the primary contributor to delays."
    elif step == "Forecast":
        return "If trends continue, delivery performance will degrade further during the next surge."
    elif step == "Solution":
        return "Optimizing courier allocation and improving infrastructure can significantly improve outcomes."

def play_voice(text):
    tts = gTTS(text)
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tts.save(tmp.name)
    audio_file = open(tmp.name, 'rb')
    st.audio(audio_file.read(), format='audio/mp3')

narration = generate_narration(current_step, filtered)
st.info(f"🧠 AI Narration: {narration}")

if st.checkbox("🔊 Play Voice Narration"):
    play_voice(narration)

# --------------------------
# KPI SECTION
# --------------------------
st.markdown("## 📊 Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Orders", int(filtered["Orders"].sum()))
col2.metric("On-Time %", round(filtered["On-Time %"].mean(),1))
col3.metric("RTO %", round(filtered["RTO %"].mean(),1))
col4.metric("Complaints %", round(filtered["Complaints %"].mean(),1))

# --------------------------
# STORY VISUALS
# --------------------------
if current_step == "Problem":
    st.image("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d", use_container_width=True)

elif current_step == "Impact":
    st.image("https://images.unsplash.com/photo-1553413077-190dd305871c", use_container_width=True)

elif current_step == "Diagnosis":
    fig = px.bar(filtered.groupby("City")["On-Time %"].mean().reset_index(),
                 x="City", y="On-Time %")
    st.plotly_chart(fig, use_container_width=True)

elif current_step == "Insights":
    fig = px.bar(filtered.groupby("Courier")["On-Time %"].mean().reset_index(),
                 x="Courier", y="On-Time %", color="Courier")
    st.plotly_chart(fig, use_container_width=True)

elif current_step == "Forecast":
    trend = filtered.groupby("Date")["Orders"].sum().reset_index()
    trend["Day"] = np.arange(len(trend))

    model = LinearRegression().fit(trend[["Day"]], trend["Orders"])
    future = np.arange(len(trend), len(trend)+7).reshape(-1,1)
    forecast = model.predict(future)

    forecast_df = pd.DataFrame({"Day": future.flatten(), "Forecast Orders": forecast})

    fig = px.line(forecast_df, x="Day", y="Forecast Orders")
    st.plotly_chart(fig, use_container_width=True)

elif current_step == "Solution":
    st.image("https://images.unsplash.com/photo-1605902711834-8b11c3c0d5d6", use_container_width=True)
    st.success("""
    🚀 Recommended Actions:
    - Optimize courier allocation  
    - Improve Tier-2 infrastructure  
    - Add proactive communication  
    - Plan for surge capacity  
    """)

# --------------------------
# ADDITIONAL ANALYTICS
# --------------------------
st.markdown("## 🔍 Deep Dive Analytics")

selected_city = st.selectbox("Select City", filtered["City"].unique())
drill = filtered[filtered["City"] == selected_city]

fig = px.bar(drill, x="Courier", y="On-Time %", color="Courier")
st.plotly_chart(fig, use_container_width=True)

# Cohort
cohort = filtered.groupby(["Segment","Courier"])["Orders"].sum().reset_index()
fig2 = px.bar(cohort, x="Segment", y="Orders", color="Courier", barmode="group")
st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# DOWNLOAD
# --------------------------
st.download_button("📥 Download Report",
                   filtered.to_csv(index=False),
                   "seashells_report.csv")

# --------------------------
# DATA TABLE
# --------------------------
st.markdown("## 📄 Data Table")
st.dataframe(filtered)
