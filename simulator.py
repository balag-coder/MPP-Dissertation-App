# ==============================================================================
# DECODING DIGITAL FISCALISM: THE POLICY SIMULATOR
# Author: Balaji K., MPP, IIT Tirupati
# Format: Interactive Econometric Narrative
# ==============================================================================

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time

# --- 1. PAGE CONFIGURATION & ELITE CSS ---
st.set_page_config(page_title="Digital Fiscalism", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    h1, h2, h3, p, div {font-family: 'Georgia', serif;}
    .story-text {font-size: 1.15rem; line-height: 1.7; margin-bottom: 20px; color: #2c3e50;}
    .quote-block {border-left: 4px solid #002147; padding-left: 15px; font-style: italic; color: #555; margin-bottom: 20px;}
    .highlight {color: #d1383c; font-weight: bold;}
    .highlight-blue {color: #002147; font-weight: bold;}
    .metric-box {background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 8px; text-align: center; margin-top: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    .metric-title {font-size: 0.9rem; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;}
    .metric-value {font-size: 2rem; font-weight: bold; color: #d1383c; margin: 0;}
    .stButton>button {width: 100%; height: 60px; font-size: 18px; font-weight: bold; background-color: #002147; color: white; border-radius: 4px; border: none;}
    .stButton>button:hover {background-color: #003366; color: white;}
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

# --- 3. DISSERTATION DATA (STATE TAX BASES & EWBs) ---
# Approximations for simulation purposes based on panel data means
data = {
    'State': ['Jammu and Kashmir', 'Manipur', 'Nagaland', 'Assam', 'Haryana', 'Punjab', 'Madhya Pradesh', 'Tamil Nadu', 'Maharashtra'],
    'Taxpayer_Base': [110000, 35000, 20000, 250000, 500000, 400000, 600000, 1100000, 1600000],
    'Monthly_EWB': [150000, 80000, 45000, 300000, 2500000, 1800000, 1500000, 8000000, 20000000]
}
df = pd.DataFrame(data)
df['Log_EWB'] = np.log(df['Monthly_EWB'])

# ==============================================================================
# ROOM 1: THE PREMISE
# ==============================================================================
if st.session_state.step == 1:
    st.title("Decoding Digital Fiscalism")
    st.markdown("<div class='quote-block'>“The fiscal state's extraction is preserved. The compliance cost of that preservation lands on the taxpayer.” — <i>Balaji K.</i></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='story-text'>India’s Goods and Services Tax (GST) is a legally mandatory, exclusively digital fiscal system. You cannot file on paper. To claim input tax credits and stay compliant, suppliers must upload their <b>GSTR-1</b> outward supply data by the <b>11th of every month</b>.</div>", unsafe_allow_html=True)
    
    st.markdown("### Step 1: Select Your Jurisdiction")
    st.markdown("<div class='story-text'>Different states have different levels of institutional capacity, proxied by formal economic activity (E-Way Bills). Let's see how your state handles a digital shock.</div>", unsafe_allow_html=True)
    
    selected_state = st.selectbox("Select State to Analyze:", df['State'].tolist(), index=1) # Default Manipur
    st.session_state.user_state = selected_state
    
    disruption_days = st.slider("Set Disruption Duration (Days):", min_value=1, max_value=15, value=5)
    st.session_state.days = disruption_days
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Trigger Telecom Suspension ->", on_click=next_step)

# ==============================================================================
# ROOM 2: THE SCIENCE (MARGINAL EFFECT CURVE)
# ==============================================================================
elif st.session_state.step == 2:
    state_data = df[df['State'] == st.session_state.user_state].iloc[0]
    log_ewb = state_data['Log_EWB']
    
    st.title("Heterogeneous Administrative Resilience")
    st.markdown(f"<div class='story-text'>A <b>{st.session_state.days}-day</b> mobile internet suspension has been ordered in <b>{st.session_state.user_state}</b> right before the GSTR-1 deadline. <br><br>Does this cause widespread late filing? According to our Two-Way Fixed Effects (TWFE) model, <b>it depends entirely on the state's economic density.</b></div>", unsafe_allow_html=True)
    
    # --- RENDER FIGURE 6 (MARGINAL EFFECT CURVE) ---
    x_vals = np.linspace(8, 16, 100)
    y_vals = 0.0144 - (0.0011 * x_vals) # Beta1 + Beta2*logEWB
    
    fig = go.Figure()
    # The Zero Line
    fig.add_trace(go.Scatter(x=[8, 16], y=[0, 0], mode='lines', line=dict(color='black', dash='dash'), name='Zero Effect'))
    # The Marginal Effect Line
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#8b0000', width=3), name='Marginal Effect'))
    
    # Highlight the specific state
    state_y = 0.0144 - (0.0011 * log_ewb)
    fig.add_trace(go.Scatter(x=[log_ewb], y=[state_y], mode='markers+text', 
                             marker=dict(size=15, color='#002147'),
                             text=[f"<b>{st.session_state.user_state}</b>"], textposition="top center", name='Selected State'))
    
    # Threshold Line (13.09)
    fig.add_vline(x=13.09, line_dash="dot", line_color="grey")
    fig.add_annotation(x=13.09, y=0.01, text="Resilience Threshold (488k EWBs)", showarrow=False, textangle=-90, xshift=-15)
    
    fig.update_layout(
        height=400, margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="Log E-Way Bill Volume", yaxis_title="Marginal Effect on Late Filing",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(family="Georgia"),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
        <div style='font-size: 0.95rem; color: #555; text-align: justify;'>
        <b>The Econometrics:</b> The marginal effect of a disruption crosses zero at log EWB = 13.09. States above this line (like Maharashtra) have the practitioner networks, ERP systems, and broadband redundancy to buffer the shock. States below this line suffer severe compliance friction.
        </div><br>
    """, unsafe_allow_html=True)
    
    st.button("Calculate The Economic Cost ->", on_click=next_step)

# ==============================================================================
# ROOM 3: THE COST OF DIGITAL FISCALISM
# ==============================================================================
elif st.session_state.step == 3:
    state_data = df[df['State'] == st.session_state.user_state].iloc[0]
    log_ewb = state_data['Log_EWB']
    tax_base = state_data['Taxpayer_Base']
    days = st.session_state.days
    
    # --- ECONOMETRIC MATH ---
    # Effect per day = Beta1 + Beta2*logEWB. If negative, clamp to 0 (institutional buffering).
    effect_per_day = max(0, 0.0144 - (0.0011 * log_ewb))
    total_percentage_increase = effect_per_day * days
    
    # Dynamic Financials
    new_late_filers = int(tax_base * total_percentage_increase)
    late_fee_per_day = 50 # Standard CGST+SGST late fee per day
    total_fees_extracted = new_late_filers * late_fee_per_day * days
    
    st.title("The Institutional Fallout")
    
    if total_percentage_increase > 0:
        st.markdown(f"<div class='story-text'>Because <b>{st.session_state.user_state}</b> sits below the digital resilience threshold, this {days}-day disruption actively breaks the compliance process. The state’s aggregate revenue is unaffected—the penalty regime ensures eventual payment—but the burden falls entirely on the MSMEs.</div>", unsafe_allow_html=True)
        
        st.markdown("### Estimated Disruption Penalty")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>Involuntary Late Filers</div><p class='metric-value'>{new_late_filers:,}</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-box'><div class='metric-title'>Late Fees Extracted</div><p class='metric-value'>₹{total_fees_extracted:,.0f}</p></div>", unsafe_allow_html=True)
            
        st.markdown(f"""
            <br>
            <div style='font-size: 1rem; color: #555;'>
            <b>The Mundlak Reality:</b> You are looking at the <i>Within-State Causal Effect</i>. The state government effectively taxes its own citizens ₹{total_fees_extracted:,.0f} for an infrastructural failure caused by the state itself, simply because these MSMEs could not file GSTR-1 on the 11th.
            </div>
            <hr>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown(f"<div class='story-text'><b>{st.session_state.user_state}</b> sits well above the resilience threshold.</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='metric-box'><div class='metric-title'>Involuntary Late Filers</div><p class='metric-value' style='color:#002147;'>0</p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='metric-box'><div class='metric-title'>System Status</div><p class='metric-value' style='color:#002147; font-size:1.5rem; padding-top:10px;'>BUFFERED</p></div>", unsafe_allow_html=True)
            
        st.markdown("""
            <br>
            <div style='font-size: 1rem; color: #555;'>
            <b>Intertemporal Substitution:</b> In high-capacity states, the institutional ecosystem (large tax firms, fixed-line broadband, automated ERPs) absorbs the shock. Revenue and compliance remain stable. The system works—but only for the digitally privileged.
            </div>
            <hr>
        """, unsafe_allow_html=True)

    st.markdown("### Policy Recommendation")
    st.markdown("<div class='story-text'><b>Disrupt-and-Defer:</b> We do not need to change the internet shutdown laws to fix this. Section 168A of the CGST Act already allows for deadline extensions during force majeure events. An API link between telecom suspension orders and the GSTN portal could automatically waive late fees for jurisdictions in the vulnerability zone.</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("↺ Restart Simulation", on_click=reset_sim)
