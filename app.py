# ==============================================================================
# DIGITAL FISCALISM: POLICY VULNERABILITY EXPLORER (WITH GIS)
# Author: Balaji K. 
# Framework: Streamlit, Plotly
# ==============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Digital Fiscalism Explorer", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #FAFAFA;}
    h1, h2, h3 {font-family: 'Times New Roman', Times, serif; color: #1a1a1a;}
    </style>
""", unsafe_allow_html=True)

st.title("Digital Fiscalism: Policy Vulnerability Explorer")
st.markdown("""
*An interactive simulation of GST compliance friction under digital disruptions.*  
**Instructions for Committee:** Adjust the parameters in the sidebar to simulate the probability of late GST filings. Watch the spatial impact dynamically update on the map of India.
---
""")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("Model Parameters")
    
    st.subheader("1. Economic Activity")
    ewb_volume = st.slider("Monthly E-Way Bill Transactions", 10000, 10000000, 350000, 50000)
    
    st.subheader("2. Infrastructural Resilience")
    telecom_pen = st.slider("Digital Infrastructure Readiness (%)", 10, 100, 60, 1)
    
    st.markdown("---")
    st.subheader("3. Exogenous Shock")
    disruption_active = st.toggle("🚨 Activate Internet Disruption", value=False)

# --- SPATIAL DATASET (REPRESENTATIVE TIERED STATES) ---
data = {
    'State': ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh', 'Madhya Pradesh', 'Punjab', 'Assam', 'Bihar', 'Jharkhand'],
    'Lat': [19.75, 15.31, 11.12, 26.84, 22.97, 31.14, 26.20, 25.09, 23.61],
    'Lon': [75.71, 75.71, 78.65, 80.94, 78.65, 75.34, 92.93, 85.31, 85.27],
    'Tier': [1, 1, 1, 2, 2, 2, 3, 3, 3]
}
df = pd.DataFrame(data)

# --- DYNAMIC RISK CALCULATION FOR MAP ---
def calculate_risk(tier, ewb, telecom, disruption):
    base_risk = {1: 2.5, 2: 5.5, 3: 9.0}[tier]
    infra_bonus = ((telecom - 50) / 50) * 2.0 if telecom > 50 else 0
    structural_risk = max(0.5, base_risk - infra_bonus)
    
    causal_shock = 0.0
    if disruption:
        causal_shock += 2.5
        if ewb < 500000:
            causal_shock += 3.0
            
    return structural_risk + causal_shock

df['Current Risk (%)'] = df.apply(lambda row: calculate_risk(row['Tier'], ewb_volume, telecom_pen, disruption_active), axis=1)

# --- VISUALIZATIONS ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### National Geographic Vulnerability")
    # Dynamic GIS Map
    fig_map = px.scatter_mapbox(
        df, lat="Lat", lon="Lon", size="Current Risk (%)", color="Current Risk (%)",
        hover_name="State", hover_data={"Tier": True, "Lat": False, "Lon": False, "Current Risk (%)": ':.2f'},
        color_continuous_scale=["#005b9f", "#e6f2ff", "#ffb3b3", "#d1383c"], # Safe Blue to Critical Red
        range_color=[0, 20],
        size_max=35 if disruption_active else 15,
        zoom=3.5, center={"lat": 22.0, "lon": 79.0},
        mapbox_style="carto-positron",
        title="Live Spatial Distribution of Tax Friction"
    )
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=450)
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.markdown("### State-Level Risk Typologies")
    # Bar Chart updating based on map data
    fig_bar = px.bar(
        df.sort_values('Current Risk (%)', ascending=True), 
        x="Current Risk (%)", y="State", orientation='h', color="Current Risk (%)",
        color_continuous_scale=["#005b9f", "#e6f2ff", "#ffb3b3", "#d1383c"],
        range_color=[0, 20]
    )
    fig_bar.update_layout(height=450, margin={"r":20,"t":40,"l":20,"b":20}, coloraxis_showscale=False)
    fig_bar.add_vline(x=10, line_dash="dash", line_color="red", annotation_text="Critical Threshold")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- METHODOLOGICAL NOTE ---
st.markdown("---")
st.caption("**Methodological Note:** Estimates are derived from Fractional Logit and Two-Way Fixed Effects (TWFE) models using 70 months of state-level panel data. Size and color intensity on the map represent the predicted probability of late GST filings based on structural tier, digital readiness, and real-time network disruptions.")
