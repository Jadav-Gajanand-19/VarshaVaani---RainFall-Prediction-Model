import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from streamlit.components.v1 import html
import plotly.graph_objects as go

# --- SETTINGS ---
PEXELS_API_KEY = "cHLzVW6EUPDn1dI4MQ6PkCPtcEQFtXZve2uYdTmxY9HXy28ZbUToumsp"  # Replace with your actual Pexels API key

def fetch_pexels_images(query, api_key, count=5):
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": count}
    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    if response.status_code == 200:
        return [photo["src"]["landscape"] for photo in response.json()["photos"]]
    else:
        st.warning("⚠️ Failed to fetch images from Pexels")
        return []

# --- DATA LOAD ---
df = pd.read_csv("District_Rainfall_Normal_0.csv")
df.columns = df.columns.str.strip().str.upper()

# --- PAGE CONFIG ---
st.set_page_config(page_title="🌧️ VarshVaani - Rainfall Intelligence", layout="wide")

# --- CUSTOM CSS & ANIMATION ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #a8edea, #fed6e3);
        animation: rain 10s linear infinite;
    }
    @keyframes rain {
        0% { background-position: 0 0; }
        100% { background-position: 1000px 1000px; }
    }
    .block-container {
        padding: 2rem;
    }
    .rain-animation {
        background: url('https://i.ibb.co/7yzjLBQ/rain.gif') repeat;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        opacity: 0.4;
    }
    </style>
""", unsafe_allow_html=True)

# --- BACKGROUND SOUND ---
html("""
<audio autoplay loop>
  <source src="https://www.fesliyanstudios.com/play-mp3/387" type="audio/mp3">
</audio>
""", height=0)

st.markdown("<div class='rain-animation'></div>", unsafe_allow_html=True)

st.title("🌧️ VarshVaani - Rainfall Intelligence Dashboard")
st.markdown("### 📊 Predict historical monthly rainfall trends by location")

# --- LOCATION FILTERS ---
st.sidebar.header("🗺️ Select Location")
states = sorted(df["STATE/UT"].unique())
selected_state = st.sidebar.selectbox("Select State", states)
districts = sorted(df[df["STATE/UT"] == selected_state]["DISTRICT"].unique())
selected_district = st.sidebar.selectbox("Select District", districts)

filtered = df[(df["STATE/UT"] == selected_state) & (df["DISTRICT"] == selected_district)]

st.subheader(f"📍 Rainfall Data for {selected_district}, {selected_state}")

# --- IMAGE GALLERY ---
image_urls = fetch_pexels_images(f"{selected_district} {selected_state} India weather", PEXELS_API_KEY)

if image_urls:
    carousel_html = f"""
    <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel" style="max-width:800px;margin:auto">
      <div class="carousel-inner">
        {"".join([f'<div class="carousel-item {"active" if i == 0 else ""}"><img src="{img}" class="d-block w-100" alt="Image"></div>' for i, img in enumerate(image_urls)])}
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

fig = go.Figure()
fig.add_trace(go.Bar(
    x=rainfall_df["Month"],
    y=rainfall_df["Rainfall (mm)"],
    marker=dict(color=rainfall_df["Rainfall (mm)"], colorscale='Viridis'),
    name='Rainfall',
))
fig.add_trace(go.Scatter(
    x=rainfall_df["Month"],
    y=rainfall_df["Rainfall (mm)"],
    mode='lines+markers',
    line=dict(color='black', dash='dash'),
    name='Trend'
))
fig.update_layout(
    title="🌈 Average Monthly Rainfall with Trend Line",
    template="plotly_dark",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    scene=dict(zaxis_title='Rainfall (mm)')
)
st.plotly_chart(fig, use_container_width=True)

# --- EXPORT OPTION ---
st.download_button(
    label="📥 Download Graph Data",
    data=rainfall_df.to_csv(index=False).encode('utf-8'),
    file_name="rainfall_data.csv",
    mime="text/csv"
)

# --- TOTAL ANNUAL RAINFALL ---
total_rainfall = monthly_values.sum()
st.metric("🌧️ Average Total Annual Rainfall", f"{total_rainfall:.2f} mm")

# --- FOOTER ---
st.markdown("---")
st.markdown("💡 *Powered by historical data, 3D visuals, and ambient rain from Pexels & open sources*")

