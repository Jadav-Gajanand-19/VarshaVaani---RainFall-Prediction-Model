import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html

# Load dataset
df = pd.read_csv("District_Rainfall_Normal_0.csv")
df.columns = df.columns.str.strip().str.upper()

# UI Setup
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

# Sidebar Filters
st.sidebar.header("🗺️ Select Location")
states = sorted(df["STATE_UT_NAME"].unique())
selected_state = st.sidebar.selectbox("Select State", states)
districts = sorted(df[df["STATE_UT_NAME"] == selected_state]["DISTRICT"].unique())
selected_district = st.sidebar.selectbox("Select District", districts)

# Filter Data
filtered = df[(df["STATE_UT_NAME"] == selected_state) & (df["DISTRICT"] == selected_district)]

st.subheader(f"📍 Rainfall Data for {selected_district}, {selected_state}")

# Unsplash Main Image
img_url = f"https://source.unsplash.com/800x400/?rain,{selected_district},india"
st.image(img_url, caption=f"{selected_district}, {selected_state}", use_column_width=True)

# Carousel for more images
carousel_html = f"""
<div id=\"carouselExampleIndicators\" class=\"carousel slide\" data-bs-ride=\"carousel\" style=\"max-width:800px;margin:auto\">
  <div class=\"carousel-inner\">
    {"".join([
        f'<div class=\"carousel-item {"active" if i == 0 else ""}\"><img src=\"https://source.unsplash.com/800x400/?{selected_district},india&sig={i}\" class=\"d-block w-100\" alt=\"...\"></div>'
        for i in range(1, 6)
    ])}
  </div>
  <button class=\"carousel-control-prev\" type=\"button\" data-bs-target=\"#carouselExampleIndicators\" data-bs-slide=\"prev\">
    <span class=\"carousel-control-prev-icon\" aria-hidden=\"true\"></span>
  </button>
  <button class=\"carousel-control-next\" type=\"button\" data-bs-target=\"#carouselExampleIndicators\" data-bs-slide=\"next\">
    <span class=\"carousel-control-next-icon\" aria-hidden=\"true\"></span>
  </button>
</div>

<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
<script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js\"></script>
"""

html(carousel_html, height=450)

# Show Monthly Rainfall
monthly_cols = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
monthly_values = filtered[monthly_cols].mean().round(2)

rainfall_df = pd.DataFrame({"Month": monthly_cols, "Rainfall (mm)": monthly_values.values})

# Chart
st.plotly_chart(
    px.bar(rainfall_df, x="Month", y="Rainfall (mm)", title="📊 Average Monthly Rainfall",
           color="Rainfall (mm)", color_continuous_scale="Blues"),
    use_container_width=True
)

# Total Rainfall Card
total_rainfall = monthly_values.sum()
st.metric("🌧️ Average Total Annual Rainfall", f"{total_rainfall:.2f} mm")

# Trend Over Years (if available)
year_cols = [col for col in df.columns if col.isdigit()]
if year_cols:
    yearwise_data = filtered[year_cols].T
    yearwise_data.columns = ["Rainfall"]
    yearwise_data["Year"] = yearwise_data.index.astype(int)
    yearwise_data = yearwise_data.sort_values("Year")

    st.subheader("🕰️ Rainfall Trend Over Years")
    st.line_chart(yearwise_data.set_index("Year"))

# Footer
st.markdown("---")
st.markdown("💡 *Powered by historical data and beautiful weather-inspired design.*")

