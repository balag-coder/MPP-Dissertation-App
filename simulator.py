# ==============================================================================
# DECODING DIGITAL FISCALISM: THE POLICY SIMULATOR
# Author: Balaji K., MPP, IIT Tirupati
# FINAL RESEARCH-GRADE VERSION
# ==============================================================================

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="Decoding Digital Fiscalism",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# ELITE CSS STYLING
# ==============================================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Georgia', serif;
    background-color: #fcfcfc;
}

h1 {
    font-size: 3.4rem !important;
    color: #232736;
    line-height: 1.1;
    margin-bottom: 0.7rem;
}

h2 {
    font-size: 2.3rem !important;
    color: #232736;
    margin-top: 2rem;
}

h3 {
    color: #232736;
}

.story-text {
    font-size: 1.18rem;
    line-height: 1.85;
    color: #34495e;
    margin-bottom: 1.5rem;
}

.quote-block {
    border-left: 5px solid #002147;
    padding-left: 18px;
    font-style: italic;
    color: #555;
    margin-bottom: 2rem;
    font-size: 1.15rem;
}

.metric-box {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 22px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.04);
}

.metric-title {
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #777;
    margin-bottom: 10px;
}

.metric-value {
    font-size: 2.2rem;
    font-weight: bold;
    color: #b22222;
}

.buffer-value {
    font-size: 1.7rem;
    font-weight: bold;
    color: #002147;
}

.stButton > button {
    width: 100%;
    height: 58px;
    font-size: 18px;
    font-weight: bold;
    background-color: #002147;
    color: white;
    border-radius: 6px;
    border: none;
}

.stButton > button:hover {
    background-color: #003366;
    color: white;
}

hr {
    border: none;
    height: 1px;
    background: linear-gradient(to right,
        rgba(0,0,0,0),
        rgba(0,0,0,0.2),
        rgba(0,0,0,0));
    margin-top: 2rem;
    margin-bottom: 2rem;
}

.small-note {
    font-size: 0.92rem;
    color: #666;
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE
# ==============================================================================

if "step" not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

def reset_sim():
    st.session_state.step = 1

# ==============================================================================
# MASTER STATE DATASET
# ==============================================================================

state_data = {
    "State": [
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Bihar",
        "Chhattisgarh",
        "Goa",
        "Gujarat",
        "Haryana",
        "Himachal Pradesh",
        "Jharkhand",
        "Karnataka",
        "Kerala",
        "Madhya Pradesh",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Punjab",
        "Rajasthan",
        "Sikkim",
        "Tamil Nadu",
        "Telangana",
        "Tripura",
        "Uttar Pradesh",
        "Uttarakhand",
        "West Bengal",
        "Jammu and Kashmir"
    ],

    "Taxpayer_Base": [
        750000,
        50000,
        250000,
        500000,
        220000,
        90000,
        1400000,
        500000,
        120000,
        180000,
        1600000,
        850000,
        600000,
        1800000,
        35000,
        40000,
        25000,
        20000,
        450000,
        400000,
        700000,
        15000,
        1100000,
        950000,
        30000,
        2200000,
        180000,
        950000,
        110000
    ],

    "Monthly_EWB": [
        3000000,
        50000,
        300000,
        450000,
        350000,
        200000,
        12000000,
        2500000,
        120000,
        250000,
        10000000,
        3500000,
        1500000,
        20000000,
        80000,
        60000,
        30000,
        45000,
        1200000,
        1800000,
        2500000,
        25000,
        8000000,
        6000000,
        40000,
        15000000,
        300000,
        5000000,
        150000
    ]
}

df = pd.DataFrame(state_data)

# ==============================================================================
# ECONOMETRIC TRANSFORMATION
# ==============================================================================

df["Log_EWB"] = np.log(df["Monthly_EWB"])

# TWFE Coefficients
BETA_1 = 0.0144
BETA_2 = -0.0011

# ==============================================================================
# ROOM 1 — INTRODUCTION
# ==============================================================================

if st.session_state.step == 1:

    st.title("Decoding Digital Fiscalism")

    st.markdown("""
    <div class='quote-block'>
    “The fiscal state's extraction is preserved.
    The compliance cost of that preservation lands on the taxpayer.”
    — <i>Balaji K.</i>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='story-text'>
    India’s GST system is a legally mandatory digital tax infrastructure.
    Firms cannot file manually. Every month, suppliers must upload
    GSTR-1 outward supply data before the statutory deadline.

    But what happens when the digital infrastructure itself collapses?
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Select Your Jurisdiction")

    st.markdown("""
    <div class='story-text'>
    Different Indian states possess radically different levels of
    institutional resilience. This simulator estimates how telecom
    disruptions affect GST compliance across heterogeneous economic systems.
    </div>
    """, unsafe_allow_html=True)

    selected_state = st.selectbox(
        "Choose State",
        sorted(df["State"].tolist()),
        index=14
    )

    st.session_state.user_state = selected_state

    disruption_days = st.slider(
        "Telecom Suspension Duration (Days)",
        min_value=1,
        max_value=15,
        value=5
    )

    st.session_state.days = disruption_days

    st.markdown("<br>", unsafe_allow_html=True)

    st.button(
        "Trigger Telecom Suspension →",
        on_click=next_step
    )

# ==============================================================================
# ROOM 2 — ECONOMETRIC VISUALIZATION
# ==============================================================================

elif st.session_state.step == 2:

    state_row = df[df["State"] == st.session_state.user_state].iloc[0]

    real_ewb = state_row["Monthly_EWB"]

    log_ewb = np.log(real_ewb)

    state_effect = BETA_1 + (BETA_2 * log_ewb)

    st.title("Heterogeneous Administrative Resilience")

    st.markdown(f"""
    <div class='story-text'>
    A <b>{st.session_state.days}-day</b> mobile internet suspension
    has been imposed in <b>{st.session_state.user_state}</b>
    immediately before the GST filing deadline.

    According to the Two-Way Fixed Effects (TWFE) model,
    the impact depends entirely on the state's underlying
    economic density and institutional resilience.
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # PLOT
    # ==========================================================================

    real_x = np.geomspace(50000, 25000000, 250)

    log_x = np.log(real_x)

    y_vals = BETA_1 + (BETA_2 * log_x)

    fig = go.Figure()

    # Marginal effect curve
    fig.add_trace(go.Scatter(
        x=real_x,
        y=y_vals,
        mode='lines',
        line=dict(color='#8b0000', width=4),
        hovertemplate=
        "<b>EWB Volume:</b> %{x:,.0f}<br>" +
        "<b>Marginal Effect:</b> %{y:.4f}<extra></extra>"
    ))

    # Zero effect line
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="black"
    )

    # Resilience threshold
    threshold_real = np.exp(13.09)

    fig.add_vline(
        x=threshold_real,
        line_dash="dot",
        line_color="gray"
    )

    fig.add_annotation(
        x=threshold_real,
        y=0.012,
        text="Resilience Threshold",
        showarrow=False,
        textangle=-90,
        font=dict(size=12)
    )

    # State point
    fig.add_trace(go.Scatter(
        x=[real_ewb],
        y=[state_effect],
        mode='markers+text',
        marker=dict(
            size=16,
            color='#002147'
        ),
        text=[st.session_state.user_state],
        textposition="top center",
        hovertemplate=
        "<b>%{text}</b><br>" +
        "Monthly EWBs: %{x:,.0f}<br>" +
        "Marginal Effect: %{y:.4f}<extra></extra>"
    ))

    fig.update_xaxes(
        type="log",
        tickvals=[
            50000,
            100000,
            500000,
            1000000,
            5000000,
            10000000,
            20000000
        ],
        ticktext=[
            "50K",
            "100K",
            "500K",
            "1M",
            "5M",
            "10M",
            "20M"
        ]
    )

    fig.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        font=dict(family="Georgia"),
        xaxis_title="Monthly E-Way Bill Volume",
        yaxis_title="Marginal Effect on Late Filing"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("""
    <div class='small-note'>
    <b>Interpretation:</b>
    States positioned left of the resilience threshold lack sufficient
    digital redundancy, practitioner ecosystems, and institutional
    buffering capacity. As a result, telecom disruptions substantially
    increase involuntary late filing.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button(
        "Calculate Institutional Cost →",
        on_click=next_step
    )

# ==============================================================================
# ROOM 3 — ECONOMIC COST
# ==============================================================================

elif st.session_state.step == 3:

    state_row = df[df["State"] == st.session_state.user_state].iloc[0]

    log_ewb = state_row["Log_EWB"]

    tax_base = state_row["Taxpayer_Base"]

    days = st.session_state.days

    # ==========================================================================
    # ECONOMETRIC CALCULATION
    # ==========================================================================

    effect_per_day = max(
        0,
        BETA_1 + (BETA_2 * log_ewb)
    )

    total_percentage_increase = effect_per_day * days

    new_late_filers = int(
        tax_base * total_percentage_increase
    )

    # ==========================================================================
    # LEGAL LATE FEE CALCULATION
    # ==========================================================================

    # Section 47 CGST
    # ₹25 CGST + ₹25 SGST = ₹50/day

    late_fee_per_day = 50

    # Realistic recovery adjustment
    average_actual_delay = max(
        1,
        round(days * 0.45)
    )

    total_fees_extracted = (
        new_late_filers
        * late_fee_per_day
        * average_actual_delay
    )

    # ==========================================================================
    # PAGE CONTENT
    # ==========================================================================

    st.title("The Institutional Fallout")

    if total_percentage_increase > 0:

        st.markdown(f"""
        <div class='story-text'>
        Because <b>{st.session_state.user_state}</b>
        sits below the resilience threshold,
        this disruption directly fractures the compliance process.

        Revenue collection eventually recovers,
        but the institutional burden is transferred
        entirely onto small taxpayers and MSMEs.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## Estimated Disruption Burden")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>
                Involuntary Late Filers
                </div>

                <div class='metric-value'>
                {new_late_filers:,}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-title'>
                Estimated Late Fees
                </div>

                <div class='metric-value'>
                ₹{total_fees_extracted:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.caption(f"""
        Estimated burden assumes:
        • ₹50/day statutory late fee under Section 47 CGST Act
        • average compliance recovery after disruption
        • no waiver intervention
        • no NIL-return adjustment
        • average delay of {average_actual_delay} days
        """)

        st.markdown("""
        <hr>

        <div class='story-text'>
        <b>The Mundlak Reality:</b>
        The state preserves fiscal extraction despite infrastructural failure.
        The compliance burden is privatized onto citizens who are legally
        unable to comply during network disruption.
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown(f"""
        <div class='story-text'>
        <b>{st.session_state.user_state}</b>
        sits above the resilience threshold.

        Institutional buffering mechanisms absorb the disruption,
        preventing systemic late filing escalation.
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class='metric-box'>
                <div class='metric-title'>
                Involuntary Late Filers
                </div>

                <div class='buffer-value'>
                0
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class='metric-box'>
                <div class='metric-title'>
                Institutional Status
                </div>

                <div class='buffer-value'>
                BUFFERED
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("## Policy Recommendation")

    st.markdown("""
    <div class='story-text'>
    <b>Disrupt-and-Defer Framework:</b>

    Section 168A of the CGST Act already permits statutory deadline
    extensions during force majeure events.

    A machine-readable API linkage between telecom suspension orders
    and the GSTN architecture could automatically:

    • defer filing deadlines  
    • suspend penalty accumulation  
    • protect MSMEs from involuntary non-compliance  
    • preserve administrative legitimacy during digital disruptions
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button(
        "↺ Restart Simulation",
        on_click=reset_sim
    )
