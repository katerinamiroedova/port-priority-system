import streamlit as st
import pandas as pd
import numpy as np
import itertools
import plotly.graph_objects as go
from datetime import datetime


# ============================================================
# PORT PRIORITY
# Maritime Operations Decision Support System
# Version 4.0
# ============================================================

st.set_page_config(
    page_title="PORT PRIORITY",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# VISUAL SYSTEM
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 50% -10%,
            rgba(37, 108, 135, 0.20),
            transparent 52%
        ),
        linear-gradient(
            180deg,
            #07131c 0%,
            #081720 42%,
            #091923 100%
        );
    color: #e8f0f4;
}

/* subtle ocean layers */

.stApp::before {
    content: "";
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    height: 32vh;
    pointer-events: none;
    opacity: 0.12;
    background:
        repeating-linear-gradient(
            175deg,
            transparent 0px,
            transparent 27px,
            rgba(80, 180, 202, 0.20) 28px,
            transparent 29px
        );
    z-index: 0;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    position: relative;
    z-index: 1;
}

header[data-testid="stHeader"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #08131c 0%,
            #0a1821 100%
        );
    border-right: 1px solid #1d3542;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}


/* ============================================================
   TYPOGRAPHY
   ============================================================ */

.tech-label {
    font-family: 'DM Mono', monospace;
    color: #6d8997;
    font-size: 0.64rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.main-title {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.055em;
    line-height: 0.95;
    margin-top: 0.25rem;
    background:
        linear-gradient(
            90deg,
            #edf8fa 0%,
            #8ed4df 48%,
            #d8eef0 100%
        );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.main-subtitle {
    color: #7f98a5;
    font-size: 0.88rem;
    margin-top: 0.45rem;
}


/* ============================================================
   MARITIME HEADER
   ============================================================ */

.marine-header {
    position: relative;
    overflow: hidden;
    padding: 2rem 2.1rem 1.8rem 2.1rem;
    border: 1px solid #214252;
    background:
        linear-gradient(
            180deg,
            rgba(17, 53, 67, 0.55),
            rgba(7, 20, 29, 0.88)
        );
}

.marine-header::after {
    content: "";
    position: absolute;
    left: -5%;
    right: -5%;
    bottom: -24px;
    height: 70px;
    opacity: 0.28;
    background:
        radial-gradient(
            ellipse at 20% 50%,
            transparent 0 55%,
            rgba(91, 190, 207, 0.35) 56%,
            transparent 59%
        ),
        radial-gradient(
            ellipse at 70% 55%,
            transparent 0 55%,
            rgba(91, 190, 207, 0.25) 56%,
            transparent 59%
        );
    transform: rotate(-2deg);
}

.header-grid {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 2rem;
    align-items: center;
    position: relative;
    z-index: 2;
}

.system-status {
    text-align: right;
}

.status-live {
    color: #62d8c4;
    font-family: 'DM Mono', monospace;
    font-size: 0.69rem;
    letter-spacing: 0.09em;
}

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #62d8c4;
    box-shadow: 0 0 12px rgba(98,216,196,0.65);
    margin-right: 7px;
}


/* ============================================================
   LINES
   ============================================================ */

.rule {
    height: 1px;
    background:
        linear-gradient(
            90deg,
            transparent,
            #254554,
            transparent
        );
    margin: 1.4rem 0;
}


/* ============================================================
   METRICS
   ============================================================ */

.metric-box {
    background:
        linear-gradient(
            145deg,
            rgba(18, 35, 45, 0.92),
            rgba(10, 23, 31, 0.95)
        );
    border: 1px solid #1f3947;
    padding: 1rem 1.15rem;
    min-height: 105px;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.025);
}

.metric-label {
    color: #6d8997;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.metric-value {
    font-size: 1.65rem;
    font-weight: 600;
    margin-top: 0.35rem;
    color: #dcecef;
}

.metric-note {
    color: #637b88;
    font-size: 0.7rem;
    margin-top: 0.2rem;
}


/* ============================================================
   PANELS
   ============================================================ */

.panel {
    background:
        linear-gradient(
            145deg,
            rgba(13, 29, 38, 0.94),
            rgba(9, 20, 28, 0.96)
        );
    border: 1px solid #1d3542;
    padding: 1.15rem;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.02);
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.9rem;
}

.panel-title {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.035em;
}

.panel-code {
    color: #536d7a;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
}


/* ============================================================
   RECOMMENDATION
   ============================================================ */

.recommendation {
    border-left: 3px solid #62d8c4;
    background:
        linear-gradient(
            90deg,
            rgba(45, 130, 133, 0.12),
            rgba(10, 27, 33, 0.4)
        );
    padding: 1rem 1.1rem;
}

.recommendation-title {
    color: #62d8c4;
    font-family: 'DM Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.recommendation-main {
    font-size: 1.18rem;
    font-weight: 600;
    margin-top: 0.3rem;
}

.recommendation-text {
    color: #8196a1;
    font-size: 0.76rem;
    line-height: 1.55;
    margin-top: 0.35rem;
}


/* ============================================================
   ALERTS
   ============================================================ */

.alert-danger {
    border-left: 3px solid #d86c78;
    background: rgba(72, 24, 31, 0.28);
    padding: 0.9rem 1rem;
    color: #d8b9bd;
}

.alert-warning {
    border-left: 3px solid #d6b66c;
    background: rgba(73, 58, 25, 0.25);
    padding: 0.9rem 1rem;
    color: #cfc19c;
}

.alert-good {
    border-left: 3px solid #62d8c4;
    background: rgba(24, 70, 65, 0.20);
    padding: 0.9rem 1rem;
    color: #a9d8d0;
}


/* ============================================================
   VESSEL ROWS
   ============================================================ */

.vessel-row {
    display: grid;
    grid-template-columns: 42px 1fr 100px 90px;
    align-items: center;
    border-top: 1px solid #19303c;
    padding: 0.75rem 0;
}

.vessel-rank {
    font-family: 'DM Mono', monospace;
    color: #4e6875;
    font-size: 0.7rem;
}

.vessel-name {
    font-weight: 600;
    font-size: 0.82rem;
}

.vessel-type {
    color: #667f8b;
    font-size: 0.67rem;
    margin-top: 0.12rem;
}

.vessel-number {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #a9bac3;
    text-align: right;
}

.priority-high {
    color: #62d8c4;
}

.priority-medium {
    color: #d6b66c;
}

.priority-low {
    color: #6d808b;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    border-radius: 2px;
    border: 1px solid #2b4a59;
    background: #10232d;
    color: #d7e4e8;
    font-weight: 500;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #62d8c4;
    color: #62d8c4;
    background: #122c35;
}


/* ============================================================
   TABS
   ============================================================ */

button[data-baseweb="tab"] {
    font-size: 0.72rem;
    font-weight: 500;
    color: #708792;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #62d8c4;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="select"] > div {
    background: #0d1d26;
    border-color: #274352;
}

.stSlider label,
.stNumberInput label,
.stSelectbox label,
.stTextArea label {
    color: #7d939e !important;
    font-size: 0.72rem !important;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    color: #49616c;
    font-family: 'DM Mono', monospace;
    font-size: 0.59rem;
    letter-spacing: 0.05em;
    line-height: 1.7;
    margin-top: 1.5rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "decision_log" not in st.session_state:
    st.session_state.decision_log = []

if "override_sequence" not in st.session_state:
    st.session_state.override_sequence = None


# ============================================================
# VESSEL DATA
# ============================================================

vessels = pd.DataFrame([
    {
        "Vessel": "Ocean Star",
        "Type": "Cruise liner",
        "Passengers": 2840,
        "Cargo": 5,
        "Economic": 0.42,
        "Waiting": 3.3,
        "Service": 35,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": True,
        "Perishable": False,
        "Fuel": 65,
        "MaxWind": 32,
        "MaxWaves": 4.5
    },
    {
        "Vessel": "Pacific Horizon",
        "Type": "Cruise liner",
        "Passengers": 4100,
        "Cargo": 5,
        "Economic": 0.56,
        "Waiting": 1.4,
        "Service": 40,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel": 70,
        "MaxWind": 30,
        "MaxWaves": 4.0
    },
    {
        "Vessel": "MedExpress",
        "Type": "Medical cargo",
        "Passengers": 0,
        "Cargo": 100,
        "Economic": 0.75,
        "Waiting": 0.8,
        "Service": 25,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": True,
        "Fuel": 40,
        "MaxWind": 40,
        "MaxWaves": 5.5
    },
    {
        "Vessel": "Baltic Trader",
        "Type": "Container ship",
        "Passengers": 0,
        "Cargo": 55,
        "Economic": 1.35,
        "Waiting": 2.2,
        "Service": 50,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel": 50,
        "MaxWind": 38,
        "MaxWaves": 5.0
    },
    {
        "Vessel": "Aurora",
        "Type": "Tanker",
        "Passengers": 0,
        "Cargo": 70,
        "Economic": 1.10,
        "Waiting": 1.7,
        "Service": 45,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel": 95,
        "MaxWind": 34,
        "MaxWaves": 4.5
    },
    {
        "Vessel": "Northern Wind",
        "Type": "Ferry",
        "Passengers": 720,
        "Cargo": 35,
        "Economic": 0.18,
        "Waiting": 4.1,
        "Service": 20,
        "Tugs": 0,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel": 65,
        "MaxWind": 36,
        "MaxWaves": 5.0
    },
    {
        "Vessel": "FreshLine",
        "Type": "Refrigerated cargo",
        "Passengers": 0,
        "Cargo": 80,
        "Economic": 0.82,
        "Waiting": 2.8,
        "Service": 30,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": True,
        "Fuel": 55,
        "MaxWind": 37,
        "MaxWaves": 5.0
    },
    {
        "Vessel": "Atlas Heavy",
        "Type": "Heavy cargo",
        "Passengers": 0,
        "Cargo": 65,
        "Economic": 1.55,
        "Waiting": 5.2,
        "Service": 60,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel": 35,
        "MaxWind": 35,
        "MaxWaves": 4.5
    }
])


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    '<div class="tech-label">ENVIRONMENTAL CONDITIONS</div>',
    unsafe_allow_html=True
)

wind = st.sidebar.slider(
    "Wind speed",
    5, 55, 28
)

waves = st.sidebar.slider(
    "Wave height",
    0.5, 8.0, 4.2, 0.1
)

visibility = st.sidebar.slider(
    "Visibility",
    0.2, 15.0, 1.8, 0.1
)

deterioration = st.sidebar.slider(
    "Weather deterioration",
    10, 180, 35
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    '<div class="tech-label">PORT CAPACITY</div>',
    unsafe_allow_html=True
)

berths = st.sidebar.number_input(
    "Available berths",
    min_value=1,
    max_value=6,
    value=3
)

tugs = st.sidebar.number_input(
    "Available tugboats",
    min_value=0,
    max_value=6,
    value=2
)

pilots = st.sidebar.number_input(
    "Available pilots",
    min_value=0,
    max_value=6,
    value=1
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    '<div class="tech-label">DECISION MODEL</div>',
    unsafe_allow_html=True
)

safety_weight = st.sidebar.slider(
    "Safety",
    0, 100, 30
)

passenger_weight = st.sidebar.slider(
    "Passenger impact",
    0, 100, 15
)

cargo_weight = st.sidebar.slider(
    "Cargo criticality",
    0, 100, 15
)

economic_weight = st.sidebar.slider(
    "Economic impact",
    0, 100, 15
)

waiting_weight = st.sidebar.slider(
    "Waiting time",
    0, 100, 10
)

weather_weight = st.sidebar.slider(
    "Weather window",
    0, 100, 15
)

weight_sum = (
    safety_weight +
    passenger_weight +
    cargo_weight +
    economic_weight +
    waiting_weight +
    weather_weight
)


# ============================================================
# WEATHER MODEL
# ============================================================

def weather_risk(wind, waves, visibility):

    wind_score = np.clip(
        (wind - 10) / 40 * 100,
        0,
        100
    )

    wave_score = np.clip(
        (waves - 0.5) / 7.5 * 100,
        0,
        100
    )

    visibility_score = np.clip(
        (8 - visibility) / 8 * 100,
        0,
        100
    )

    return round(
        0.4 * wind_score +
        0.4 * wave_score +
        0.2 * visibility_score,
        1
    )


def weather_label(risk):

    if risk >= 80:
        return "CRITICAL"

    if risk >= 60:
        return "HIGH"

    if risk >= 35:
        return "MODERATE"

    return "LOW"


current_risk = weather_risk(
    wind,
    waves,
    visibility
)

risk_label = weather_label(
    current_risk
)


# ============================================================
# NORMALIZATION
# ============================================================

def normalize(series):

    low = series.min()
    high = series.max()

    if high == low:
        return pd.Series(
            [50] * len(series),
            index=series.index
        )

    return (
        (series - low) /
        (high - low)
    ) * 100


vessels["PassengerScore"] = normalize(
    vessels["Passengers"]
)

vessels["EconomicScore"] = normalize(
    vessels["Economic"]
)

vessels["WaitingScore"] = normalize(
    vessels["Waiting"]
)


# ============================================================
# SAFETY FILTER
# ============================================================

vessels["SafeNow"] = vessels.apply(
    lambda row:
        wind <= row["MaxWind"]
        and waves <= row["MaxWaves"],
    axis=1
)

vessels["ResourcesAvailable"] = vessels.apply(
    lambda row:
        row["Tugs"] <= tugs
        and row["Pilots"] <= pilots,
    axis=1
)

vessels["Eligible"] = (
    vessels["SafeNow"] &
    vessels["ResourcesAvailable"]
)


# ============================================================
# WEATHER WINDOW
# ============================================================

def weather_window(row):

    wind_margin = max(
        0,
        row["MaxWind"] - wind
    )

    wave_margin = max(
        0,
        row["MaxWaves"] - waves
    )

    wind_score = min(
        100,
        wind_margin / 20 * 100
    )

    wave_score = min(
        100,
        wave_margin / 4 * 100
    )

    urgency = max(
        0,
        100 - deterioration / 1.8
    )

    return round(
        0.35 * wind_score +
        0.35 * wave_score +
        0.30 * urgency,
        2
    )


vessels["WeatherWindow"] = vessels.apply(
    weather_window,
    axis=1
)


# ============================================================
# PRIORITY
# ============================================================

def calculate_priority(row):

    safety = 100 if row["SafeNow"] else 0

    score = (
        safety * safety_weight +
        row["PassengerScore"] * passenger_weight +
        row["Cargo"] * cargo_weight +
        row["EconomicScore"] * economic_weight +
        row["WaitingScore"] * waiting_weight +
        row["WeatherWindow"] * weather_weight
    )

    if weight_sum:
        score /= weight_sum

    if row["Medical"]:
        score += 5

    if row["Perishable"]:
        score += 3

    return round(
        min(100, score),
        2
    )


vessels["Priority"] = vessels.apply(
    calculate_priority,
    axis=1
)


# ============================================================
# COST MODEL
# ============================================================

def delay_cost(row, delay):

    hours = delay / 60

    economic = (
        row["Economic"] *
        hours
    )

    passengers = (
        row["Passengers"] *
        0.00008 *
        hours
    )

    cargo = (
        row["Cargo"] /
        100 *
        0.25 *
        hours
    )

    medical = (
        2.5 * hours
        if row["Medical"]
        else 0
    )

    perish = (
        1.2 * hours
        if row["Perishable"]
        else 0
    )

    waiting = (
        row["Waiting"] *
        0.04 *
        hours
    )

    return (
        economic +
        passengers +
        cargo +
        medical +
        perish +
        waiting
    )


def sequence_cost(sequence, data):

    current_time = 0
    total = 0
    details = []

    for name in sequence:

        row = data[
            data["Vessel"] == name
        ].iloc[0]

        start = current_time

        finish = (
            current_time +
            row["Service"]
        )

        cost = delay_cost(
            row,
            start
        )

        if not row["SafeNow"]:
            cost += 100

        if start > deterioration:
            cost += 20

        total += cost

        details.append({
            "Vessel": name,
            "Start": start,
            "Finish": finish,
            "Delay": start,
            "Cost": cost
        })

        current_time = finish

    return total, details


# ============================================================
# OPTIMIZER
# ============================================================

def optimize(data):

    eligible = data[
        data["Eligible"]
    ].copy()

    if eligible.empty:
        return None

    names = eligible["Vessel"].tolist()

    best_sequence = None
    best_cost = float("inf")
    best_details = None

    for sequence in itertools.permutations(names):

        cost, details = sequence_cost(
            sequence,
            eligible
        )

        if cost < best_cost:

            best_cost = cost
            best_sequence = sequence
            best_details = details

    return {
        "sequence": list(best_sequence),
        "cost": best_cost,
        "details": best_details
    }


optimization = optimize(
    vessels
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="marine-header">

        <div class="header-grid">

            <div>
                <div class="tech-label">
                    MARITIME OPERATIONS / DECISION SUPPORT
                </div>

                <div class="main-title">
                    PORT PRIORITY
                </div>

                <div class="main-subtitle">
                    Vessel sequencing under weather uncertainty
                    and limited port resources
                </div>
            </div>

            <div class="system-status">
                <div class="status-live">
                    <span class="status-dot"></span>
                    SYSTEM ONLINE
                </div>

                <div class="tech-label" style="margin-top:8px;">
                    LIVE SIMULATION
                </div>
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="rule"></div>',
    unsafe_allow_html=True
)


# ============================================================
# STATUS METRICS
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">
                Weather risk
            </div>

            <div class="metric-value">
                {current_risk:.0f}
            </div>

            <div class="metric-note">
                {risk_label}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    safe_count = int(
        vessels["Eligible"].sum()
    )

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">
                Safe vessels
            </div>

            <div class="metric-value">
                {safe_count}/{len(vessels)}
            </div>

            <div class="metric-note">
                currently eligible
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">
                Berths
            </div>

            <div class="metric-value">
                {berths}
            </div>

            <div class="metric-note">
                available
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">
                Tugboats
            </div>

            <div class="metric-value">
                {tugs}
            </div>

            <div class="metric-note">
                available
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">
                Weather window
            </div>

            <div class="metric-value">
                {deterioration}
            </div>

            <div class="metric-note">
                minutes
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# WEATHER STATUS
# ============================================================

if current_risk >= 80:

    st.markdown(
        f"""
        <div class="alert-danger">
            <strong>CRITICAL WEATHER CONDITION</strong><br>
            Environmental risk index: {current_risk}/100.
            The safety filter is restricting eligible vessels.
        </div>
        """,
        unsafe_allow_html=True
    )

elif current_risk >= 60:

    st.markdown(
        f"""
        <div class="alert-warning">
            <strong>HIGH WEATHER RISK</strong><br>
            Environmental risk index: {current_risk}/100.
            The available operating window is narrowing.
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="alert-good">
            <strong>OPERATING CONDITIONS MANAGEABLE</strong><br>
            Environmental risk index: {current_risk}/100.
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# PORT MAP
# ============================================================

def build_port_map(data):

    fig = go.Figure()

    # water
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=100,
        y1=67,
        fillcolor="#0b2635",
        line=dict(
            color="#174052",
            width=1
        )
    )

    # harbour basin
    fig.add_shape(
        type="rect",
        x0=27,
        y0=15,
        x1=78,
        y1=62,
        fillcolor="#0d2d3d",
        line=dict(
            color="#1d5268",
            width=1
        )
    )

    # land
    fig.add_shape(
        type="rect",
        x0=0,
        y0=67,
        x1=100,
        y1=100,
        fillcolor="#10191f",
        line=dict(
            color="#20323c",
            width=1
        )
    )

    # navigation channel
    fig.add_shape(
        type="path",
        path="M 48 0 L 43 15 L 45 62 L 39 67 L 61 67 L 55 62 L 57 15 L 52 0 Z",
        fillcolor="#10374a",
        line=dict(
            color="#1c566c",
            width=1
        )
    )

    # berth positions
    berth_positions = [
        (10, 70),
        (37, 70),
        (64, 70),
        (10, 84),
        (37, 84),
        (64, 84)
    ]

    for i in range(
        min(int(berths), 6)
    ):

        x, y = berth_positions[i]

        fig.add_shape(
            type="rect",
            x0=x,
            y0=y,
            x1=x + 20,
            y1=y + 7,
            fillcolor="#16252e",
            line=dict(
                color="#45606c",
                width=1
            )
        )

        fig.add_annotation(
            x=x + 10,
            y=y + 3.5,
            text=f"BERTH {i+1}",
            showarrow=False,
            font=dict(
                color="#8096a2",
                size=9
            )
        )

    # vessels
    eligible = data[
        data["Eligible"]
    ].sort_values(
        "Priority",
        ascending=False
    )

    coordinates = [
        (20, 20),
        (73, 27),
        (28, 40),
        (76, 48),
        (52, 18),
        (15, 51),
        (86, 42),
        (45, 34)
    ]

    for idx, (_, row) in enumerate(
        eligible.iterrows()
    ):

        x, y = coordinates[
            idx % len(coordinates)
        ]

        priority = row["Priority"]

        if priority >= 70:
            marker_color = "#62d8c4"

        elif priority >= 45:
            marker_color = "#d6b66c"

        else:
            marker_color = "#738692"

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(
                    size=13,
                    color=marker_color,
                    line=dict(
                        color="#dce9ed",
                        width=1
                    )
                ),
                text=[row["Vessel"]],
                textposition="top center",
                textfont=dict(
                    color="#cddbe0",
                    size=9
                ),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    f"Type: {row['Type']}<br>"
                    f"Priority: {priority:.1f}<br>"
                    "<extra></extra>"
                ),
                showlegend=False
            )
        )

    fig.add_annotation(
        x=94,
        y=92,
        text="N",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=20,
        font=dict(
            color="#8da2ad",
            size=10
        )
    )

    fig.update_xaxes(
        range=[0, 100],
        visible=False
    )

    fig.update_yaxes(
        range=[0, 100],
        visible=False,
        scaleanchor="x"
    )

    fig.update_layout(
        height=540,
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),
        paper_bgcolor="#0d1d26",
        plot_bgcolor="#0d1d26",
        hoverlabel=dict(
            bgcolor="#10232d",
            bordercolor="#34515f",
            font_color="#e7f0f3"
        )
    )

    return fig


left, right = st.columns(
    [1.65, 1],
    gap="large"
)


# ============================================================
# MAP
# ============================================================

with left:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-header">

                <div class="panel-title">
                    PORT OPERATIONS MAP
                </div>

                <div class="panel-code">
                    LIVE / SCHEMATIC
                </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    st.plotly_chart(
        build_port_map(vessels),
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    st.markdown(
        """
        <div style="
            display:flex;
            gap:1.4rem;
            color:#637b87;
            font-family:'DM Mono',monospace;
            font-size:0.61rem;
            padding-top:0.2rem;
        ">
            <span>
                <span style="color:#62d8c4;">●</span>
                HIGH PRIORITY
            </span>

            <span>
                <span style="color:#d6b66c;">●</span>
                MEDIUM
            </span>

            <span>
                <span style="color:#738692;">●</span>
                LOW
            </span>
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SYSTEM RECOMMENDATION
# ============================================================

with right:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-header">

                <div class="panel-title">
                    SYSTEM RECOMMENDATION
                </div>

                <div class="panel-code">
                    OPT-01
                </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    if optimization:

        first = optimization["sequence"][0]

        first_row = vessels[
            vessels["Vessel"] == first
        ].iloc[0]

        reasons = []

        if first_row["Medical"]:
            reasons.append(
                "medical priority"
            )

        if first_row["Passengers"] > 0:
            reasons.append(
                f"{int(first_row['Passengers']):,} passengers"
            )

        if first_row["WeatherWindow"] >= 60:
            reasons.append(
                "limited weather window"
            )

        if first_row["Waiting"] >= 4:
            reasons.append(
                "extended waiting time"
            )

        reason = ", ".join(
            reasons
        )

        st.markdown(
            f"""
            <div class="recommendation">

                <div class="recommendation-title">
                    Recommended first movement
                </div>

                <div class="recommendation-main">
                    {first}
                </div>

                <div class="recommendation-text">
                    {first_row["Type"]}.
                    {reason.capitalize()
                    if reason
                    else
                    "Highest current position in the optimized sequence."}.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="tech-label">OPTIMIZED SEQUENCE</div>',
            unsafe_allow_html=True
        )

        for i, name in enumerate(
            optimization["sequence"],
            1
        ):

            row = vessels[
                vessels["Vessel"] == name
            ].iloc[0]

            priority = row["Priority"]

            if priority >= 70:
                cls = "priority-high"

            elif priority >= 45:
                cls = "priority-medium"

            else:
                cls = "priority-low"

            st.markdown(
                f"""
                <div class="vessel-row">

                    <div class="vessel-rank">
                        0{i}
                    </div>

                    <div>

                        <div class="vessel-name">
                            {name}
                        </div>

                        <div class="vessel-type">
                            {row["Type"]}
                        </div>

                    </div>

                    <div class="vessel-number">
                        +{row["Service"]} min
                    </div>

                    <div class="vessel-number {cls}">
                        {priority:.0f}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            """
            <div class="alert-danger">

                <strong>
                    NO ELIGIBLE VESSEL
                </strong>

                <br>

                Current conditions exceed
                the simulated safety envelope.

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# TABS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "VESSEL QUEUE",
    "DECISION RATIONALE",
    "SCENARIO LAB",
    "HUMAN OVERRIDE"
])


# ============================================================
# TAB 1
# ============================================================

with tab1:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-header">

                <div class="panel-title">
                    CURRENT VESSEL QUEUE
                </div>

                <div class="panel-code">
                    8 OBJECTS
                </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    display = vessels[
        [
            "Vessel",
            "Type",
            "Passengers",
            "Cargo",
            "Economic",
            "Waiting",
            "Priority",
            "SafeNow"
        ]
    ].copy()

    display.columns = [
        "Vessel",
        "Type",
        "Passengers",
        "Criticality",
        "Economic exposure",
        "Waiting / h",
        "Priority",
        "Safe now"
    ]

    st.dataframe(
        display.sort_values(
            "Priority",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Priority":
                st.column_config.ProgressColumn(
                    "Priority",
                    min_value=0,
                    max_value=100,
                    format="%.0f"
                ),

            "Economic exposure":
                st.column_config.NumberColumn(
                    "Economic exposure",
                    format="%.2f"
                )
        }
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# TAB 2
# ============================================================

with tab2:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-header">

                <div class="panel-title">
                    DECISION RATIONALE
                </div>

                <div class="panel-code">
                    MODEL EXPLANATION
                </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    if optimization:

        selected = st.selectbox(
            "Inspect vessel",
            optimization["sequence"],
            key="rationale_vessel"
        )

        row = vessels[
            vessels["Vessel"] == selected
        ].iloc[0]

        col1, col2 = st.columns(2)

        with col1:

            factors = pd.DataFrame({
                "Factor": [
                    "Safety",
                    "Passengers",
                    "Cargo",
                    "Economic",
                    "Waiting",
                    "Weather window"
                ],

                "Value": [
                    100
                    if row["SafeNow"]
                    else 0,

                    row["PassengerScore"],
                    row["Cargo"],
                    row["EconomicScore"],
                    row["WaitingScore"],
                    row["WeatherWindow"]
                ]
            })

            chart = go.Figure(
                go.Bar(
                    x=factors["Value"],
                    y=factors["Factor"],
                    orientation="h",
                    marker_color="#62d8c4"
                )
            )

            chart.update_layout(
                height=320,
                margin=dict(
                    l=0,
                    r=0,
                    t=10,
                    b=10
                ),
                paper_bgcolor="#0d1d26",
                plot_bgcolor="#0d1d26",
                font=dict(
                    color="#9aaeb7"
                ),
                xaxis=dict(
                    range=[0, 100],
                    gridcolor="#1d3440"
                ),
                yaxis=dict(
                    gridcolor="rgba(0,0,0,0)"
                )
            )

            st.plotly_chart(
                chart,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        with col2:

            st.markdown(
                '<div class="tech-label">'
                'MODEL INTERPRETATION'
                '</div>',
                unsafe_allow_html=True
            )

            reasons = []

            if row["Medical"]:
                reasons.append(
                    "medical urgency increases the estimated cost of delay"
                )

            if row["Passengers"] > 0:
                reasons.append(
                    f"passenger exposure: {int(row['Passengers']):,}"
                )

            if row["Cargo"] >= 80:
                reasons.append(
                    "high criticality cargo"
                )

            if row["Economic"] >= 1:
                reasons.append(
                    "high economic exposure"
                )

            if row["WeatherWindow"] >= 60:
                reasons.append(
                    "favourable but potentially narrowing weather window"
                )

            if row["Waiting"] >= 4:
                reasons.append(
                    "long waiting time"
                )

            if not row["SafeNow"]:
                reasons.append(
                    "currently outside simulated safety envelope"
                )

            for reason in reasons:

                st.markdown(
                    f"""
                    <div style="
                        padding:0.7rem 0;
                        border-bottom:1px solid #19303c;
                        color:#aab9c1;
                        font-size:0.76rem;
                    ">
                        {reason}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# TAB 3 — SCENARIO LAB
# ============================================================

with tab3:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-header">

                <div class="panel-title">
                    SCENARIO LABORATORY
                </div>

                <div class="panel-code">
                    WHAT-IF ANALYSIS
                </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    s1, s2, s3 = st.columns(3)

    with s1:

        scenario_wind = st.slider(
            "Scenario wind",
            5,
            55,
            wind,
            key="scenario_wind"
        )

    with s2:

        scenario_waves = st.slider(
            "Scenario wave height",
            0.5,
            8.0,
            waves,
            0.1,
            key="scenario_waves"
        )

    with s3:

        scenario_time = st.slider(
            "Deterioration in",
            10,
            180,
            deterioration,
            key="scenario_time"
        )

    scenario_risk = weather_risk(
        scenario_wind,
        scenario_waves,
        visibility
    )

    st.markdown(
        f"""
        <div class="metric-box">

            <div class="metric-label">
                Scenario risk
            </div>

            <div class="metric-value">
                {scenario_risk:.0f}
            </div>

            <div class="metric-note">
                {weather_label(scenario_risk)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    scenario = vessels.copy()

    scenario["Eligible"] = scenario.apply(
        lambda row:
            scenario_wind <= row["MaxWind"]
            and scenario_waves <= row["MaxWaves"]
            and row["Tugs"] <= tugs
            and row["Pilots"] <= pilots,
        axis=1
    )

    scenario["ScenarioPriority"] = scenario.apply(
        lambda row: (
            (
                (100 if row["Eligible"] else 0)
                * safety_weight

                +

                row["PassengerScore"]
                * passenger_weight

                +

                row["Cargo"]
                * cargo_weight

                +

                row["EconomicScore"]
                * economic_weight

                +

                row["WaitingScore"]
                * waiting_weight
            )
            /
            weight_sum
            if weight_sum
            else 0
        ),
        axis=1
    )

    scenario_queue = scenario[
        scenario["Eligible"]
    ].sort_values(
        "ScenarioPriority",
        ascending=False
    )

    if scenario_queue.empty:

        st.markdown(
            """
            <div class="alert-danger">

                <strong>
                    NO ELIGIBLE VESSEL
                </strong>

                <br>

                No vessel satisfies
                the scenario constraints.

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="tech-label">'
            'SCENARIO SEQUENCE'
            '</div>',
            unsafe_allow_html=True
        )

        for i, (_, row) in enumerate(
            scenario_queue.iterrows(),
            1
        ):

            st.markdown(
                f"""
                <div class="vessel-row">

                    <div class="vessel-rank">
                        0{i}
                    </div>

                    <div>

                        <div class="vessel-name">
                            {row["Vessel"]}
                        </div>

                        <div class="vessel-type">
                            {row["Type"]}
                        </div>

                    </div>

                    <div class="vessel-number">
                        {row["Service"]} min
                    </div>

                    <div class="vessel-number">
                        {row["ScenarioPriority"]:.0f}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# TAB 4 — HUMAN OVERRIDE
# ============================================================

with tab4:

    st.markdown(
        """
        <div class="panel">

            <div class="panel-header">

                <div class="panel-title">
                    HUMAN OVERRIDE
                </div>

                <div class="panel-code">
                    OPERATOR DECISION
                </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "The model provides a recommendation. "
        "The operator retains authority to override it "
        "when new information is available."
    )

    if optimization:

        override_vessel = st.selectbox(
            "Move vessel to priority position",
            optimization["sequence"],
            key="override_vessel"
        )

        override_reason = st.text_area(
            "Decision rationale",
            placeholder=(
                "Record information unavailable to the model."
            ),
            key="override_reason"
        )

        if st.button(
            "APPLY OPERATOR DECISION",
            type="primary"
        ):

            if not override_reason.strip():

                st.error(
                    "A rationale is required."
                )

            else:

                sequence = list(
                    optimization["sequence"]
                )

                sequence.remove(
                    override_vessel
                )

                sequence.insert(
                    0,
                    override_vessel
                )

                st.session_state.override_sequence = sequence

                st.session_state.decision_log.append({
                    "Timestamp":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        ),

                    "Vessel":
                        override_vessel,

                    "Decision":
                        "Moved to priority #1",

                    "Rationale":
                        override_reason
                })

                st.success(
                    "Operator decision recorded."
                )

        if st.session_state.override_sequence:

            st.markdown(
                '<div class="tech-label">'
                'REVISED SEQUENCE'
                '</div>',
                unsafe_allow_html=True
            )

            for i, name in enumerate(
                st.session_state.override_sequence,
                1
            ):

                st.markdown(
                    f"""
                    <div class="vessel-row">

                        <div class="vessel-rank">
                            0{i}
                        </div>

                        <div>
                            <div class="vessel-name">
                                {name}
                            </div>
                        </div>

                        <div></div>

                        <div class="vessel-number">
                            POSITION {i}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# DECISION AUDIT TRAIL
# ============================================================

if st.session_state.decision_log:

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="panel">

            <div class="panel-header">

                <div class="panel-title">
                    DECISION AUDIT TRAIL
                </div>

                <div class="panel-code">
                    SESSION HISTORY
                </div>

            </div>
        """,
        unsafe_allow_html=True
    )

    log_df = pd.DataFrame(
        st.session_state.decision_log
    )

    st.dataframe(
        log_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        PORT PRIORITY / MARITIME OPERATIONS DECISION SUPPORT SYSTEM
        / ACADEMIC PROTOTYPE
        <br>
        NOT FOR REAL-WORLD NAVIGATION OR PORT SAFETY OPERATIONS
    </div>
    """,
    unsafe_allow_html=True
)
