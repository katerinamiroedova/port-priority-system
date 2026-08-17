import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================
# PORT PRIORITY SYSTEM
# Decision-support system for vessel prioritization
# during severe weather and limited port capacity.
# ============================================================

st.set_page_config(
    page_title="Port Priority System",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    .main {
        background-color: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.8rem 2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #0b1f33 0%, #173b5f 100%);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        font-size: 2.4rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        font-size: 1.05rem;
        opacity: 0.85;
    }

    .metric-card {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 14px;
        border: 1px solid #e3e8ef;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .risk-high {
        background: #fff0f0;
        border-left: 5px solid #d64545;
        padding: 1rem;
        border-radius: 10px;
    }

    .risk-medium {
        background: #fff8e6;
        border-left: 5px solid #e6a700;
        padding: 1rem;
        border-radius: 10px;
    }

    .risk-low {
        background: #eef9f2;
        border-left: 5px solid #35a66f;
        padding: 1rem;
        border-radius: 10px;
    }

    .decision-box {
        background: #ffffff;
        border: 1px solid #dce3ec;
        border-radius: 14px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    .small-muted {
        color: #667085;
        font-size: 0.9rem;
    }

    .priority-number {
        font-size: 2rem;
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #e3e8ef;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "decision_log" not in st.session_state:
    st.session_state.decision_log = []

if "simulation_ran" not in st.session_state:
    st.session_state.simulation_ran = False

if "results" not in st.session_state:
    st.session_state.results = None


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <h1>⚓ PORT PRIORITY SYSTEM</h1>
    <p>
        Decision-support system for vessel prioritization
        during severe weather and limited port capacity.
    </p>
</div>
""", unsafe_allow_html=True)

st.caption(
    "A simulation-based model exploring how ports can allocate scarce resources "
    "when safety, passengers, critical cargo, economic impact and weather conditions conflict."
)


# ============================================================
# SIDEBAR — WEATHER & PORT CONDITIONS
# ============================================================

st.sidebar.header("🌊 Port conditions")

wind_speed = st.sidebar.slider(
    "Wind speed (knots)",
    min_value=5,
    max_value=55,
    value=28
)

wave_height = st.sidebar.slider(
    "Wave height (m)",
    min_value=0.5,
    max_value=8.0,
    value=4.2,
    step=0.1
)

visibility = st.sidebar.slider(
    "Visibility (km)",
    min_value=0.2,
    max_value=15.0,
    value=1.8,
    step=0.1
)

weather_change_minutes = st.sidebar.slider(
    "Expected severe deterioration in (minutes)",
    min_value=10,
    max_value=180,
    value=35
)

st.sidebar.divider()

st.sidebar.header("🏗️ Available port resources")

available_berths = st.sidebar.number_input(
    "Available berths",
    min_value=1,
    max_value=10,
    value=3
)

available_tugs = st.sidebar.number_input(
    "Available tugboats",
    min_value=0,
    max_value=10,
    value=2
)

available_pilots = st.sidebar.number_input(
    "Available pilots",
    min_value=0,
    max_value=10,
    value=1
)

st.sidebar.divider()

st.sidebar.header("⚙️ Decision philosophy")

safety_weight = st.sidebar.slider(
    "Safety",
    0,
    100,
    30
)

urgency_weight = st.sidebar.slider(
    "Urgency",
    0,
    100,
    20
)

passenger_weight = st.sidebar.slider(
    "Passenger impact",
    0,
    100,
    15
)

cargo_weight = st.sidebar.slider(
    "Cargo criticality",
    0,
    100,
    15
)

waiting_weight = st.sidebar.slider(
    "Waiting time",
    0,
    100,
    10
)

economic_weight = st.sidebar.slider(
    "Economic impact",
    0,
    100,
    10
)

total_weight = (
    safety_weight +
    urgency_weight +
    passenger_weight +
    cargo_weight +
    waiting_weight +
    economic_weight
)

if total_weight == 0:
    st.sidebar.error("At least one decision weight must be greater than zero.")


# ============================================================
# WEATHER RISK MODEL
# ============================================================

def calculate_weather_risk(wind, waves, visibility):
    """
    Converts environmental conditions into a 0-100 risk score.
    This is a simulation model, not a real maritime safety standard.
    """

    wind_component = np.clip((wind - 10) / 40 * 100, 0, 100)
    wave_component = np.clip((waves - 0.5) / 7.5 * 100, 0, 100)
    visibility_component = np.clip((8 - visibility) / 8 * 100, 0, 100)

    risk = (
        0.40 * wind_component +
        0.40 * wave_component +
        0.20 * visibility_component
    )

    return round(float(np.clip(risk, 0, 100)), 1)


weather_risk = calculate_weather_risk(
    wind_speed,
    wave_height,
    visibility
)


def weather_status(risk):
    if risk >= 75:
        return "CRITICAL", "risk-high"
    elif risk >= 50:
        return "HIGH", "risk-medium"
    elif risk >= 30:
        return "MODERATE", "risk-medium"
    else:
        return "LOW", "risk-low"


risk_label, risk_class = weather_status(weather_risk)


# ============================================================
# DYNAMIC WEATHER PRESSURE
# ============================================================

def deterioration_pressure(minutes):
    """
    The closer severe deterioration is, the stronger
    the model prioritizes vessels that have a safe window now.
    """

    if minutes <= 20:
        return 100
    elif minutes <= 40:
        return 85
    elif minutes <= 60:
        return 70
    elif minutes <= 90:
        return 50
    elif minutes <= 120:
        return 30
    else:
        return 15


weather_pressure = deterioration_pressure(weather_change_minutes)


# ============================================================
# VESSEL DATABASE
# ============================================================

vessels = pd.DataFrame([
    {
        "Vessel": "Ocean Star",
        "Type": "Cruise Liner",
        "Passengers": 2840,
        "Cargo Value ($M)": 0,
        "Cargo Criticality": 10,
        "Waiting (h)": 3.3,
        "Economic Impact ($M/h)": 0.42,
        "Medical Emergency": True,
        "Perishable Cargo": False,
        "Fuel Urgency": 60,
        "Safe Entry": True,
        "Berth Time (min)": 35,
        "Tug Required": True,
        "Pilot Required": True
    },
    {
        "Vessel": "MedExpress",
        "Type": "Medical Cargo",
        "Passengers": 0,
        "Cargo Value ($M)": 38,
        "Cargo Criticality": 100,
        "Waiting (h)": 0.8,
        "Economic Impact ($M/h)": 0.75,
        "Medical Emergency": False,
        "Perishable Cargo": True,
        "Fuel Urgency": 40,
        "Safe Entry": True,
        "Berth Time (min)": 25,
        "Tug Required": True,
        "Pilot Required": True
    },
    {
        "Vessel": "Baltic Trader",
        "Type": "Container Ship",
        "Passengers": 0,
        "Cargo Value ($M)": 120,
        "Cargo Criticality": 55,
        "Waiting (h)": 2.2,
        "Economic Impact ($M/h)": 1.35,
        "Medical Emergency": False,
        "Perishable Cargo": False,
        "Fuel Urgency": 50,
        "Safe Entry": True,
        "Berth Time (min)": 50,
        "Tug Required": True,
        "Pilot Required": True
    },
    {
        "Vessel": "Aurora",
        "Type": "Tanker",
        "Passengers": 0,
        "Cargo Value ($M)": 95,
        "Cargo Criticality": 70,
        "Waiting (h)": 1.7,
        "Economic Impact ($M/h)": 1.10,
        "Medical Emergency": False,
        "Perishable Cargo": False,
        "Fuel Urgency": 95,
        "Safe Entry": True,
        "Berth Time (min)": 45,
        "Tug Required": True,
        "Pilot Required": True
    },
    {
        "Vessel": "Northern Wind",
        "Type": "Ferry",
        "Passengers": 720,
        "Cargo Value ($M)": 4,
        "Cargo Criticality": 35,
        "Waiting (h)": 4.1,
        "Economic Impact ($M/h)": 0.18,
        "Medical Emergency": False,
        "Perishable Cargo": False,
        "Fuel Urgency": 65,
        "Safe Entry": True,
        "Berth Time (min)": 20,
        "Tug Required": False,
        "Pilot Required": True
    },
    {
        "Vessel": "FreshLine",
        "Type": "Refrigerated Cargo",
        "Passengers": 0,
        "Cargo Value ($M)": 52,
        "Cargo Criticality": 80,
        "Waiting (h)": 2.8,
        "Economic Impact ($M/h)": 0.82,
        "Medical Emergency": False,
        "Perishable Cargo": True,
        "Fuel Urgency": 55,
        "Safe Entry": True,
        "Berth Time (min)": 30,
        "Tug Required": True,
        "Pilot Required": True
    },
    {
        "Vessel": "Pacific Horizon",
        "Type": "Cruise Liner",
        "Passengers": 4100,
        "Cargo Value ($M)": 0,
        "Cargo Criticality": 5,
        "Waiting (h)": 1.4,
        "Economic Impact ($M/h)": 0.56,
        "Medical Emergency": False,
        "Perishable Cargo": False,
        "Fuel Urgency": 70,
        "Safe Entry": True,
        "Berth Time (min)": 40,
        "Tug Required": True,
        "Pilot Required": True
    },
    {
        "Vessel": "Atlas Heavy",
        "Type": "Heavy Cargo",
        "Passengers": 0,
        "Cargo Value ($M)": 180,
        "Cargo Criticality": 65,
        "Waiting (h)": 5.2,
        "Economic Impact ($M/h)": 1.55,
        "Medical Emergency": False,
        "Perishable Cargo": False,
        "Fuel Urgency": 35,
        "Safe Entry": True,
        "Berth Time (min)": 60,
        "Tug Required": True,
        "Pilot Required": True
    }
])


# ============================================================
# NORMALIZATION HELPERS
# ============================================================

def normalize(series):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(
            [50] * len(series),
            index=series.index
        )

    return ((series - minimum) / (maximum - minimum) * 100)


vessels["Waiting Score"] = normalize(vessels["Waiting (h)"])
vessels["Economic Score"] = normalize(vessels["Economic Impact ($M/h)"])
vessels["Passenger Score"] = normalize(vessels["Passengers"])


# ============================================================
# SAFETY FEASIBILITY
# ============================================================

def calculate_safe_entry(row, risk):
    """
    Hard safety filter.

    This is deliberately conservative.
    It is a conceptual simulation and not a real port safety rule.
    """

    if not row["Safe Entry"]:
        return False

    if risk >= 90:
        return False

    if risk >= 75 and row["Type"] in ["Cruise Liner", "Tanker"]:
        return False

    if risk >= 65 and row["Type"] == "Cruise Liner":
        return False

    if risk >= 80 and row["Berth Time (min)"] > 45:
        return False

    return True


vessels["Currently Safe"] = vessels.apply(
    lambda row: calculate_safe_entry(row, weather_risk),
    axis=1
)


# ============================================================
# PRIORITY COMPONENTS
# ============================================================

def calculate_priority_components(row):
    """
    Calculates interpretable components of the priority score.
    """

    # Safety urgency:
    # Higher when environmental conditions are deteriorating
    # and when the vessel has a narrow safe window.
    safety_component = (
        weather_pressure * 0.65 +
        row["Fuel Urgency"] * 0.20 +
        (100 if row["Medical Emergency"] else 0) * 0.15
    )

    urgency_component = min(
        100,
        row["Waiting Score"] * 0.45 +
        row["Fuel Urgency"] * 0.25 +
        (100 if row["Perishable Cargo"] else 0) * 0.20 +
        weather_pressure * 0.10
    )

    passenger_component = row["Passenger Score"]

    cargo_component = row["Cargo Criticality"]

    waiting_component = row["Waiting Score"]

    economic_component = row["Economic Score"]

    return {
        "Safety": np.clip(safety_component, 0, 100),
        "Urgency": np.clip(urgency_component, 0, 100),
        "Passengers": np.clip(passenger_component, 0, 100),
        "Cargo": np.clip(cargo_component, 0, 100),
        "Waiting": np.clip(waiting_component, 0, 100),
        "Economic": np.clip(economic_component, 0, 100)
    }


component_rows = []

for _, row in vessels.iterrows():
    components = calculate_priority_components(row)

    component_rows.append({
        "Vessel": row["Vessel"],
        **components
    })

components_df = pd.DataFrame(component_rows)


# ============================================================
# FINAL SCORE
# ============================================================

def calculate_final_score(row, components):
    if total_weight == 0:
        return 0

    score = (
        components["Safety"] * safety_weight +
        components["Urgency"] * urgency_weight +
        components["Passengers"] * passenger_weight +
        components["Cargo"] * cargo_weight +
        components["Waiting"] * waiting_weight +
        components["Economic"] * economic_weight
    ) / total_weight

    return round(float(score), 2)


scores = []

for _, row in vessels.iterrows():
    comp = components_df[
        components_df["Vessel"] == row["Vessel"]
    ].iloc[0]

    score = calculate_final_score(row, comp)

    scores.append(score)

vessels["Priority Score"] = scores


# ============================================================
# RESOURCE FEASIBILITY
# ============================================================

def resource_feasibility(row):
    tug_ok = (
        not row["Tug Required"] or
        available_tugs > 0
    )

    pilot_ok = (
        not row["Pilot Required"] or
        available_pilots > 0
    )

    return tug_ok and pilot_ok


vessels["Resources Available"] = vessels.apply(
    resource_feasibility,
    axis=1
)


# ============================================================
# FINAL ELIGIBILITY
# ============================================================

vessels["Eligible"] = (
    vessels["Currently Safe"] &
    vessels["Resources Available"]
)


# ============================================================
# DOWNSTREAM IMPACT
# ============================================================

def downstream_impact(row):
    """
    Estimates consequences of delaying this vessel.
    This is a conceptual simulation metric.
    """

    impact = (
        row["Economic Impact ($M/h)"] * 15 +
        row["Cargo Criticality"] * 0.25 +
        row["Passengers"] / 100 +
        row["Waiting (h)"] * 8
    )

    if row["Medical Emergency"]:
        impact += 40

    if row["Perishable Cargo"]:
        impact += 20

    return round(float(np.clip(impact, 0, 100)), 2)


vessels["Downstream Impact"] = vessels.apply(
    downstream_impact,
    axis=1
)


# ============================================================
# DECISION SCORE
# ============================================================

vessels["Decision Score"] = (
    vessels["Priority Score"] * 0.75 +
    vessels["Downstream Impact"] * 0.25
)

vessels.loc[
    ~vessels["Eligible"],
    "Decision Score"
] = -1


vessels = vessels.sort_values(
    "Decision Score",
    ascending=False
).reset_index(drop=True)

vessels["Recommended Position"] = np.arange(
    1,
    len(vessels) + 1
)


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Weather risk",
        f"{weather_risk}/100",
        risk_label
    )

with col2:
    st.metric(
        "Safe vessels",
        f"{int(vessels['Eligible'].sum())}/{len(vessels)}"
    )

with col3:
    st.metric(
        "Available berths",
        available_berths
    )

with col4:
    st.metric(
        "Storm deterioration",
        f"{weather_change_minutes} min"
    )


# ============================================================
# WEATHER STATUS
# ============================================================

st.markdown("## 🌊 Current situation")

if risk_label == "CRITICAL":
    st.markdown(
        f"""
        <div class="risk-high">
            <strong>CRITICAL WEATHER CONDITIONS</strong><br>
            Current environmental risk is <strong>{weather_risk}/100</strong>.
            The system is applying a highly conservative safety filter.
            Some vessel types may be temporarily ineligible for entry.
        </div>
        """,
        unsafe_allow_html=True
    )

elif risk_label == "HIGH":
    st.markdown(
        f"""
        <div class="risk-medium">
            <strong>HIGH WEATHER RISK</strong><br>
            Environmental risk is <strong>{weather_risk}/100</strong>.
            The system is prioritizing vessels with urgent or
            high-impact consequences while preserving safety constraints.
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.markdown(
        f"""
        <div class="risk-low">
            <strong>MANAGEABLE CONDITIONS</strong><br>
            Current environmental risk is <strong>{weather_risk}/100</strong>.
            Normal prioritization logic is active.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚢 Decision Board",
    "📊 Why this order?",
    "🌪️ Scenario Simulator",
    "👤 Human Override",
    "📋 Decision Log"
])


# ============================================================
# TAB 1 — DECISION BOARD
# ============================================================

with tab1:

    st.subheader("Recommended vessel priority")

    display_df = vessels[[
        "Recommended Position",
        "Vessel",
        "Type",
        "Passengers",
        "Cargo Criticality",
        "Waiting (h)",
        "Priority Score",
        "Downstream Impact",
        "Decision Score",
        "Currently Safe",
        "Eligible"
    ]].copy()

    display_df.columns = [
        "Position",
        "Vessel",
        "Type",
        "Passengers",
        "Cargo criticality",
        "Waiting (h)",
        "Priority",
        "Downstream impact",
        "Final decision score",
        "Safe now",
        "Eligible"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Recommended sequence")

    eligible_vessels = vessels[
        vessels["Eligible"]
    ].copy()

    if len(eligible_vessels) == 0:
        st.warning(
            "No vessel currently satisfies the safety and resource constraints. "
            "The system recommends keeping all vessels in a safe waiting area."
        )
    else:
        for i, (_, row) in enumerate(
            eligible_vessels.head(available_berths).iterrows(),
            start=1
        ):
            st.markdown(
                f"""
                <div class="decision-box">
                    <strong>#{i} — {row['Vessel']}</strong><br>
                    {row['Type']} · {int(row['Passengers'])} passengers ·
                    Priority score: <strong>{row['Priority Score']}</strong><br>
                    <span class="small-muted">
                    Downstream impact: {row['Downstream Impact']}/100
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.info(
        "Important: this is a conceptual decision-support model for an academic project. "
        "It is not a real maritime safety system and does not replace port authorities, "
        "captains, pilots or official navigation rules."
    )


# ============================================================
# TAB 2 — WHY THIS ORDER?
# ============================================================

with tab2:

    st.subheader("Decision explainability")

    vessel_choice = st.selectbox(
        "Select a vessel",
        vessels["Vessel"].tolist()
    )

    selected = vessels[
        vessels["Vessel"] == vessel_choice
    ].iloc[0]

    selected_components = components_df[
        components_df["Vessel"] == vessel_choice
    ].iloc[0]

    explain_data = pd.DataFrame({
        "Factor": [
            "Safety",
            "Urgency",
            "Passenger impact",
            "Cargo criticality",
            "Waiting time",
            "Economic impact"
        ],
        "Score": [
            selected_components["Safety"],
            selected_components["Urgency"],
            selected_components["Passengers"],
            selected_components["Cargo"],
            selected_components["Waiting"],
            selected_components["Economic"]
        ]
    })

    col1, col2 = st.columns([1.4, 1])

    with col1:

        fig = px.bar(
            explain_data,
            x="Score",
            y="Factor",
            orientation="h",
            range_x=[0, 100],
            title=f"Decision factors — {vessel_choice}"
        )

        fig.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.markdown("### Decision explanation")

        if selected["Medical Emergency"]:
            st.success(
                "Medical emergency detected: urgency is significantly increased."
            )

        if selected["Perishable Cargo"]:
            st.info(
                "Perishable cargo increases the cost of prolonged waiting."
            )

        if selected["Passengers"] > 0:
            st.info(
                f"{int(selected['Passengers'])} passengers are affected by delay."
            )

        if selected["Cargo Criticality"] >= 75:
            st.info(
                "Cargo is classified as highly critical."
            )

        if weather_pressure >= 70:
            st.warning(
                "Rapid weather deterioration increases the value of using "
                "the current safe entry window."
            )

        if not selected["Currently Safe"]:
            st.error(
                "This vessel currently fails the safety filter and cannot "
                "receive an operational priority recommendation."
            )

    st.markdown("### How the final score is constructed")

    st.latex(
        r"""
        Priority =
        \frac{
        S_wS +
        U_wU +
        P_wP +
        C_wC +
        W_wW +
        E_wE
        }{
        S_w+U_w+P_w+C_w+W_w+E_w
        }
        """
    )

    st.caption(
        "The model uses normalized and interpretable components so that "
        "a human decision-maker can inspect why a vessel was prioritized."
    )


# ============================================================
# TAB 3 — SCENARIO SIMULATOR
# ============================================================

with tab3:

    st.subheader("🌪️ What happens if conditions change?")

    st.write(
        "Change one or more conditions and compare how the recommended "
        "decision changes."
    )

    scenario_col1, scenario_col2, scenario_col3 = st.columns(3)

    with scenario_col1:
        scenario_wind = st.slider(
            "Scenario wind (knots)",
            5,
            55,
            wind_speed,
            key="scenario_wind"
        )

    with scenario_col2:
        scenario_waves = st.slider(
            "Scenario waves (m)",
            0.5,
            8.0,
            wave_height,
            step=0.1,
            key="scenario_waves"
        )

    with scenario_col3:
        scenario_time = st.slider(
            "Deterioration in (min)",
            10,
            180,
            weather_change_minutes,
            key="scenario_time"
        )

    scenario_risk = calculate_weather_risk(
        scenario_wind,
        scenario_waves,
        visibility
    )

    scenario_pressure = deterioration_pressure(
        scenario_time
    )

    st.metric(
        "Scenario weather risk",
        f"{scenario_risk}/100"
    )

    scenario_vessels = vessels.copy()

    scenario_vessels["Scenario Safe"] = scenario_vessels.apply(
        lambda row: calculate_safe_entry(
            row,
            scenario_risk
        ),
        axis=1
    )

    scenario_vessels["Scenario Pressure"] = scenario_pressure

    scenario_vessels["Scenario Decision"] = (
        scenario_vessels["Decision Score"]
    )

    scenario_vessels.loc[
        ~scenario_vessels["Scenario Safe"],
        "Scenario Decision"
    ] = -1

    scenario_vessels = scenario_vessels.sort_values(
        "Scenario Decision",
        ascending=False
    )

    scenario_table = scenario_vessels[[
        "Vessel",
        "Type",
        "Scenario Safe",
        "Scenario Decision"
    ]].copy()

    scenario_table.columns = [
        "Vessel",
        "Type",
        "Safe under scenario",
        "Decision score"
    ]

    st.dataframe(
        scenario_table,
        use_container_width=True,
        hide_index=True
    )

    if st.button(
        "RUN SCENARIO",
        type="primary"
    ):
        st.session_state.simulation_ran = True

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        st.session_state.decision_log.append({
            "Time": timestamp,
            "Event": "Scenario simulation",
            "Wind": scenario_wind,
            "Waves": scenario_waves,
            "Weather risk": scenario_risk,
            "Deterioration": scenario_time
        })

        st.success(
            "Scenario simulated. The decision order has been recalculated."
        )

    # Compare baseline and scenario
    baseline_order = vessels[
        vessels["Eligible"]
    ]["Vessel"].tolist()

    scenario_order = scenario_vessels[
        scenario_vessels["Scenario Safe"]
    ]["Vessel"].tolist()

    comparison = pd.DataFrame({
        "Baseline": pd.Series(baseline_order),
        "Scenario": pd.Series(scenario_order)
    })

    st.markdown("### Baseline vs scenario")

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 4 — HUMAN OVERRIDE
# ============================================================

with tab4:

    st.subheader("👤 Human override")

    st.write(
        "The algorithm is a decision-support tool, not the final authority. "
        "A port coordinator may override the recommendation when new information "
        "is unavailable to the model."
    )

    override_vessel = st.selectbox(
        "Choose a vessel to manually prioritize",
        vessels["Vessel"].tolist(),
        key="override_vessel"
    )

    override_reason = st.text_area(
        "Reason for override",
        placeholder=(
            "Example: Unexpected medical emergency aboard the vessel. "
            "The information was received after the latest algorithm update."
        )
    )

    if st.button(
        "APPLY HUMAN OVERRIDE",
        type="secondary"
    ):

        if not override_reason.strip():
            st.error(
                "Please provide a reason for the override."
            )

        else:

            current_order = vessels[
                vessels["Eligible"]
            ]["Vessel"].tolist()

            if override_vessel in current_order:
                current_order.remove(
                    override_vessel
                )

            current_order.insert(
                0,
                override_vessel
            )

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            st.session_state.decision_log.append({
                "Time": timestamp,
                "Event": "Human override",
                "Vessel": override_vessel,
                "Reason": override_reason
            })

            st.success(
                f"{override_vessel} has been moved to priority position #1."
            )

            st.markdown("### Revised decision")

            for i, vessel_name in enumerate(
                current_order[:available_berths],
                start=1
            ):
                st.write(
                    f"**#{i} — {vessel_name}**"
                )

            st.caption(
                "The override is logged so that the system maintains "
                "an auditable decision history."
            )


# ============================================================
# TAB 5 — DECISION LOG
# ============================================================

with tab5:

    st.subheader("📋 Decision history")

    if not st.session_state.decision_log:

        st.info(
            "No decisions have been logged yet. "
            "Run a scenario or apply a human override."
        )

    else:

        log_df = pd.DataFrame(
            st.session_state.decision_log
        )

        st.dataframe(
            log_df,
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "Clear decision log"
        ):
            st.session_state.decision_log = []
            st.rerun()


# ============================================================
# RESEARCH SECTION
# ============================================================

st.divider()

st.markdown("## 🧠 Research question")

st.markdown(
    """
    **How should a port prioritize vessels when severe weather creates
    a temporary shortage of safe berthing capacity?**
    
    The system explores the conflict between:
    
    - **safety**
    - **passenger welfare**
    - **critical cargo**
    - **economic consequences**
    - **waiting time**
    - **limited infrastructure**
    - **uncertain weather**
    
    Rather than searching for a universally "correct" order, the model
    demonstrates how different decision priorities produce different
    outcomes.
    """
)

st.markdown("## ⚠️ Model limitation")

st.caption(
    "This application is an academic simulation. Its numerical thresholds, "
    "weights and safety filters are illustrative and must not be used for "
    "real maritime navigation or operational decisions."
)
