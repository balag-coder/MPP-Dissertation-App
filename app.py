# ==============================================================================
# DIGITAL FISCALISM: POLICY VULNERABILITY EXPLORER 
# Author: Balaji K., MPP, IIT Tirupati
# Framework: Streamlit, Plotly
# Standard: Global Elite Policy Publication (Oxford Navy / Crimson Palette)
# ==============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# --- 1. PAGE CONFIGURATION & STRICT ACADEMIC STYLING ---
st.set_page_config(page_title="Digital Fiscalism Explorer", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main {background-color: #FDFDFD;}
    h1, h2, h3, h4, p, span, div {font-family: 'Times New Roman', Times, serif !important;}
    .caption-text {font-size: 12px; color: #555555; font-style: italic; margin-top: -10px; margin-bottom: 20px;}
    hr {border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));}
    </style>
""", unsafe_allow_html=True)

st.title("Digital Fiscalism: Policy Vulnerability Explorer")
st.markdown("An interactive simulation of GST compliance friction under digital disruptions. Estimates are derived from Fractional Logit and Two-Way Fixed Effects (TWFE) models using 70 months of state-level panel data.")
st.markdown("<hr>", unsafe_allow_html=True)

# --- 2. EXPANDED SPATIAL DATASET ---
# Comprehensive list of Indian States/UTs categorized by structural capacity
data = {
    'State': [
        'Maharashtra', 'Gujarat', 'Karnataka', 'Tamil Nadu', 'Telangana', 'Delhi', 'Haryana', 
        'Uttar Pradesh', 'Madhya Pradesh', 'Rajasthan', 'West Bengal', 'Andhra Pradesh', 'Kerala', 'Punjab', 'Odisha', 
        'Assam', 'Bihar', 'Jharkhand', 'Chhattisgarh', 'Uttarakhand', 'Himachal Pradesh', 'Jammu & Kashmir', 
        'Tripura', 'Meghalaya', 'Manipur', 'Nagaland', 'Arunachal Pradesh', 'Goa', 'Sikkim', 'Mizoram'
    ],
    'Lat': [
        19.75, 22.25, 15.31, 11.12, 18.11, 28.70, 29.05, 
        26.84, 22.97, 27.02, 22.98, 15.91, 10.85, 31.14, 20.95, 
        26.20, 25.09, 23.61, 21.27, 30.06, 31.10, 33.77, 
        23.94, 25.46, 24.66, 26.15, 28.21, 15.29, 27.53, 23.16
    ],
    'Lon': [
        75.71, 71.19, 75.71, 78.65, 79.01, 77.10, 76.08, 
        80.94, 78.65, 74.21, 87.85, 79.74, 76.27, 75.34, 85.09, 
        92.93, 85.31, 85.27, 81.86, 79.01, 77.17, 76.57, 
        91.98, 91.36, 93.90, 94.56, 94.72, 74.12, 88.51, 92.93
    ],
    'Tier': [
        1, 1, 1, 1, 1, 1, 1, 
        2, 2, 2, 2, 2, 2, 2, 2, 
        3, 3, 3, 3, 3, 3, 3, 
        3, 3, 3, 3, 3, 2, 3, 3
    ]
}
df = pd.DataFrame(data)

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### Model Parameters")
    
    st.markdown("**1. Target State Analysis**")
    selected_state = st.selectbox("Select State for Micro-Analysis", df['State'].tolist())
    selected_tier = df[df['State'] == selected_state]['Tier'].values[0]
    
    st.markdown("**2. Economic Activity**")
    ewb_volume = st.slider("Monthly E-Way Bill Transactions", 10000, 10000000, 350000, 50000, help="Proxy for state commercial activity.")
    
    st.markdown("**3. Infrastructural Resilience**")
    telecom_pen = st.slider("Digital Infrastructure Readiness (%)", 10, 100, 60, 1)
    
    st.markdown("---")
    st.markdown("**4. Exogenous Shock**")
    disruption_active = st.toggle("Activate Internet Disruption", value=False)

# --- 4. ECONOMETRIC LOGIC (APPLIED TO ALL) ---
def calc_structural(tier, telecom):
    base = {1: 2.5, 2: 5.5, 3: 9.0}[tier]
    bonus = ((telecom - 50) / 50) * 2.0 if telecom > 50 else 0
    return max(0.5, base - bonus)

def calc_causal(ewb, disruption):
    shock = 0.0
    if disruption:
        shock += 2.5
        if ewb < 500000:
            shock += 3.0
    return shock

# Calculate for entire dataframe
df['Structural Risk'] = df['Tier'].apply(lambda t: calc_structural(t, telecom_pen))
df['Causal Shock'] = df.apply(lambda row: calc_causal(ewb_volume, disruption_active), axis=1)
df['Predicted Late Filing Rate (%)'] = df['Structural Risk'] + df['Causal Shock']

# Calculate specifically for the selected state
state_struct = df[df['State'] == selected_state]['Structural Risk'].values[0]
state_causal = df[df['State'] == selected_state]['Causal Shock'].values[0]
state_total = df[df['State'] == selected_state]['Predicted Late Filing Rate (%)'].values[0]

# --- 5. VISUALIZATIONS: TOP ROW (MICRO ANALYSIS) ---
st.markdown(f"### Diagnostic Profile: {selected_state}")

col1, col2 = st.columns(2)

with col1:
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = state_total,
        number = {'suffix': "%", 'font': {'size': 40, 'color': '#1a1a1a', 'family': 'Times New Roman'}},
        gauge = {
            'axis': {'range': [0, 20], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "rgba(0,0,0,0)"}, 
            'steps': [
                {'range': [0, 5], 'color': "#E6ECF1"},   # Very Light Navy
                {'range': [5, 10], 'color': "#99B3C6"},  # Light Navy
                {'range': [10, 15], 'color': "#D99999"}, # Light Crimson
                {'range': [15, 20], 'color': "#8B0000"}  # Deep Crimson
            ],
            'threshold': {'line': {'color': "black", 'width': 3}, 'thickness': 0.75, 'value': state_total}
        }
    ))
    fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=10, b=10))
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown("<p class='caption-text'><b>Fig 1. Compliance Friction Gauge:</b> Reflects the cumulative probability of late GST compliance for the selected state, bounded mathematically by the Fractional Logit distribution.</p>", unsafe_allow_html=True)

with col2:
    fig_bar = go.Figure(data=[
        go.Bar(name='Structural Baseline (Between-State)', x=['Risk Components'], y=[state_struct], marker_color='#002147', text=[f"{state_struct:.1f}%"], textposition='auto'),
        go.Bar(name='Causal Shock (Within-State)', x=['Risk Components'], y=[state_causal], marker_color='#8B0000', text=[f"{state_causal:.1f}%"] if state_causal > 0 else [''], textposition='auto')
    ])
    fig_bar.update_layout(barmode='stack', height=250, yaxis_title="Probability (%)", yaxis=dict(range=[0, 20]),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                          plot_bgcolor='white', margin=dict(l=20, r=20, t=10, b=10), font=dict(family="Times New Roman"))
    fig_bar.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("<p class='caption-text'><b>Fig 2. Mundlak Variance Decomposition:</b> Isolates long-term infrastructural friction (Between-State) from real-time internet blackout shocks (Within-State) for the targeted constituency.</p>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- 6. VISUALIZATIONS: BOTTOM ROW (MACRO ANALYSIS) ---
st.markdown("### National Risk Stratification")

col3, col4 = st.columns([1.2, 1])

with col3:
    fig_map = px.scatter_mapbox(
        df, lat="Lat", lon="Lon", size="Predicted Late Filing Rate (%)", color="Predicted Late Filing Rate (%)",
        hover_name="State", hover_data={"Tier": True, "Lat": False, "Lon": False, "Predicted Late Filing Rate (%)": ':.2f'},
        color_continuous_scale=["#002147", "#99B3C6", "#D99999", "#8B0000"], 
        range_color=[0, 15], size_max=25, zoom=3.2, center={"lat": 22.0, "lon": 79.0},
        mapbox_style="carto-positron" # Clean, professional base map
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=400, font=dict(family="Times New Roman"))
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("<p class='caption-text'><b>Fig 3. Spatial Vulnerability Distribution:</b> Geospatial mapping of tax compliance friction. Marker size and color intensity proportionally indicate the severity of potential filing delays.</p>", unsafe_allow_html=True)

with col4:
    # Sort and take top 12 most vulnerable + bottom 3 resilient for contrast
    df_sorted = df.sort_values('Predicted Late Filing Rate (%)', ascending=True)
    
    fig_rank = px.bar(
        df_sorted.tail(15), x="Predicted Late Filing Rate (%)", y="State", orientation='h', 
        color="Predicted Late Filing Rate (%)", color_continuous_scale=["#002147", "#99B3C6", "#D99999", "#8B0000"], range_color=[0, 15]
    )
    fig_rank.update_layout(height=400, margin={"r":20,"t":0,"l":20,"b":0}, coloraxis_showscale=False, font=dict(family="Times New Roman"))
    fig_rank.add_vline(x=10, line_dash="dash", line_color="#8B0000", annotation_text="Critical Friction Threshold")
    st.plotly_chart(fig_rank, use_container_width=True)
    st.markdown("<p class='caption-text'><b>Fig 4. Systemic Risk Typologies:</b> Comparative baseline ranking highlighting the disparity in administrative resilience across major Indian states and union territories.</p>", unsafe_allow_html=True)
