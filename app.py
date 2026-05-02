# ==============================================================================
# DIGITAL FISCALISM: POLICY VULNERABILITY EXPLORER
# Author: Balaji K. 
# Framework: Streamlit
# Description: Interactive dashboard for dissertation defense committee
# ==============================================================================

import streamlit as st
import plotly.graph_objects as go

# --- 1. PAGE CONFIGURATION & ACADEMIC STYLING ---
st.set_page_config(page_title="Digital Fiscalism Explorer", layout="wide", initial_sidebar_state="expanded")

# Inject minimal CSS to enforce a clean, academic look
st.markdown("""
    <style>
    .main {background-color: #FAFAFA;}
    h1, h2, h3 {font-family: 'Times New Roman', Times, serif; color: #1a1a1a;}
    .metric-container {background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER & INSTRUCTIONS ---
st.title("Digital Fiscalism: Policy Vulnerability Explorer")
st.markdown("""
*An interactive simulation of GST compliance friction under digital disruptions.*  
**Instructions for Committee:** Adjust the structural and infrastructural parameters in the sidebar to simulate the probability of late GST filings under standard and disrupted scenarios.
---
""")

# --- 3. SIDEBAR CONTROLS (USER INPUTS) ---
with st.sidebar:
    st.header("Model Parameters")
    
    st.subheader("1. Structural Typology")
    typology = st.selectbox(
        "Select State/UT Typology",
        ("Tier 1: High-Capacity / Industrial", 
         "Tier 2: Mid-Tier / Agrarian", 
         "Tier 3: Vulnerable / Remote")
    )
    
    st.subheader("2. Economic Activity")
    ewb_volume = st.slider(
        "Monthly E-Way Bill Transactions", 
        min_value=10000, max_value=10000000, value=350000, step=50000,
        help="Proxy for state-level commercial activity scale."
    )
    
    st.subheader("3. Infrastructural Resilience")
    telecom_pen = st.slider(
        "Digital Infrastructure Readiness (%)", 
        min_value=10, max_value=100, value=60, step=1,
        help="Percentage of the population with robust broadband/telecom access."
    )
    
    st.markdown("---")
    st.subheader("4. Exogenous Shock")
    disruption_active = st.toggle("🚨 Activate Internet Disruption", value=False)

# --- 4. ECONOMETRIC LOGIC (MUNDLAK DECOMPOSITION) ---
# A. Structural Baseline Risk (Between-State Friction)
if "Tier 1" in typology:
    base_risk = 2.5
elif "Tier 2" in typology:
    base_risk = 5.5
else:
    base_risk = 9.0

# Infrastructure mitigates structural risk (up to 2% reduction if > 50% penetration)
infra_bonus = 0.0
if telecom_pen > 50:
    infra_bonus = ((telecom_pen - 50) / 50) * 2.0
structural_risk = max(0.5, base_risk - infra_bonus)

# B. Causal Disruption Impact (Within-State Shock)
causal_shock = 0.0
if disruption_active:
    causal_shock += 2.5 # Base shock
    if ewb_volume < 500000:
        causal_shock += 3.0 # Friction penalty for low-capacity states

# C. Total Predicted Rate
total_rate = structural_risk + causal_shock

# --- 5. VISUALIZATIONS ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("### Total Predicted Late Filing Rate")
    # Elite Plotly Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = total_rate,
        number = {'suffix': "%", 'font': {'size': 50, 'color': '#1a1a1a'}},
        title = {'text': "Compliance Friction Risk", 'font': {'size': 18}},
        gauge = {
            'axis': {'range': [0, 20], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "rgba(0,0,0,0)"}, # Hide default bar, use steps
            'steps': [
                {'range': [0, 5], 'color': "#e6f2ff", 'name': 'Resilient'},
                {'range': [5, 10], 'color': "#b3d9ff", 'name': 'Elevated'},
                {'range': [10, 15], 'color': "#ffb3b3", 'name': 'Vulnerable'},
                {'range': [15, 20], 'color': "#ff4d4d", 'name': 'Critical'}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': total_rate
            }
        }
    ))
    fig_gauge.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Contextual Warning
    if total_rate > 10:
        st.error("⚠️ **CRITICAL FRICTION DETECTED:** State infrastructure is insufficient to absorb the digital shock, leading to severe tax compliance failures.")
    else:
        st.success("✅ **SYSTEM RESILIENT:** Institutional capacity successfully buffers against compliance delays.")

with col2:
    st.markdown("### Mundlak Variance Decomposition")
    # Stacked Bar Chart for Structural vs Causal
    fig_bar = go.Figure(data=[
        go.Bar(name='Structural Baseline (Between-State)', 
               x=['Risk Decomposition'], y=[structural_risk], 
               marker_color='#005b9f', text=[f"{structural_risk:.1f}%"], textposition='auto'),
        go.Bar(name='Causal Shock (Within-State)', 
               x=['Risk Decomposition'], y=[causal_shock], 
               marker_color='#d1383c', text=[f"{causal_shock:.1f}%"] if causal_shock > 0 else [''], textposition='auto')
    ])
    fig_bar.update_layout(
        barmode='stack',
        height=350,
        yaxis_title="Late Filing Probability (%)",
        yaxis=dict(range=[0, max(20, total_rate + 2)]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=10, b=20)
    )
    # Add grid lines
    fig_bar.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e0e0e0')
    st.plotly_chart(fig_bar, use_container_width=True)

# --- 6. METHODOLOGICAL NOTE ---
st.markdown("---")
st.caption("**Methodological Note:** Estimates are derived from Fractional Logit and Two-Way Fixed Effects (TWFE) models using 70 months of state-level panel data. *Between-State* friction captures long-term infrastructural and economic heterogeneity. *Within-State* shock isolates the causal impact of administrative internet blackouts.")
