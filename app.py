import streamlit as st
import pandas as pd
import numpy as np
import itertools
import math
from datetime import datetime

# ============================================================
# PORT PRIORITY SYSTEM 2.0
# Academic decision-support simulation
# ============================================================

st.set_page_config(
    page_title="Port Priority System",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>
.main {
    background: #f7f9fc;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(135deg, #081c2e, #17466b);
    color: white;
    padding: 2rem 2.3rem;
    border-radius: 20px;
    margin-bottom: 1.5rem;
}

.hero h1 {
    font-size: 2.5rem;
    margin: 0;
}

.hero p {
    margin-top: 0.5rem;
    opacity: 0.85;
    font-size: 1.05rem;
}

.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 15px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}

.good {
    background: #edf9f1;
    border-left: 5px solid #2e9d62;
    padding: 1rem;
    border-radius: 10px;
}

.warning {
    background: #fff8e7;
    border-left: 5px solid #e2a51c;
    padding: 1rem;
    border-radius: 10px;
}

.danger {
    background: #fff0f0;
    border-left: 5px solid #d64545;
    padding: 1rem;
    border-radius: 10px;
}

.small {
    color: #667085;
    font-size: 0.88rem;
}

.sequence {
    background: white;
    border: 1px solid #dbe3ec;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin: 0.5rem 0;
}

.big-number {
    font-size: 2rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "decision_log" not in st.session_state:
    st.session_state.decision_log = []

if "optimization_result" not in st.session_state:
    st.session_state.optimization_result = None


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <h1>⚓ PORT PRIORITY SYSTEM</h1>
    <p>
        Decision-support system for vessel sequencing,
        resource allocation and risk management during severe weather.
    </p>
</div>
""", unsafe_allow_html=True)

st.caption(
    "Academic simulation — designed to explore decision-making under "
    "uncertainty, limited infrastructure and competing priorities."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🌊 WEATHER")

wind = st.sidebar.slider(
    "Wind speed (knots)",
    5, 55, 28
)

waves = st.sidebar.slider(
    "Wave height (m)",
    0.5, 8.0, 4.2, 0.1
)

visibility = st.sidebar.slider(
    "Visibility (km)",
    0.2, 15.0, 1.8, 0.1
)

deterioration = st.sidebar.slider(
    "Severe deterioration expected in (min)",
    10, 180, 35
)

st.sidebar.divider()

st.sidebar.header("⚓ PORT CAPACITY")

berths = st.sidebar.number_input(
    "Available berths",
    1, 6, 3
)

tugs = st.sidebar.number_input(
    "Available tugboats",
    0, 6, 2
)

pilots = st.sidebar.number_input(
    "Available pilots",
    0, 6, 1
)

st.sidebar.divider()

st.sidebar.header("🎯 DECISION PRIORITIES")

safety_weight = st.sidebar.slider(
    "Safety",
    0, 100, 30
)

passenger_weight = st.sidebar.slider(
    "Passenger impact",
    0, 100, 15
)

cargo_weight = st.sidebar.slider(
    "Critical cargo",
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
    wind_score = np.clip((wind - 10) / 40 * 100, 0, 100)
    wave_score = np.clip((waves - 0.5) / 7.5 * 100, 0, 100)
    visibility_score = np.clip((8 - visibility) / 8 * 100, 0, 100)

    return round(
        0.4 * wind_score +
        0.4 * wave_score +
        0.2 * visibility_score,
        1
    )


current_risk = weather_risk(
    wind,
    waves,
    visibility
)


def weather_label(risk):
    if risk >= 80:
        return "CRITICAL"
    if risk >= 60:
        return "HIGH"
    if risk >= 35:
        return "MODERATE"
    return "LOW"


risk_label = weather_label(current_risk)


# ============================================================
# VESSEL DATA
# ============================================================

vessels = pd.DataFrame([
    {
        "Vessel": "Ocean Star",
        "Type": "Cruise Liner",
        "Passengers": 2840,
        "Cargo Criticality": 5,
        "Economic Impact": 0.42,
        "Waiting": 3.3,
        "Service Time": 35,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": True,
        "Perishable": False,
        "Fuel Urgency": 65,
        "Max Wind": 32,
        "Max Waves": 4.5
    },
    {
        "Vessel": "Pacific Horizon",
        "Type": "Cruise Liner",
        "Passengers": 4100,
        "Cargo Criticality": 5,
        "Economic Impact": 0.56,
        "Waiting": 1.4,
        "Service Time": 40,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel Urgency": 70,
        "Max Wind": 30,
        "Max Waves": 4.0
    },
    {
        "Vessel": "MedExpress",
        "Type": "Medical Cargo",
        "Passengers": 0,
        "Cargo Criticality": 100,
        "Economic Impact": 0.75,
        "Waiting": 0.8,
        "Service Time": 25,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": True,
        "Fuel Urgency": 40,
        "Max Wind": 40,
        "Max Waves": 5.5
    },
    {
        "Vessel": "Baltic Trader",
        "Type": "Container Ship",
        "Passengers": 0,
        "Cargo Criticality": 55,
        "Economic Impact": 1.35,
        "Waiting": 2.2,
        "Service Time": 50,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel Urgency": 50,
        "Max Wind": 38,
        "Max Waves": 5.0
    },
    {
        "Vessel": "Aurora",
        "Type": "Tanker",
        "Passengers": 0,
        "Cargo Criticality": 70,
        "Economic Impact": 1.10,
        "Waiting": 1.7,
        "Service Time": 45,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel Urgency": 95,
        "Max Wind": 34,
        "Max Waves": 4.5
    },
    {
        "Vessel": "Northern Wind",
        "Type": "Ferry",
        "Passengers": 720,
        "Cargo Criticality": 35,
        "Economic Impact": 0.18,
        "Waiting": 4.1,
        "Service Time": 20,
        "Tugs": 0,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel Urgency": 65,
        "Max Wind": 36,
        "Max Waves": 5.0
    },
    {
        "Vessel": "FreshLine",
        "Type": "Refrigerated Cargo",
        "Passengers": 0,
        "Cargo Criticality": 80,
        "Economic Impact": 0.82,
        "Waiting": 2.8,
        "Service Time": 30,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": True,
        "Fuel Urgency": 55,
        "Max Wind": 37,
        "Max Waves": 5.0
    },
    {
        "Vessel": "Atlas Heavy",
        "Type": "Heavy Cargo",
        "Passengers": 0,
        "Cargo Criticality": 65,
        "Economic Impact": 1.55,
        "Waiting": 5.2,
        "Service Time": 60,
        "Tugs": 1,
        "Pilots": 1,
        "Medical": False,
        "Perishable": False,
        "Fuel Urgency": 35,
        "Max Wind": 35,
        "Max Waves": 4.5
    }
])


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

    return (series - low) / (high - low) * 100


vessels["Passenger Score"] = normalize(
    vessels["Passengers"]
)

vessels["Economic Score"] = normalize(
    vessels["Economic Impact"]
)

vessels["Waiting Score"] = normalize(
    vessels["Waiting"]
)


# ============================================================
# SAFETY MODEL
# ============================================================

def safety_status(row, risk):

    wind_safe = wind <= row["Max Wind"]
    wave_safe = waves <= row["Max Waves"]

    if wind_safe and wave_safe:
        return True

    return False


vessels["Safe Now"] = vessels.apply(
    lambda row: safety_status(row, current_risk),
    axis=1
)


# ============================================================
# WEATHER WINDOW
# ============================================================

def weather_window_score(row):

    wind_margin = max(
        0,
        row["Max Wind"] - wind
    )

    wave_margin = max(
        0,
        row["Max Waves"] - waves
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


vessels["Weather Window"] = vessels.apply(
    weather_window_score,
    axis=1
)


# ============================================================
# PRIORITY MODEL
# ============================================================

def base_priority(row):

    medical_bonus = 35 if row["Medical"] else 0
    perish_bonus = 20 if row["Perishable"] else 0

    safety_score = (
        100
        if row["Safe Now"]
        else 0
    )

    urgency = min(
        100,
        row["Fuel Urgency"] * 0.6 +
        row["Waiting Score"] * 0.25 +
        perish_bonus +
        medical_bonus
    )

    if weight_sum == 0:
        return 0

    score = (
        safety_score * safety_weight +
        row["Passenger Score"] * passenger_weight +
        row["Cargo Criticality"] * cargo_weight +
        row["Economic Score"] * economic_weight +
        row["Waiting Score"] * waiting_weight +
        row["Weather Window"] * weather_weight
    ) / weight_sum

    # Emergency bonus
    score += medical_bonus * 0.15
    score += perish_bonus * 0.08

    return round(
        min(100, score),
        2
    )


vessels["Priority"] = vessels.apply(
    base_priority,
    axis=1
)


# ============================================================
# OPERATIONAL FEASIBILITY
# ============================================================

def resource_feasible(row):

    if row["Tugs"] > tugs:
        return False

    if row["Pilots"] > pilots:
        return False

    return True


vessels["Resources Available"] = vessels.apply(
    resource_feasible,
    axis=1
)


vessels["Eligible"] = (
    vessels["Safe Now"] &
    vessels["Resources Available"]
)


# ============================================================
# COST OF DELAY
# ============================================================

def delay_cost(row, delay_minutes):

    delay_hours = delay_minutes / 60

    cost = (
        row["Economic Impact"] *
        delay_hours
    )

    # passenger welfare component
    passenger_cost = (
        row["Passengers"] *
        0.00008 *
        delay_hours
    )

    # critical cargo
    cargo_cost = (
        row["Cargo Criticality"] /
        100 *
        0.25 *
        delay_hours
    )

    # medical emergency
    medical_cost = (
        2.5 * delay_hours
        if row["Medical"]
        else 0
    )

    # perishables
    perish_cost = (
        1.2 * delay_hours
        if row["Perishable"]
        else 0
    )

    # waiting itself creates increasing pressure
    waiting_penalty = (
        row["Waiting"] *
        0.04 *
        delay_hours
    )

    return (
        cost +
        passenger_cost +
        cargo_cost +
        medical_cost +
        perish_cost +
        waiting_penalty
    )


# ============================================================
# OPTIMIZATION ENGINE
# ============================================================

def sequence_cost(sequence, data):

    current_time = 0

    total_cost = 0

    details = []

    for name in sequence:

        row = data[
            data["Vessel"] == name
        ].iloc[0]

        start_time = current_time
        finish_time = (
            current_time +
            row["Service Time"]
        )

        # If the vessel becomes unsafe before its turn,
        # applying a severe penalty.
        safe_until_storm = deterioration

        safety_penalty = 0

        if start_time > safe_until_storm:
            safety_penalty += 20

        if start_time <= safe_until_storm:

            if not row["Safe Now"]:
                safety_penalty += 100

        delay = start_time

        cost = delay_cost(
            row,
            delay
        )

        # Strongly penalize unsafe entry
        if not row["Safe Now"]:
            cost += 100

        cost += safety_penalty

        total_cost += cost

        details.append({
            "Vessel": name,
            "Start": start_time,
            "Finish": finish_time,
            "Delay": delay,
            "Cost": cost
        })

        current_time = finish_time

    return total_cost, details


def optimize_sequence(data):

    eligible = data[
        data["Eligible"]
    ].copy()

    if len(eligible) == 0:
        return None

    names = eligible["Vessel"].tolist()

    best_sequence = None
    best_cost = float("inf")
    best_details = None

    # For 8 vessels this is still computationally manageable.
    # 8! = 40,320 possible sequences.
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
        "sequence": best_sequence,
        "cost": best_cost,
        "details": best_details
    }


optimization = optimize_sequence(
    vessels
)


# ============================================================
# ALTERNATIVE STRATEGIES
# ============================================================

def strategy_sequence(data, strategy):

    eligible = data[
        data["Eligible"]
    ].copy()

    if len(eligible) == 0:
        return []

    if strategy == "Priority-first":
        return eligible.sort_values(
            "Priority",
            ascending=False
        )["Vessel"].tolist()

    if strategy == "Economic-first":
        return eligible.sort_values(
            "Economic Impact",
            ascending=False
        )["Vessel"].tolist()

    if strategy == "Passenger-first":
        return eligible.sort_values(
            "Passengers",
            ascending=False
        )["Vessel"].tolist()

    if strategy == "Critical-cargo-first":
        return eligible.sort_values(
            "Cargo Criticality",
            ascending=False
        )["Vessel"].tolist()

    if strategy == "Waiting-time-first":
        return eligible.sort_values(
            "Waiting",
            ascending=False
        )["Vessel"].tolist()

    return []


def evaluate_sequence(sequence, data):

    if not sequence:
        return 0

    cost, details = sequence_cost(
        sequence,
        data[
            data["Vessel"].isin(sequence)
        ]
    )

    return round(cost, 3)


strategies = [
    "Priority-first",
    "Economic-first",
    "Passenger-first",
    "Critical-cargo-first",
    "Waiting-time-first"
]

strategy_results = []

for strategy in strategies:

    seq = strategy_sequence(
        vessels,
        strategy
    )

    cost = evaluate_sequence(
        seq,
        vessels
    )

    strategy_results.append({
        "Strategy": strategy,
        "Cost": cost
    })


if optimization:

    strategy_results.append({
        "Strategy": "OPTIMIZED",
        "Cost": round(
            optimization["cost"],
            3
        )
    })

strategy_df = pd.DataFrame(
    strategy_results
).sort_values(
    "Cost"
)


# ============================================================
# TOP METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Weather risk",
        f"{current_risk}/100",
        risk_label
    )

with m2:
    st.metric(
        "Safe vessels",
        f"{int(vessels['Eligible'].sum())}/{len(vessels)}"
    )

with m3:
    st.metric(
        "Available berths",
        int(berths)
    )

with m4:
    if optimization:
        st.metric(
            "Optimal sequence cost",
            f"{optimization['cost']:.2f}"
        )
    else:
        st.metric(
            "Optimal sequence",
            "NONE"
        )


# ============================================================
# WEATHER STATUS
# ============================================================

st.markdown("## 🌊 Current operational situation")

if current_risk >= 80:

    st.markdown(
        f"""
        <div class="danger">
        <strong>CRITICAL CONDITIONS</strong><br>
        Environmental risk: {current_risk}/100.
        The model applies a strict safety filter.
        </div>
        """,
        unsafe_allow_html=True
    )

elif current_risk >= 60:

    st.markdown(
        f"""
        <div class="warning">
        <strong>HIGH WEATHER RISK</strong><br>
        Environmental risk: {current_risk}/100.
        The available safe operating window is becoming limited.
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        f"""
        <div class="good">
        <strong>MANAGEABLE CONDITIONS</strong><br>
        Environmental risk: {current_risk}/100.
        Standard prioritization is active.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚓ OPTIMAL PLAN",
    "📊 WHY?",
    "🌪️ SCENARIOS",
    "👤 HUMAN OVERRIDE",
    "📋 DECISION LOG"
])


# ============================================================
# TAB 1 — OPTIMAL PLAN
# ============================================================

with tab1:

    st.subheader("Optimal operational sequence")

    if optimization is None:

        st.error(
            "No vessel currently satisfies the safety and resource constraints."
        )

    else:

        st.markdown(
            f"""
            <div class="card">
            <strong>Optimization objective</strong><br>
            Minimize the estimated total cost of delay, passenger impact,
            cargo disruption and safety-related penalties while respecting
            current operational constraints.
            </div>
            """,
            unsafe_allow_html=True
        )

        for i, item in enumerate(
            optimization["details"],
            start=1
        ):

            row = vessels[
                vessels["Vessel"] == item["Vessel"]
            ].iloc[0]

            icon = "🛳️"

            if row["Type"] == "Medical Cargo":
                icon = "💊"
            elif row["Type"] == "Tanker":
                icon = "🛢️"
            elif row["Type"] == "Container Ship":
                icon = "📦"
            elif row["Type"] == "Ferry":
                icon = "⛴️"

            st.markdown(
                f"""
                <div class="sequence">
                <strong>#{i} {icon} {item['Vessel']}</strong><br>
                {row['Type']}<br>
                <span class="small">
                Starts at +{item['Start']:.0f} min ·
                completes at +{item['Finish']:.0f} min ·
                estimated delay: {item['Delay']:.0f} min
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### Operational comparison")

        st.dataframe(
            strategy_df,
            use_container_width=True,
            hide_index=True
        )

        chart = strategy_df.sort_values(
            "Cost"
        )

        st.bar_chart(
            chart.set_index("Strategy")["Cost"]
        )

        st.success(
            "The optimized sequence is selected by minimizing the model's "
            "estimated total operational cost rather than maximizing a single priority score."
        )


# ============================================================
# TAB 2 — WHY
# ============================================================

with tab2:

    st.subheader("Why did the model choose this order?")

    if optimization:

        selected_vessel = st.selectbox(
            "Select vessel",
            optimization["sequence"]
        )

        row = vessels[
            vessels["Vessel"] == selected_vessel
        ].iloc[0]

        factors = pd.DataFrame({
            "Factor": [
                "Passenger impact",
                "Cargo criticality",
                "Economic impact",
                "Waiting time",
                "Weather window",
                "Fuel urgency"
            ],
            "Value": [
                row["Passenger Score"],
                row["Cargo Criticality"],
                row["Economic Score"],
                row["Waiting Score"],
                row["Weather Window"],
                row["Fuel Urgency"]
            ]
        })

        st.bar_chart(
            factors.set_index("Factor")
        )

        st.markdown("### Decision explanation")

        if row["Medical"]:
            st.success(
                "Medical emergency detected: the model increases the cost of delay."
            )

        if row["Perishable"]:
            st.info(
                "Perishable cargo increases the estimated consequences of waiting."
            )

        if row["Passengers"] > 0:
            st.info(
                f"This vessel carries {int(row['Passengers']):,} passengers."
            )

        if row["Cargo Criticality"] >= 80:
            st.info(
                "The cargo has very high criticality."
            )

        if row["Economic Impact"] >= 1:
            st.info(
                "Delay has substantial estimated economic consequences."
            )

        if not row["Safe Now"]:
            st.error(
                "This vessel is currently outside its simulated safe operating envelope."
            )

        st.markdown("### Model principle")

        st.write(
            "The system does not assume that the vessel with the highest "
            "individual priority should always go first. It evaluates how "
            "each vessel's position in the sequence changes the consequences "
            "for the entire queue."
        )


# ============================================================
# TAB 3 — SCENARIOS
# ============================================================

with tab3:

    st.subheader("🌪️ Scenario laboratory")

    st.write(
        "Change the conditions and observe how the optimal strategy changes."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        scenario_wind = st.slider(
            "Scenario wind",
            5,
            55,
            wind,
            key="scenario_wind"
        )

    with c2:
        scenario_waves = st.slider(
            "Scenario waves",
            0.5,
            8.0,
            waves,
            0.1,
            key="scenario_waves"
        )

    with c3:
        scenario_deterioration = st.slider(
            "Scenario deterioration",
            10,
            180,
            deterioration,
            key="scenario_deterioration"
        )

    scenario_risk = weather_risk(
        scenario_wind,
        scenario_waves,
        visibility
    )

    st.metric(
        "Scenario risk",
        f"{scenario_risk}/100"
    )

    scenario_data = vessels.copy()

    scenario_data["Safe Now"] = scenario_data.apply(
        lambda row: (
            scenario_wind <= row["Max Wind"] and
            scenario_waves <= row["Max Waves"]
        ),
        axis=1
    )

    scenario_data["Eligible"] = (
        scenario_data["Safe Now"] &
        scenario_data["Resources Available"]
    )

    # Temporarily update weather window
    old_wind = wind
    old_waves = waves
    old_deterioration = deterioration

    # calculate scenario window manually
    def scenario_window(row):

        wind_margin = max(
            0,
            row["Max Wind"] - scenario_wind
        )

        wave_margin = max(
            0,
            row["Max Waves"] - scenario_waves
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
            100 - scenario_deterioration / 1.8
        )

        return (
            0.35 * wind_score +
            0.35 * wave_score +
            0.30 * urgency
        )

    scenario_data["Weather Window"] = scenario_data.apply(
        scenario_window,
        axis=1
    )

    # Recalculate priority for scenario
    scenario_priorities = []

    for _, row in scenario_data.iterrows():

        safety_score = (
            100 if row["Safe Now"] else 0
        )

        score = (
            safety_score * safety_weight +
            row["Passenger Score"] * passenger_weight +
            row["Cargo Criticality"] * cargo_weight +
            row["Economic Score"] * economic_weight +
            row["Waiting Score"] * waiting_weight +
            row["Weather Window"] * weather_weight
        )

        if weight_sum > 0:
            score /= weight_sum

        if row["Medical"]:
            score += 5

        if row["Perishable"]:
            score += 3

        scenario_priorities.append(
            min(100, score)
        )

    scenario_data["Priority"] = scenario_priorities

    scenario_sequence = scenario_data[
        scenario_data["Eligible"]
    ].sort_values(
        "Priority",
        ascending=False
    )["Vessel"].tolist()

    if scenario_sequence:

        st.markdown("### Scenario recommendation")

        for i, name in enumerate(
            scenario_sequence,
            1
        ):
            st.write(
                f"**#{i} — {name}**"
            )

        if optimization:

            baseline = optimization["sequence"]

            changed = (
                scenario_sequence !=
                list(baseline)
            )

            if changed:

                st.warning(
                    "The scenario changes the recommended sequence."
                )

            else:

                st.success(
                    "The recommended sequence remains stable under this scenario."
                )

    else:

        st.error(
            "No vessel can currently enter safely under this scenario."
        )


# ============================================================
# TAB 4 — HUMAN OVERRIDE
# ============================================================

with tab4:

    st.subheader("👤 Human override")

    st.write(
        "The system is deliberately designed so that the algorithm "
        "does not have absolute authority. A human decision-maker "
        "can introduce information that the model does not have."
    )

    if optimization:

        override_vessel = st.selectbox(
            "Vessel to prioritize manually",
            list(optimization["sequence"])
        )

        reason = st.text_area(
            "Reason for override",
            placeholder=(
                "Example: A new medical emergency was reported "
                "after the latest data update."
            )
        )

        if st.button(
            "APPLY OVERRIDE",
            type="primary"
        ):

            if not reason.strip():

                st.error(
                    "A reason is required."
                )

            else:

                new_sequence = list(
                    optimization["sequence"]
                )

                new_sequence.remove(
                    override_vessel
                )

                new_sequence.insert(
                    0,
                    override_vessel
                )

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                st.session_state.decision_log.append({
                    "Time": timestamp,
                    "Type": "Human override",
                    "Vessel": override_vessel,
                    "Reason": reason
                })

                original_cost = evaluate_sequence(
                    optimization["sequence"],
                    vessels
                )

                override_cost = evaluate_sequence(
                    new_sequence,
                    vessels
                )

                st.success(
                    f"{override_vessel} moved to priority #1."
                )

                st.metric(
                    "Estimated cost difference",
                    f"{override_cost - original_cost:+.2f}"
                )

                st.markdown("### Revised sequence")

                for i, name in enumerate(
                    new_sequence,
                    1
                ):

                    st.write(
                        f"**#{i} — {name}**"
                    )

                st.caption(
                    "A higher estimated cost does not necessarily mean "
                    "the human decision is wrong: the human may possess "
                    "information not represented in the model."
                )


# ============================================================
# TAB 5 — LOG
# ============================================================

with tab5:

    st.subheader("📋 Decision history")

    if not st.session_state.decision_log:

        st.info(
            "No human overrides have been recorded yet."
        )

    else:

        log = pd.DataFrame(
            st.session_state.decision_log
        )

        st.dataframe(
            log,
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "Clear log"
        ):

            st.session_state.decision_log = []

            st.rerun()


# ============================================================
# RESEARCH SECTION
# ============================================================

st.divider()

st.markdown("## 🔬 Research logic")

st.write(
    """
    The central research question is not simply which vessel should enter first.
    It is how a port should allocate scarce infrastructure when several
    legitimate priorities conflict at the same time.
    """
)

r1, r2, r3 = st.columns(3)

with r1:

    st.markdown(
        """
        ### Safety

        A vessel outside its simulated safe operating envelope
        cannot receive a normal operational recommendation.
        """
    )

with r2:

    st.markdown(
        """
        ### Optimization

        The model evaluates possible sequences and estimates
        the total consequences of delaying different vessels.
        """
    )

with r3:

    st.markdown(
        """
        ### Human judgment

        The final decision remains with a human operator,
        especially when new information is unavailable to the model.
        """
    )


st.markdown("## ⚠️ Important limitation")

st.caption(
    "This is an academic simulation. Numerical thresholds, cost functions "
    "and safety limits are illustrative and are not maritime regulations. "
    "The system must not be used for real navigation or port operations."
)

st.caption(
    "Version 2.0 · Port Priority System"
)
