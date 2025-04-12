import streamlit as st
import pandas as pd
import numpy as np
import requests
import joblib
import wikipedia
import plotly.express as px
from io import StringIO
from datetime import datetime

# Load data and model
df = pd.read_csv("District_Rainfall_Normal_0.csv")
model = joblib.load("Rainfall_Prediction_model.pkl")

# App Configuration
st.set_page_config(page_title="🌧️ VarshVaani - Rainfall Intelligence Dashboard", layout="wide")
st.title("🌧️ VarshVaani - Rainfall Prediction & Analysis App")

# Sidebar - Region Selector
st.sidebar.header("🌍 Region Selection")
state_district_map = df.groupby("STATE_UT_NAME")["DISTRICT"].unique().to_dict()
state = st.sidebar.selectbox("Select State", sorted(state_district_map.keys()))
district = st.sidebar.selectbox("Select District", sorted(state_district_map[state]))

# Sidebar - Optional Weather API Key
st.sidebar.header("☁️ Weather API")
weather_api_key = st.sidebar.text_input("Enter OpenWeatherMap API Key", type="password")

# Location Display
st.subheader(f"📍 {district}, {state}")
st.image(f"https://source.unsplash.com/800x400/?{state},india", caption=f"Scenery from {state}", use_column_width=True)

try:
    summary = wikipedia.summary(f"{district}, {state}, India", sentences=2)
    st.info(summary)
except:
    st.warning("ℹ️ Wikipedia summary not found.")

# Weather Section
if weather_api_key:
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={district},{state},IN&appid={weather_api_key}&units=metric"
    try:
        res = requests.get(weather_url).json()
        if res.get("cod") == 200 and res.get("main"):
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            st.metric("🌡️ Current Temperature", f"{temp} °C")
            st.write(f"Condition: **{desc.title()}**")
        else:
            st.warning("Weather information currently unavailable.")
    except:
        st.warning("Failed to fetch weather data.")

# Monthly Rainfall Input
st.subheader("📥 Enter Monthly Rainfall (in mm)")
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
seasonal = ["Jan-Feb", "Mar-May", "Jun-Sep", "Oct-Dec"]

monthly_inputs = {}
cols = st.columns(4)
for i, month in enumerate(months):
    with cols[i % 4]:
        monthly_inputs[month] = st.number_input(f"{month}", 0.0, 2000.0, 100.0)

# Auto-Fill Seasonal
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

# Prediction
st.subheader("🤖 Predicted Rainfall")
features = list(monthly_inputs.values()) + list(season_inputs.values())

if all(v >= 0 for v in features):
    with st.spinner("Predicting..."):
        prediction = model.predict(np.array(features).reshape(1, -1))[0]

    if prediction < 500:
        category = "Low"
    elif prediction < 1500:
        category = "Moderate"
    else:
        category = "Heavy"

    st.success(f"🌧️ Predicted Annual Rainfall: **{prediction:.2f} mm**")
    st.info(f"Category: **{category} Rainfall**")

    # Monthly Bar Chart
    st.subheader("📊 Monthly Rainfall Distribution")
    monthly_df = pd.DataFrame({"Month": months, "Rainfall (mm)": list(monthly_inputs.values())})
    st.plotly_chart(px.bar(monthly_df, x="Month", y="Rainfall (mm)", title="Monthly Rainfall Distribution"))

    # Seasonal Pie Chart
    st.subheader("📈 Seasonal Rainfall Composition")
    season_df = pd.DataFrame({"Season": seasonal, "Rainfall (mm)": list(season_inputs.values())})
    st.plotly_chart(px.pie(season_df, names="Season", values="Rainfall (mm)", title="Seasonal Rainfall Breakdown"))

    # CSV Download
    csv_data = f"District,State,Prediction_mm,Category\n{district},{state},{prediction:.2f},{category}"
    if st.download_button("📥 Download Prediction", data=csv_data, file_name="varshvaani_prediction.csv"):
        st.success("✅ File ready for download")
else:
    st.warning("🚫 Please enter valid values for all inputs.")
