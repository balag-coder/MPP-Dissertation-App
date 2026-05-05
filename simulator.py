# ==============================================================================
# DIGITAL FISCALISM: THE "FILING DAY" SIMULATOR (MOBILE-OPTIMIZED)
# Author: Balaji K., MPP, IIT Tirupati
# Format: Narrative Policy Simulator (Scrollytelling & Geospatial)
# ==============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

# --- 1. PAGE CONFIGURATION & MOBILE-FIRST CSS ---
st.set_page_config(page_title="Digital Fiscalism Simulator", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    h1, h2, h3, p, div {font-family: 'Georgia', serif;}
    .story-text {font-size: 1.15rem; line-height: 1.7; margin-bottom: 20px; color: #2c3e50;}
    .highlight {color: #d1383c; font-weight: bold;}
    .highlight-blue {color: #002147; font-weight: bold;}
    .alert-box {background-color: #fff5f5; border-left: 5px solid #d1383c; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);}
    .metric-box {background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px;}
    .stButton>button {width: 100%; height: 60px; font-size: 18px; font-weight: bold; background-color: #002147; color: white; border-radius: 8px; border: none;}
    .stButton>button:hover {background-color: #003366; color: white; box-shadow: 0 4px 12px rgba(0,33,71,0.2);}
    hr {border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0));}
    </style>
""", unsafe_allow_html=True)

# --- 2. STATE MANAGEMENT ---
if 'step' not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

def reset_sim():
    st.session_state.step = 1

# --- 3. EXPANDED NATIONAL DATASET ---
data = {
    'State': [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 
        'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 
        'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 
        'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar', 'Chandigarh', 
        'Dadra and Nagar Haveli', 'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
    ],
    'Lat': [15.91, 28.21, 26.20, 25.09, 21.27, 15.29, 22.25, 29.05, 31.10, 23.61, 15.31, 10.85, 22.97, 19.75, 24.66, 25.46, 23.16, 26.15, 20.95, 31.14, 27.02, 27.53, 11.12, 18.11, 23.94, 26.84, 30.06, 22.98, 11.74, 30.73, 20.18, 28.70, 33.77, 34.15, 10.56, 11.94],
    'Lon': [79.74, 94.72, 92.93, 85.31, 81.86, 74.12, 71.19, 76.08, 77.17, 85.27, 75.71, 76.27, 78.65, 75.71, 93.90, 91.36, 92.93, 94.56, 85.09, 75.34, 74.21, 88.51, 78.65, 79.01, 91.98, 80.94, 79.01, 87.85, 92.65, 76.77, 73.01, 77.10, 76.57, 77.57, 72.64, 79.80],
    'Tier': [2, 3, 3, 3, 3, 1, 1, 1, 2, 3, 1, 1, 2, 1, 3, 3, 3, 3, 2, 2, 2, 3, 1, 1, 3, 2, 2, 2, 3, 1, 2, 1, 3, 3, 3, 2],
    'Base_Readiness': [60, 30, 35, 30, 35, 80, 85, 82, 65, 28, 82, 85, 52, 85, 30, 35, 35, 35, 50, 75, 55, 45, 80, 78, 40, 55, 60, 58, 45, 90, 60, 95, 40, 35, 40, 70]
}
df = pd.DataFrame(data)

# ==============================================================================
# ROOM 1: THE SETUP
# ==============================================================================
if st.session_state.step == 1:
    st.title("The Digital Fiscalism Journey")
    st.markdown("<div class='story-text'>Welcome to India's digital economy. The Goods and Services Tax (GST) represents a monumental shift toward digital taxation. But what happens when mandatory digital compliance meets uneven digital infrastructure?</div>", unsafe_allow_html=True)
    
    st.markdown("### Step 1: Establish Your Enterprise")
    st.markdown("<div class='story-text'>Imagine you manage a supply chain business. You rely heavily on generating e-way bills, and you must file your GSTR-3B returns by the 20th of the month.</div>", unsafe_allow_html=True)
    
    selected_state = st.selectbox("Where is your primary operational hub?", df['State'].tolist(), index=13) # Default Maharashtra
    st.session_state.user_state = selected_state
    
    business_size = st.select_slider(
        "Select your monthly economic activity (E-Way Bill Volume):",
        options=["Micro (< 50k)", "Medium (250k)", "Macro (1M+)"],
        value="Medium (250k)"
    )
    st.session_state.business_size = business_size
    vol_map = {"Micro (< 50k)": 40000, "Medium (250k)": 250000, "Macro (1M+)": 1500000}
    st.session_state.ewb_vol = vol_map[business_size]
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Fast Forward to the 20th ->", on_click=next_step)

# ==============================================================================
# ROOM 2: THE SHOCK (WITH GEOSPATIAL MAP)
# ==============================================================================
elif st.session_state.step == 2:
    st.title("The 20th: GST Filing Day")
    st.markdown(f"<div class='story-text'>It is 2:00 PM. Your accountants in <b>{st.session_state.user_state}</b> are preparing to upload the final sales invoices to the GSTN portal.</div>", unsafe_allow_html=True)
    
    with st.spinner("Connecting to GST Network..."):
        time.sleep(1.5)
    
    # Render Dynamic Map showing the disruption
    state_data = df[df['State'] == st.session_state.user_state].iloc[0]
    fig_map = px.scatter_mapbox(
        pd.DataFrame([state_data]), lat="Lat", lon="Lon", 
        zoom=4, center={"lat": 22.0, "lon": 79.0},
        mapbox_style="carto-positron", title="Live Network Status"
    )
    # Add a pulsing red disruption zone
    fig_map.add_trace(go.Scattermapbox(
        lat=[state_data['Lat']], lon=[state_data['Lon']],
        mode='markers', marker=go.scattermapbox.Marker(size=40, color='red', opacity=0.4),
        name="Disruption Zone"
    ))
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=300)
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("""
        <div class='alert-box'>
            <h3 style='color: #d1383c; margin-top: 0;'>🚨 ADMINISTRATIVE DISRUPTION</h3>
            <p>Under the <b>Temporary Suspension of Telecom Services Rules, 2017</b>, district authorities have ordered an immediate suspension of internet services to curb local unrest.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='story-text'>Your business is now offline. OTPs for the GST portal cannot be received. Common Service Centres (CSCs) are shut. The filing deadline is at midnight.</div>", unsafe_allow_html=True)
    
    st.button("Analyze Institutional Stress ->", on_click=next_step)

# ==============================================================================
# ROOM 3: THE FALLOUT & THE COST
# ==============================================================================
elif st.session_state.step == 3:
    st.title("Institutional Vulnerability Report")
    
    state_data = df[df['State'] == st.session_state.user_state].iloc[0]
    tier = state_data['Tier']
    readiness = state_data['Base_Readiness']
    
    # Econometrics
    base = {1: 2.5, 2: 5.5, 3: 9.0}[tier]
    bonus = ((readiness - 50) / 50) * 2.0 if readiness > 50 else 0
    struct_risk = max(0.5, base - bonus)
    
    causal_shock = 2.5 
    if st.session_state.ewb_vol < 500000:
         causal_shock += 3.0 
    total_risk = struct_risk + causal_shock
    
    st.markdown(f"<div class='story-text'>Your probability of missing the deadline is <span class='highlight'>{total_risk:.1f}%</span>. This is not a failure of your business, but a failure of <b>administrative resilience</b>. Here is exactly why you were forced to default:</div>", unsafe_allow_html=True)

    # --- THE FIXED, EXPLANATORY GRAPH ---
    fig = go.Figure(data=[
        go.Bar(name='Structural Baseline (State Infra)', x=['Friction Sources'], y=[struct_risk], marker_color='#002147', text=[f"Baseline: {struct_risk:.1f}%"], textposition='auto'),
        go.Bar(name='Causal Shock (Internet Disruption)', x=['Friction Sources'], y=[causal_shock], marker_color='#d1383c', text=[f"Disruption Penalty: {causal_shock:.1f}%"], textposition='auto')
    ])
    fig.update_layout(
        barmode='stack', height=350,
        yaxis_title="Probability of Late Filing (%)",
        yaxis=dict(range=[0, max(15, total_risk + 2)]),
        xaxis=dict(showticklabels=False), # Hide the "useless line" text
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Georgia"),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    # Add an explanatory annotation right on the chart
    fig.add_annotation(x=0.5, y=total_risk/2, text="Total Vulnerability", showarrow=False, font=dict(color="white", size=14), textangle=-90, xshift=-60)
    st.plotly_chart(fig, use_container_width=True)

    # --- NARRATIVE TRANSLATION OF THE GRAPH ---
    st.markdown(f"""
        <div style='font-size: 1rem; color: #555;'>
        <b>Understanding this graph:</b><br>
        <span class='highlight-blue'>■ The Blue Area:</span> Even on a peaceful day, businesses in {st.session_state.user_state} face a {struct_risk:.1f}% risk of filing late simply due to long-term digital divides and poor broadband penetration.<br>
        <span class='highlight'>■ The Red Area:</span> Because the government disrupted the internet today, your risk skyrocketed by an additional {causal_shock:.1f}%.
        </div>
        <hr>
    """, unsafe_allow_html=True)

    # --- THE FINANCIAL IMPACT (THE KICKER) ---
    st.markdown("### The Cost of Digital Fiscalism")
    st.markdown("<div class='story-text'>Under GST law, late filing accrues a mandatory penalty (CGST + SGST) plus an 18% interest rate on the tax liability. Assume the internet disruption lasts for 5 days:</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='metric-box'><h2 style='color:#d1383c; margin:0;'>₹250+</h2><p style='margin:0; font-size:14px;'>Minimum Late Fees</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-box'><h2 style='color:#d1383c; margin:0;'>18%</h2><p style='margin:0; font-size:14px;'>Interest on Capital</p></div>", unsafe_allow_html=True)

    st.markdown("<br><p style='font-style: italic; text-align: center; font-size: 0.9rem;'>The state effectively taxes the citizen for an infrastructural failure caused by the state itself.</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("↺ Start New Simulation", on_click=reset_sim)
