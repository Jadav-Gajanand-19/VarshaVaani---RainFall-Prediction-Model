import streamlit as st
import pandas as pd
import numpy as np
import requests
import joblib
import wikipedia
import plotly.express as px
from io import StringIO
from datetime import datetime

# Load the dataset and model
df = pd.read_csv("District_Rainfall_Normal_0.csv")
model = joblib.load("Rainfall_Prediction_model.pkl")

st.set_page_config(page_title="🌧️ Rainfall Intelligence Dashboard", layout="wide")
st.title("🌧️ Rainfall Prediction & Analysis App")

# Sidebar filters
st.sidebar.header("Select Region")
state_district_map = df.groupby("STATE_UT_NAME")["DISTRICT"].unique().to_dict()
state = st.sidebar.selectbox("Select State", sorted(state_district_map.keys()))
district = st.sidebar.selectbox("Select District", sorted(state_district_map[state]))

# Location Image & Wikipedia Info
st.subheader(f"📍 {district}, {state}")
st.image(f"https://source.unsplash.com/800x400/?{state},india", caption=f"Scene from {state}", use_column_width=True)

try:
    summary = wikipedia.summary(f"{district}, {state}, India", sentences=2)
    st.info(summary)
except:
    st.warning("Wikipedia summary not found.")

# Weather API (optional)
weather_api_key = "your_openweather_api_key"  # Replace this with your API key
weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={district},{state},IN&appid={weather_api_key}&units=metric"
try:
    res = requests.get(weather_url).json()
    if res.get("main"):
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        st.metric("🌡️ Current Temperature", f"{temp} °C")
        st.write(f"Condition: **{desc.title()}**")
except:
    st.write("🌐 Weather info not available")

# Rainfall Input Section
st.subheader("📥 Enter Monthly Rainfall Values")
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
seasonal = ["Jan-Feb", "Mar-May", "Jun-Sep", "Oct-Dec"]

monthly_inputs = {}
cols = st.columns(4)
for i, month in enumerate(months):
    with cols[i % 4]:
        monthly_inputs[month] = st.number_input(f"{month}", 0.0, 2000.0, 100.0)

# Auto fill seasonal
if st.button("🔁 Auto-Fill Seasonal Totals"):
    seasonal_values = {
        "Jan-Feb": monthly_inputs["JAN"] + monthly_inputs["FEB"],
        "Mar-May": sum([monthly_inputs[m] for m in ["MAR", "APR", "MAY"]]),
        "Jun-Sep": sum([monthly_inputs[m] for m in ["JUN", "JUL", "AUG", "SEP"]]),
        "Oct-Dec": sum([monthly_inputs[m] for m in ["OCT", "NOV", "DEC"]]),
    }
    for s in seasonal:
        st.session_state[s] = seasonal_values[s]

season_inputs = {}
for s in seasonal:
    season_inputs[s] = st.number_input(f"{s}", 0.0, 4000.0, key=s)

# Prediction Section
st.subheader("🤖 Prediction")
features = list(monthly_inputs.values()) + list(season_inputs.values())
X = np.array(features).reshape(1, -1)
prediction = model.predict(X)[0]

# Rainfall category tagging
if prediction < 500:
    category = "Low"
elif prediction < 1500:
    category = "Moderate"
else:
    category = "Heavy"

st.success(f"🌧️ Predicted Annual Rainfall: **{prediction:.2f} mm**")
st.info(f"Rainfall Category: **{category} Rainfall**")

# Plotly chart
st.subheader("📊 Rainfall Distribution Chart")
chart_data = pd.DataFrame({"Month": months, "Rainfall (mm)": list(monthly_inputs.values())})
st.plotly_chart(px.bar(chart_data, x="Month", y="Rainfall (mm)", title="Monthly Rainfall Distribution"))

# Download CSV of prediction
if st.download_button("📥 Download Prediction", data=f"District,State,Prediction_mm,Category\n{district},{state},{prediction:.2f},{category}", file_name="rainfall_prediction.csv"):
    st.success("✅ File ready for download")
