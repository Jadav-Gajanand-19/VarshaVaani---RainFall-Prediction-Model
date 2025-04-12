import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from streamlit.components.v1 import html

# --- SETTINGS ---
PEXELS_API_KEY = "cHLzVW6EUPDn1dI4MQ6PkCPtcEQFtXZve2uYdTmxY9HXy28ZbUToumsp"

# --- IMAGE FETCHER ---
def fetch_pexels_images(query, api_key, count=5):
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": count}
    try:
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
        response.raise_for_status()
        results = response.json()
        return [photo["src"]["landscape"] for photo in results.get("photos", [])]
    except Exception as e:
        st.warning(f"⚠️ Failed to load images: {e}")
        return []

# --- DATA LOAD ---
df = pd.read_csv("District_Rainfall_Normal_0.csv")
df.columns = df.columns.str.strip().str.upper()

# --- UI CONFIG ---
st.set_page_config(page_title="🌧️ VarshVaani - Rainfall Intelligence", layout="wide")
st.markdown("""
    <style>
        .main {
            background: linear-gradient(to right, #c9d6ff, #e2e2e2);
            font-family: 'Segoe UI', sans-serif;
        }
        .block-container {
            padding: 2rem 2rem 2rem 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🌧️ VarshVaani - Rainfall Intelligence Dashboard")
st.markdown("### Predict historical monthly rainfall trends by location")

# --- LOCATION FILTERS ---
st.sidebar.header("🗺️ Select Location")
states = sorted(df["STATE_UT_NAME"].unique())
selected_state = st.sidebar.selectbox("Select State", states)
districts = sorted(df[df["STATE_UT_NAME"] == selected_state]["DISTRICT"].unique())
selected_district = st.sidebar.selectbox("Select District", districts)

filtered = df[(df["STATE_UT_NAME"] == selected_state) & (df["DISTRICT"] == selected_district)]

st.subheader(f"📍 Rainfall Data for {selected_district}, {selected_state}")

# --- IMAGE CAROUSEL ---
image_urls = fetch_pexels_images(f"{selected_district} {selected_state} india weather", PEXELS_API_KEY)

if image_urls:
    carousel_html = f"""
    <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel" style="max-width:800px;margin:auto">
      <div class="carousel-inner">
        {"".join([
            f'<div class="carousel-item {"active" if i == 0 else ""}"><img src="{img}" class="d-block w-100" alt="Image"></div>'
            for i, img in enumerate(image_urls)
        ])}
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
      </button>
    </div>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    """
    html(carousel_html, height=450)
else:
    st.image("https://source.unsplash.com/800x400/?rain", caption="Weather View", use_column_width=True)

# --- MONTHLY RAINFALL ---
monthly_cols = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
monthly_values = filtered[monthly_cols].mean().round(2)
rainfall_df = pd.DataFrame({"Month": monthly_cols, "Rainfall (mm)": monthly_values.values})

st.plotly_chart(
    px.bar(rainfall_df, x="Month", y="Rainfall (mm)", title="📊 Average Monthly Rainfall",
           color="Rainfall (mm)", color_continuous_scale="Blues"),
    use_container_width=True
)

# --- TOTAL ANNUAL RAINFALL ---
total_rainfall = monthly_values.sum()
st.metric("🌧️ Average Total Annual Rainfall", f"{total_rainfall:.2f} mm")

# --- FOOTER ---
st.markdown("---")
st.markdown("💡 *Powered by historical data and beautiful weather-inspired design.*")

