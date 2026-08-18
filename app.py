import streamlit as st
import pandas as pd
import numpy as np
import itertools
import plotly.graph_objects as go
from datetime import datetime


# ============================================================
# PORT PRIORITY
# Operational Decision Support System
# Version 3.0
# ============================================================

st.set_page_config(
    page_title="PORT PRIORITY",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GLOBAL STYLE
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1118;
    color: #e8edf2;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

/* remove default top decoration */

header[data-testid="stHeader"] {
    background: transparent;
}

/* sidebar */

section[data-testid="stSidebar"] {
    background: #0d151e;
    border-right: 1px solid #202d39;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* typography */

h1, h2, h3 {
    letter-spacing: -0.03em;
}

h1 {
    font-weight: 700;
}

h2 {
    font-size: 1.35rem;
}

h3 {
    font-size: 1rem;
}

/* technical labels */

.tech-label {
    font-family: 'DM Mono', monospace;
    color: #718191;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.status-live {
    color: #55d6be;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
}

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #55d6be;
    margin-right: 7px;
}

/* main title */

.main-title {
    font-size: 2.45rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    margin-bottom: 0.15rem;
}

.main-subtitle {
    color: #82909e;
    font-size: 0.9rem;
}

/* horizontal line */

.rule {
    height: 1px;
    background: #202d39;
    margin: 1.4rem 0;
}

/* metric blocks */

.metric-box {
    background: #101922;
    border: 1px solid #202d39;
    padding: 1.05rem 1.15rem;
    min-height: 105px;
}

.metric-label {
    color: #718191;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.metric-value {
    font-size: 1.65rem;
    font-weight: 600;
    margin-top: 0.35rem;
}

.metric-note {
    color: #718191;
    font-size: 0.72rem;
    margin-top: 0.2rem;
}

/* panels */

.panel {
    background: #0f1821;
    border: 1px solid #202d39;
    padding: 1.15rem;
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.9rem;
}

.panel-title {
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}

.panel-code {
    color: #667685;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
}

/* vessel rows */

.vessel-row {
    display: grid;
    grid-template-columns: 42px 1fr 100px 90px;
    align-items: center;
    border-top: 1px solid #1d2934;
    padding: 0.75rem 0;
}

.vessel-rank {
    font-family: 'DM Mono', monospace;
    color: #5e7180;
    font-size: 0.72rem;
}

.vessel-name {
    font-weight: 600;
    font-size: 0.82rem;
}

.vessel-type {
    color: #718191;
    font-size: 0.68rem;
    margin-top: 0.12rem;
}

.vessel-number {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #b5c0ca;
    text-align: right;
}

.priority-high {
    color: #55d6be;
}

.priority-medium {
    color: #d8b76a;
}

.priority-low {
    color: #718191;
}

/* recommendation */

.recommendation {
    border-left: 3px solid #55d6be;
    background: #101d22;
    padding: 1rem 1.1rem;
}

.recommendation-title {
    color: #55d6be;
    font-family: 'DM Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.recommendation-main {
    font-size: 1.15rem;
    font-weight: 600;
    margin-top: 0.3rem;
}

.recommendation-text {
    color: #8795a3;
    font-size: 0.78rem;
    line-height: 1.55;
    margin-top: 0.35rem;
}

/* alerts */

.alert-danger {
    border-left: 3px solid #e06c75;
    background: #1b1518;
    padding: 0.9rem 1rem;
}

.alert-warning {
    border-left: 3px solid #d8b76a;
    background: #1b1913;
    padding: 0.9rem 1rem;
}

.alert-good {
    border-left: 3px solid #55d6be;
    background: #101d1d;
    padding: 0.9rem 1rem;
}

/* buttons */

.stButton > button {
    border-radius: 2px;
    border: 1px solid #314150;
    background: #111c25;
    color: #dce4ea;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
}

.stButton > button:hover {
    border-color: #55d6be;
    color: #55d6be;
}

/* tabs */

button[data-baseweb="tab"] {
    font-size: 0.75rem;
    font-weight: 500;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #55d6be;
}

/* dataframe */

[data-testid="stDataFrame"] {
    border: 1px solid #202d39;
}

/* footer */

.footer {
    color: #53616e;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.05em;
    margin-top: 2rem;
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
# SIDEBAR — CONTROL PARAMETERS
# ============================================================

st.sidebar.markdown(
    '<div class="tech-label">CONTROL PARAMETERS</div>',
    unsafe_allow_html=True
)

wind = st.sidebar.slider(
    "Wind speed",
    5, 55, 28,
    help="Current wind speed in knots."
)

waves = st.sidebar.slider(
    "Wave height",
    0.5, 8.0, 4.2, 0.1,
    help="Significant wave height in metres."
)

visibility = st.sidebar.slider(
    "Visibility",
    0.2, 15.0, 1.8, 0.1,
    help="Horizontal visibility in kilometres."
)

deterioration = st.sidebar.slider(
    "Weather deterioration",
    10, 180, 35,
    help="Estimated minutes until severe deterioration."
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
# MODELS
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
# SAFETY
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
    <div style="display:flex; justify-content:space-between;
                align-items:flex-end;">
        <div>
            <div class="tech-label">PORT OPERATIONS / DECISION SUPPORT</div>
            <div class="main-title">PORT PRIORITY</div>
            <div class="main-subtitle">
                Vessel sequencing under weather uncertainty and limited resources
            </div>
        </div>
        <div class="status-live">
            <span class="status-dot"></span>SYSTEM ONLINE
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="rule"></div>', unsafe_allow_html=True)


# ============================================================
# TOP STATUS BAR
# ============================================================

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Weather risk</div>
            <div class="metric-value">{current_risk:.0f}</div>
            <div class="metric-note">{risk_label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    safe_count = int(vessels["Eligible"].sum())

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Safe vessels</div>
            <div class="metric-value">{safe_count}/{len(vessels)}</div>
            <div class="metric-note">currently eligible</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Berths</div>
            <div class="metric-value">{berths}</div>
            <div class="metric-note">available</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Tugboats</div>
            <div class="metric-value">{tugs}</div>
            <div class="metric-note">available</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:
    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-label">Weather window</div>
            <div class="metric-value">{deterioration}</div>
            <div class="metric-note">minutes</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# WEATHER ALERT
# ============================================================

if current_risk >= 80:

    st.markdown(
        f"""
        <div class="alert-danger">
            <strong>CRITICAL WEATHER CONDITION</strong><br>
            Current environmental risk is {current_risk}/100.
            The system is applying the strict safety filter.
        </div>
        """,
        unsafe_allow_html=True
    )

elif current_risk >= 60:

    st.markdown(
        f"""
        <div class="alert-warning">
            <strong>HIGH WEATHER RISK</strong><br>
            Risk index {current_risk}/100.
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
            Environmental risk is {current_risk}/100.
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# PORT MAP
# ============================================================

def build_port_map(data, result):

    fig = go.Figure()

    # water area
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=100,
        y1=65,
        fillcolor="#0c2534",
        line=dict(
            color="#18394d",
            width=1
        )
    )

    # land
    fig.add_shape(
        type="rect",
        x0=0,
        y0=65,
        x1=100,
        y1=100,
        fillcolor="#111920",
        line=dict(
            color="#202d39",
            width=1
        )
    )

    # entrance channel
    fig.add_shape(
        type="rect",
        x0=42,
        y0=0,
        x1=58,
        y1=65,
        fillcolor="#103044",
        line=dict(
            color="#1d4c64",
            width=1
        )
    )

    # berths
    berth_positions = [
        (15, 66),
        (42, 66),
        (69, 66),
        (15, 82),
        (42, 82),
        (69, 82)
    ]

    for i in range(min(int(berths), 6)):

        x, y = berth_positions[i]

        fig.add_shape(
            type="rect",
            x0=x,
            y0=y,
            x1=x + 18,
            y1=y + 8,
            fillcolor="#17232c",
            line=dict(
                color="#426070",
                width=1
            )
        )

        fig.add_annotation(
            x=x + 9,
            y=y + 4,
            text=f"BERTH {i+1}",
            showarrow=False,
            font=dict(
                color="#8395a3",
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

    coords = [
        (25, 18),
        (70, 28),
        (30, 40),
        (73, 50),
        (55, 14),
        (18, 52),
        (83, 43),
        (45, 30)
    ]

    for idx, (_, row) in enumerate(
        eligible.iterrows()
    ):

        x, y = coords[
            idx % len(coords)
        ]

        priority = row["Priority"]

        if priority >= 70:
            marker_color = "#55d6be"
        elif priority >= 45:
            marker_color = "#d8b76a"
        else:
            marker_color = "#6d7e8c"

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                marker=dict(
                    size=14,
                    color=marker_color,
                    line=dict(
                        color="#dce5ea",
                        width=1
                    )
                ),
                text=[row["Vessel"]],
                textposition="top center",
                textfont=dict(
                    color="#dbe4e9",
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

    # north arrow
    fig.add_annotation(
        x=94,
        y=92,
        text="N",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=20,
        font=dict(
            color="#8ea0ae",
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
        paper_bgcolor="#0f1821",
        plot_bgcolor="#0f1821",
        hoverlabel=dict(
            bgcolor="#101922",
            bordercolor="#314150",
            font_color="#e8edf2"
        )
    )

    return fig


left, right = st.columns(
    [1.65, 1],
    gap="large"
)


# ============================================================
# LEFT — MAP
# ============================================================

with left:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">PORT OPERATIONS MAP</div>
                <div class="panel-code">LIVE / SCHEMATIC</div>
            </div>
        """,
        unsafe_allow_html=True
    )

    fig = build_port_map(
        vessels,
        optimization
    )

    st.plotly_chart(
        fig,
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
            color:#667685;
            font-family:'DM Mono',monospace;
            font-size:0.62rem;
            padding-top:0.2rem;
        ">
            <span><span style="color:#55d6be;">●</span> HIGH PRIORITY</span>
            <span><span style="color:#d8b76a;">●</span> MEDIUM</span>
            <span><span style="color:#6d7e8c;">●</span> LOW</span>
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# RIGHT — SYSTEM RECOMMENDATION
# ============================================================

with right:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">SYSTEM RECOMMENDATION</div>
                <div class="panel-code">OPT-01</div>
            </div>
        """,
        unsafe_allow_html=True
    )

    if optimization:

        first = optimization["sequence"][0]

        first_row = vessels[
            vessels["Vessel"] == first
        ].iloc[0]

        reason_parts = []

        if first_row["Medical"]:
            reason_parts.append(
                "medical priority"
            )

        if first_row["Passengers"] > 0:
            reason_parts.append(
                f"{int(first_row['Passengers']):,} passengers"
            )

        if first_row["WeatherWindow"] >= 60:
            reason_parts.append(
                "limited weather window"
            )

        if first_row["Waiting"] >= 4:
            reason_parts.append(
                "extended waiting time"
            )

        reason = ", ".join(
            reason_parts
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
                    {reason.capitalize() if reason else "Best current position in the optimized sequence."}.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="tech-label">SEQUENCE</div>',
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
                    <div class="vessel-rank">0{i}</div>
                    <div>
                        <div class="vessel-name">{name}</div>
                        <div class="vessel-type">{row["Type"]}</div>
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
                No eligible vessel.
                Current conditions exceed the available operating envelope.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# MAIN TABS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "VESSEL QUEUE",
    "DECISION RATIONALE",
    "SCENARIO LAB",
    "HUMAN OVERRIDE"
])


# ============================================================
# TAB 1 — QUEUE
# ============================================================

with tab1:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">CURRENT VESSEL QUEUE</div>
                <div class="panel-code">8 OBJECTS</div>
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
            "Priority": st.column_config.ProgressColumn(
                "Priority",
                min_value=0,
                max_value=100,
                format="%.0f"
            ),
            "Economic exposure": st.column_config.NumberColumn(
                "Economic exposure",
                format="%.2f"
            )
        }
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# TAB 2 — RATIONALE
# ============================================================

with tab2:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">DECISION RATIONALE</div>
                <div class="panel-code">MODEL EXPLANATION</div>
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
                    100 if row["SafeNow"] else 0,
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
                    marker_color="#55d6be"
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
                paper_bgcolor="#0f1821",
                plot_bgcolor="#0f1821",
                font=dict(
                    color="#9aa8b4"
                ),
                xaxis=dict(
                    range=[0, 100],
                    gridcolor="#1e2b35"
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
                '<div class="tech-label">MODEL INTERPRETATION</div>',
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
                        border-bottom:1px solid #1d2934;
                        color:#aab6c0;
                        font-size:0.78rem;
                    ">
                        {reason}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# TAB 3 — SCENARIO LAB
# ============================================================

with tab3:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">SCENARIO LABORATORY</div>
                <div class="panel-code">WHAT-IF ANALYSIS</div>
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
            <div class="metric-label">Scenario risk</div>
            <div class="metric-value">{scenario_risk:.0f}</div>
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
                (100 if row["Eligible"] else 0) *
                safety_weight
                +
                row["PassengerScore"] *
                passenger_weight
                +
                row["Cargo"] *
                cargo_weight
                +
                row["EconomicScore"] *
                economic_weight
                +
                row["WaitingScore"] *
                waiting_weight
            )
            /
            weight_sum
            if weight_sum else 0
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
                No vessel satisfies the scenario constraints.
                Port access should remain restricted.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="tech-label">SCENARIO SEQUENCE</div>',
            unsafe_allow_html=True
        )

        for i, (_, row) in enumerate(
            scenario_queue.iterrows(),
            1
        ):

            st.markdown(
                f"""
                <div class="vessel-row">
                    <div class="vessel-rank">0{i}</div>
                    <div>
                        <div class="vessel-name">{row["Vessel"]}</div>
                        <div class="vessel-type">{row["Type"]}</div>
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

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# TAB 4 — HUMAN OVERRIDE
# ============================================================

with tab4:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">HUMAN OVERRIDE</div>
                <div class="panel-code">OPERATOR DECISION</div>
            </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        "The model provides a recommendation. The operator retains "
        "authority to override it when new information is available."
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
                '<div class="tech-label">REVISED SEQUENCE</div>',
                unsafe_allow_html=True
            )

            for i, name in enumerate(
                st.session_state.override_sequence,
                1
            ):

                st.markdown(
                    f"""
                    <div class="vessel-row">
                        <div class="vessel-rank">0{i}</div>
                        <div>
                            <div class="vessel-name">{name}</div>
                        </div>
                        <div></div>
                        <div class="vessel-number">
                            POSITION {i}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# DECISION LOG
# ============================================================

if st.session_state.decision_log:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">DECISION AUDIT TRAIL</div>
                <div class="panel-code">SESSION HISTORY</div>
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

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# METHODOLOGY
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="panel">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="panel-header">'
    '<div class="panel-title">SYSTEM METHODOLOGY</div>'
    '<div class="panel-code">MODEL 3.0</div>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        color:#8795a3;
        font-size:0.78rem;
        line-height:1.7;
    ">
        The system evaluates vessel sequences rather than isolated
        priority scores. Each candidate sequence is assessed against
        weather constraints, resource availability, waiting time,
        passenger exposure, cargo criticality and estimated economic
        consequences.

        <br><br>

        The optimization layer identifies the sequence with the lowest
        estimated aggregate operational cost. The human override layer
        intentionally preserves operator authority when information
        exists outside the model.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        PORT PRIORITY / OPERATIONAL DECISION SUPPORT SYSTEM / ACADEMIC PROTOTYPE
        <br>
        NOT FOR REAL-WORLD NAVIGATION OR PORT SAFETY OPERATIONS
    </div>
    """,
    unsafe_allow_html=True
)
