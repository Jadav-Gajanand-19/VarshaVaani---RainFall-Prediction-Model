import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import plotly.graph_objects as go
from streamlit.components.v1 import html

# --- SETTINGS ---
PEXELS_API_KEY = "cHLzVW6EUPDn1dI4MQ6PkCPtcEQFtXZve2uYdTmxY9HXy28ZbUToumsp"  # 🔁 Replace this with your actual API key

# --- IMAGE FETCHER (Pexels) ---
def fetch_pexels_images(query, api_key, count=5):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": count, "orientation": "landscape"}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return [photo["src"]["large"] for photo in data.get("photos", [])]
    except Exception as e:
        st.warning(f"⚠️ Failed to fetch Pexels images: {e}")
        return []

# --- DATA LOAD ---
df = pd.read_csv("District_Rainfall_Normal_0.csv")
df.columns = df.columns.str.strip().str.upper()

# --- UI CONFIG ---
st.set_page_config(page_title="\ud83c\udf27\ufe0f VarshVaani - Rainfall Intelligence", layout="wide")

# --- STYLING + RAIN ANIMATION + AUDIO ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #74ebd5, #9face6);
        overflow-x: hidden;
    }
    .block-container {
        padding: 2rem;
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }
    .rainfall-card {
        background: linear-gradient(to right, #43cea2, #185a9d);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        animation: fadeIn 2s ease-in-out;
    }
    .rain {
        background-image: url('https://i.gifer.com/VAyR.gif');
        background-size: cover;
        background-repeat: no-repeat;
        position: fixed;
        top: 0;
        left: 0;
        height: 100%;
        width: 100%;
        opacity: 0.15;
        z-index: -1;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="rain"></div>

    <audio autoplay loop>
        <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-12.mp3" type="audio/mpeg">
        Your browser does not support the audio element.
    </audio>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("\ud83c\udf27\ufe0f VarshVaani")
st.markdown("<h3 style='color:#0f2027;'>Rainfall Intelligence Dashboard</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='color:#003f5c;'>Predict historical monthly rainfall trends by location \ud83c\udf0d</h5>", unsafe_allow_html=True)

# --- LOCATION FILTERS ---
st.sidebar.header("\ud83c\udf0d Select Location")
states = sorted(df["STATE/UT"].unique())
selected_state = st.sidebar.selectbox("Select State", states)
districts = sorted(df[df["STATE/UT"] == selected_state]["DISTRICT"].unique())
selected_district = st.sidebar.selectbox("Select District", districts)

filtered = df[(df["STATE/UT"] == selected_state) & (df["DISTRICT"] == selected_district)]

st.subheader(f"\ud83d\udccd Rainfall Data for {selected_district}, {selected_state}")

# --- IMAGE CAROUSEL ---
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

# --- RAINFALL ANALYSIS ---
monthly_cols = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
monthly_values = filtered[monthly_cols].mean().round(2)
rainfall_df = pd.DataFrame({"Month": monthly_cols, "Rainfall (mm)": monthly_values.values})

# --- ADDING 3D-LIKE BAR CHART ---
fig = go.Figure()
fig.add_trace(go.Bar(
    x=rainfall_df["Month"],
    y=rainfall_df["Rainfall (mm)"],
    name='Monthly Rainfall',
    marker_color='lightskyblue',
    marker_line_color='darkblue',
    marker_line_width=1.5,
    opacity=0.8
))
fig.add_trace(go.Scatter(x=rainfall_df["Month"], y=rainfall_df["Rainfall (mm)"],
                         mode='lines+markers', name='Trend Line',
                         line=dict(color='darkblue', dash='dot')))
fig.update_layout(title="\ud83d\udcca Average Monthly Rainfall (with 3D Effect)",
                  plot_bgcolor='rgba(240,248,255,0.8)',
                  paper_bgcolor='rgba(255,255,255,0.7)',
                  margin=dict(l=40, r=20, t=60, b=30))

# --- DOWNLOAD OPTION ---
st.download_button(
    label="\ud83d\udcc5 Download Rainfall Graph as PNG",
    data=fig.to_image(format="png"),
    file_name=f"{selected_district}_{selected_state}_rainfall.png",
    mime="image/png"
)

# --- DISPLAY PLOT ---
st.plotly_chart(fig, use_container_width=True)

# --- TOTAL RAINFALL METRIC ---
total_rainfall = monthly_values.sum()
st.markdown(f"""
    <div class='rainfall-card'>
        \ud83c\udf27\ufe0f Average Total Annual Rainfall: {total_rainfall:.2f} mm
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("\ud83d\udca1 *Powered by historical data, beautiful visuals from Pexels, and good vibes from nature \ud83c\udf3f*")
