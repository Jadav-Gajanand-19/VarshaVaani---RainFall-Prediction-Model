# Updated Streamlit app for year-wise rainfall & weather prediction

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib

# --- LOAD DATA ---
df = pd.read_csv("Yearwise_Weather_Data_With_Condition.csv")
df.columns = df.columns.str.strip().str.upper()

# --- PAGE CONFIG ---
st.set_page_config(page_title="🌧️ VarshVaani - Rainfall Intelligence", layout="wide")

st.title("🌧️ VarshVaani - Rainfall Intelligence Dashboard")
st.markdown("### 📊 Explore year-wise rainfall and weather trends by location")

# --- LOCATION FILTERS ---
st.sidebar.header("🗺️ Select Location")
states = sorted(df["STATE/UT"].unique())
selected_state = st.sidebar.selectbox("Select State", states)
districts = sorted(df[df["STATE/UT"] == selected_state]["DISTRICT"].unique())
selected_district = st.sidebar.selectbox("Select District", districts)

filtered = df[(df["STATE/UT"] == selected_state) & (df["DISTRICT"] == selected_district)]

st.subheader(f"📍 Rainfall & Weather Trends for {selected_district}, {selected_state}")

# --- RAINFALL TREND ---
fig = px.line(filtered, x="YEAR", y="RAINFALL (MM)", title="📈 Annual Rainfall Trend",
              markers=True, template="plotly_dark")
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# --- WEATHER CONDITION DISTRIBUTION ---
condition_counts = filtered["WEATHER CONDITION"].value_counts().reset_index()
condition_counts.columns = ["Condition", "Count"]
fig2 = px.bar(condition_counts, x="Condition", y="Count", title="🌤️ Weather Condition Distribution",
              template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# --- RAINFALL PREDICTION ---
st.markdown("## 🔮 Predict Future Rainfall")
col1, col2, col3 = st.columns(3)
with col1:
    pred_state = st.selectbox("State (for prediction)", states)
with col2:
    pred_district = st.selectbox("District", sorted(df[df["STATE/UT"] == pred_state]["DISTRICT"].unique()))
with col3:
    pred_year = st.selectbox("Year", sorted(df["YEAR"].unique()))

try:
    model_rain = joblib.load("Rainfall_Prediction_model.pkl")
except Exception as e:
    st.error("🚫 Failed to load rainfall prediction model.")
    st.stop()

if st.button("🔍 Predict Rainfall"):
    try:
        input_df = pd.DataFrame([[pred_state, pred_district, pred_year]], columns=["STATE/UT", "DISTRICT", "YEAR"])
        prediction = model_rain.predict(input_df)[0]
        st.success(f"🌤️ Predicted Rainfall in **{pred_district}, {pred_state}** for **{pred_year}**: **{prediction:.2f} mm**")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")

# --- WEATHER CONDITION CLASSIFICATION ---
st.markdown("## 🧠 Predict Dominant Weather Condition")

try:
    model_weather = joblib.load("Weather_Condition_Classifier.pkl")
except Exception as e:
    st.error("🚫 Failed to load weather classification model.")
    st.stop()

if st.button("🌀 Predict Weather Condition"):
    try:
        input_df = pd.DataFrame([[pred_state, pred_district, pred_year]], columns=["STATE/UT", "DISTRICT", "YEAR"])
        weather_pred = model_weather.predict(input_df)[0]
        st.info(f"🌦️ Predicted dominant weather condition: **{weather_pred}**")
    except Exception as e:
        st.error(f"❌ Classification failed: {e}")

# --- FOOTER ---
st.markdown("---")
st.markdown("💡 *Powered by enriched climate data and machine learning models for rainfall & weather forecasting*")


