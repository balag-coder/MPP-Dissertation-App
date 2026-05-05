# ==============================================================================
# DIGITAL FISCALISM: THE "FILING DAY" SIMULATOR (MOBILE-FIRST)
# Author: Balaji K., MPP, IIT Tirupati
# Format: Narrative Policy Simulator (Scrollytelling)
# ==============================================================================

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time

# --- 1. PAGE CONFIGURATION & MOBILE-FIRST CSS ---
st.set_page_config(page_title="Digital Fiscalism Simulator", layout="centered", initial_sidebar_state="collapsed")

# Minimalist CSS that respects both Light and Dark modes on mobile
st.markdown("""
    <style>
    h1, h2, h3, p, div {font-family: 'Georgia', serif;}
    .story-text {font-size: 1.2rem; line-height: 1.6; margin-bottom: 20px;}
    .highlight {color: #d1383c; font-weight: bold;}
    .alert-box {background-color: rgba(209, 56, 60, 0.1); border-left: 5px solid #d1383c; padding: 15px; margin-bottom: 20px;}
    .stButton>button {width: 100%; height: 60px; font-size: 18px; font-weight: bold; background-color: #002147; color: white; border-radius: 8px;}
    .stButton>button:hover {background-color: #003366; color: white;}
    </style>
""", unsafe_allow_html=True)

# --- 2. STATE MANAGEMENT (THE "ROOMS") ---
if 'step' not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

def reset_sim():
    st.session_state.step = 1

# --- 3. BACKGROUND DATA ---
data = {
    'State': ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh', 'Madhya Pradesh', 'Punjab', 'Assam', 'Bihar', 'Jharkhand'],
    'Tier': [1, 1, 1, 2, 2, 2, 3, 3, 3],
    'Base_Readiness': [85, 82, 80, 55, 52, 60, 35, 30, 28] 
}
df = pd.DataFrame(data)

# ==============================================================================
# ROOM 1: THE SETUP
# ==============================================================================
if st.session_state.step == 1:
    st.title("The Filing Day Simulator")
    st.markdown("<div class='story-text'>Welcome to India's digital economy. Imagine you are a mid-sized supplier. You generate e-way bills daily and must file your GST returns by the 20th of every month to avoid heavy penalties.</div>", unsafe_allow_html=True)
    
    st.markdown("### Step 1: Establish Your Business")
    
    selected_state = st.selectbox("Where is your business located?", df['State'].tolist())
    st.session_state.user_state = selected_state
    
    business_size = st.select_slider(
        "What is your monthly transaction volume (E-Way Bills)?",
        options=["Small (10k/mo)", "Medium (250k/mo)", "Large (1M+/mo)"],
        value="Medium (250k/mo)"
    )
    st.session_state.business_size = business_size
    
    vol_map = {"Small (10k/mo)": 10000, "Medium (250k/mo)": 250000, "Large (1M+/mo)": 1500000}
    st.session_state.ewb_vol = vol_map[business_size]
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Fast Forward to the 20th ->", on_click=next_step)

# ==============================================================================
# ROOM 2: THE SHOCK
# ==============================================================================
elif st.session_state.step == 2:
    st.title("GST Filing Day")
    st.markdown(f"<div class='story-text'>It is 2:00 PM on the 20th. You sit down in your office in <b>{st.session_state.user_state}</b> to log into the GSTN portal.</div>", unsafe_allow_html=True)
    
    with st.spinner("Connecting to GSTN Portal..."):
        time.sleep(1.5)
    
    st.markdown("""
        <div class='alert-box'>
            <h3 style='color: #d1383c; margin-top: 0;'>⚠️ NETWORK DISRUPTION DETECTED</h3>
            <p>Due to local unrest, district authorities have invoked Section 144. All mobile internet and broadband services have been indefinitely suspended in your area.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='story-text'>You cannot reach your CA. The OTP for login will not deliver to your phone. The deadline is at midnight.</div>", unsafe_allow_html=True)
    
    st.button("Analyze My Vulnerability ->", on_click=next_step)

# ==============================================================================
# ROOM 3: THE FALLOUT & THE SCIENCE
# ==============================================================================
elif st.session_state.step == 3:
    st.title("Your Institutional Vulnerability")
    
    state_data = df[df['State'] == st.session_state.user_state].iloc[0]
    tier = state_data['Tier']
    readiness = state_data['Base_Readiness']
    
    base = {1: 2.5, 2: 5.5, 3: 9.0}[tier]
    bonus = ((readiness - 50) / 50) * 2.0 if readiness > 50 else 0
    struct_risk = max(0.5, base - bonus)
    
    causal_shock = 2.5 
    if st.session_state.ewb_vol < 500000:
         causal_shock += 3.0 
            
    total_risk = struct_risk + causal_shock
    
    st.markdown(f"<div class='story-text'>Because you are operating a {st.session_state.business_size.split(' ')[0].lower()} business in <b>{st.session_state.user_state}</b>, the econometric model predicts your probability of compliance failure is <span class='highlight'>{total_risk:.1f}%</span>.</div>", unsafe_allow_html=True)
    
    if total_risk > 10:
        st.error("You are in a high-friction zone. Your reliance on basic mobile infrastructure makes you disproportionately vulnerable to administrative shocks. You will likely default and face late fees.")
    else:
        st.success("You are in a resilient zone. Because your state has strong broadband penetration, you likely have fixed-line backups and can weather the mobile network shock.")

    st.markdown("### The Econometric Breakdown")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=['Your Compliance Friction'], x=[struct_risk], name='Baseline Infrastructure Gap', orientation='h', marker=dict(color='#002147')
    ))
    fig.add_trace(go.Bar(
        y=['Your Compliance Friction'], x=[causal_shock], name='Impact of Internet Shutdown', orientation='h', marker=dict(color='#d1383c')
    ))
    
    fig.update_layout(
        barmode='stack', height=300, 
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Georgia")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("*This simulation uses Two-Way Fixed Effects (TWFE) modeling and Fractional Logit estimations based on 70 months of GST panel data.*")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("↺ Start New Simulation", on_click=reset_sim)
