# 🌧️ VarshVaani - Rainfall Prediction & Analysis App

**VarshVaani** is a powerful, AI-driven rainfall prediction and analysis web app built using **Streamlit**. It enables users to input monthly rainfall data for Indian districts, visualize patterns, predict annual rainfall using a machine learning model, and gain contextual weather information.

---

## 🚀 Features

- 📍 **State & District Selection**  
  Choose any district in India from an intuitive dropdown menu.

- 🌤 **Live Weather Integration**  
  View current temperature and weather conditions using the OpenWeatherMap API.

- 🧠 **Machine Learning Powered Prediction**  
  Predict total annual rainfall and get categorized output: **Low**, **Moderate**, or **Heavy**.

- 📈 **Monthly & Seasonal Rainfall Visualization**  
  View rainfall trends via dynamic bar and pie charts using Plotly.

- 🔁 **Auto-Fill Seasonal Totals**  
  Automatically calculate seasonal rainfall from monthly values.

- 📥 **Download Results**  
  Download predictions as a CSV for offline use or reporting.

- 📖 **Wikipedia Summaries**  
  Quick contextual info about the selected district.

---

## 🛠 Tech Stack

- **Frontend & UI:** Streamlit
- **Data Handling:** Pandas, NumPy
- **Visualization:** Plotly
- **Model Serving:** Scikit-learn & Joblib
- **APIs Used:**
  - OpenWeatherMap (for live weather data)
  - Wikipedia (for district summaries)

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Jadav-Gajanand-19/varshvaani.git
   cd varshvaani
