import streamlit as st
from datetime import datetime

# ============================================================
# MARITIME FLOW
# Vessel Sequencing & Port Decision Support System
# FINAL VERSION
# ============================================================

st.set_page_config(
    page_title="Maritime Flow",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                180deg,
                #071b2b 0%,
                #09283e 45%,
                #0d3a52 100%
            );
        color: #eef7fb;
    }

    section[data-testid="stSidebar"] {
        background: #061522;
        border-right: 1px solid rgba(130, 200, 220, 0.20);
    }

    .main-title {
        font-size: 46px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 4px;
        color: #f4fbff;
    }

    .subtitle {
        font-size: 17px;
        color: #a9c7d5;
        margin-bottom: 24px;
    }

    .wave {
        height: 5px;
        width: 100%;
        margin: 10px 0 28px 0;
        border-radius: 10px;
        background:
            linear-gradient(
                90deg,
                #4bc0d9,
                #77d8e8,
                #4bc0d9,
                #1c718c,
                #4bc0d9
            );
    }

    .metric-card {
        background: rgba(7, 31, 47, 0.82);
        border: 1px solid rgba(113, 193, 216, 0.20);
        border-radius: 16px;
        padding: 18px;
        min-height: 105px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }

    .metric-label {
        color: #8eafbd;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        color: #f3fbff;
        font-size: 29px;
        font-weight: 750;
        margin-top: 6px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 750;
        margin-top: 32px;
        margin-bottom: 12px;
        color: #f4fbff;
    }

    .section-description {
        color: #a9c7d5;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .info-box {
        background: rgba(10, 42, 61, 0.78);
        border-left: 4px solid #4bc0d9;
        border-radius: 10px;
        padding: 15px 18px;
        margin: 10px 0;
        color: #d9edf3;
    }

    .warning-box {
        background: rgba(92, 67, 23, 0.35);
        border-left: 4px solid #e4b85c;
        border-radius: 10px;
        padding: 15px 18px;
        margin: 10px 0;
        color: #f3e4bd;
    }

    .success-box {
        background: rgba(20, 91, 78, 0.35);
        border-left: 4px solid #4dd6b1;
        border-radius: 10px;
        padding: 15px 18px;
        margin: 10px 0;
        color: #d9f7ef;
    }

    .danger-box {
        background: rgba(100, 35, 45, 0.35);
        border-left: 4px solid #e66b78;
        border-radius: 10px;
        padding: 15px 18px;
        margin: 10px 0;
        color: #f4dadd;
    }

    .vessel-card {
        background: rgba(6, 26, 41, 0.88);
        border: 1px solid rgba(105, 182, 205, 0.18);
        border-radius: 14px;
        padding: 17px;
        margin-bottom: 12px;
    }

    .vessel-name {
        font-size: 19px;
        font-weight: 700;
        color: #f4fbff;
    }

    .vessel-meta {
        font-size: 13px;
        color: #8eafbd;
        margin-top: 4px;
    }

    .sequence-number {
        font-size: 28px;
        font-weight: 800;
        color: #4bc0d9;
    }

    .score {
        font-size: 24px;
        font-weight: 750;
        color: #f4fbff;
    }

    .small-label {
        color: #7f9eac;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    div[data-testid="stButton"] button {
        border-radius: 10px;
        font-weight: 650;
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 10px;
        font-weight: 650;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# VESSEL DATABASE
# ============================================================

VESSELS = [
    {
        "name": "Baltic Horizon",
        "type": "Container",
        "loa": 240,
        "draft": 9.2,
        "priority": 5,
        "eta": 35,
        "cargo": 1800,
        "resource": "Crane A",
        "weather_limit": 6.0,
        "urgency": 5,
        "service_time": 55
    },
    {
        "name": "Northern Star",
        "type": "Bulk Carrier",
        "loa": 210,
        "draft": 10.4,
        "priority": 4,
        "eta": 10,
        "cargo": 3200,
        "resource": "Crane B",
        "weather_limit": 5.0,
        "urgency": 4,
        "service_time": 70
    },
    {
        "name": "Aurora",
        "type": "Tanker",
        "loa": 185,
        "draft": 8.7,
        "priority": 5,
        "eta": 55,
        "cargo": 2400,
        "resource": "Terminal 2",
        "weather_limit": 4.5,
        "urgency": 5,
        "service_time": 65
    },
    {
        "name": "Ocean Pearl",
        "type": "Container",
        "loa": 160,
        "draft": 7.9,
        "priority": 3,
        "eta": 20,
        "cargo": 1100,
        "resource": "Crane A",
        "weather_limit": 7.0,
        "urgency": 3,
        "service_time": 45
    },
    {
        "name": "Blue Meridian",
        "type": "Ro-Ro",
        "loa": 195,
        "draft": 8.1,
        "priority": 3,
        "eta": 5,
        "cargo": 850,
        "resource": "Ramp 1",
        "weather_limit": 8.0,
        "urgency": 3,
        "service_time": 40
    },
    {
        "name": "Sea Falcon",
        "type": "General Cargo",
        "loa": 145,
        "draft": 7.4,
        "priority": 2,
        "eta": 15,
        "cargo": 900,
        "resource": "Crane B",
        "weather_limit": 6.5,
        "urgency": 2,
        "service_time": 40
    }
]


# ============================================================
# SESSION STATE
# ============================================================

if "vessels" not in st.session_state:
    st.session_state.vessels = [dict(v) for v in VESSELS]

if "plan" not in st.session_state:
    st.session_state.plan = None

if "audit" not in st.session_state:
    st.session_state.audit = []

if "manual_order" not in st.session_state:
    st.session_state.manual_order = []


# ============================================================
# CORE LOGIC
# ============================================================

def weather_status(vessel, waves):
    limit = vessel["weather_limit"]

    if waves > limit:
        return "UNSAFE"

    if waves >= limit - 1:
        return "RESTRICTED"

    return "SAFE"


def resource_availability(resource, resource_state):
    state = resource_state.get(resource, "Available")

    if state == "Unavailable":
        return "UNAVAILABLE"

    if state == "Limited":
        return "LIMITED"

    return "AVAILABLE"


def vessel_score(
    vessel,
    waves,
    resource_state,
    position,
    current_time
):
    weather = weather_status(vessel, waves)
    resource = resource_availability(
        vessel["resource"],
        resource_state
    )

    # Hard constraints
    if weather == "UNSAFE":
        return -1000, {
            "priority": 0,
            "urgency": 0,
            "arrival": 0,
            "weather": 0,
            "resource": 0,
            "cargo": 0,
            "waiting": 0,
            "service": 0
        }

    if resource == "UNAVAILABLE":
        return -900, {
            "priority": 0,
            "urgency": 0,
            "arrival": 0,
            "weather": 0,
            "resource": 0,
            "cargo": 0,
            "waiting": 0,
            "service": 0
        }

    # --------------------------------------------------------
    # 1. Operational priority
    # --------------------------------------------------------

    priority_score = vessel["priority"] * 4.0

    # --------------------------------------------------------
    # 2. Urgency
    # --------------------------------------------------------

    urgency_score = vessel["urgency"] * 3.2

    # --------------------------------------------------------
    # 3. Arrival / waiting
    # --------------------------------------------------------

    ready_time = vessel["eta"]

    if current_time >= ready_time:
        waiting = current_time - ready_time
        arrival_score = min(10.0, waiting / 5.0)
        waiting_score = min(10.0, waiting / 6.0)
    else:
        arrival_score = -8.0
        waiting_score = 0.0

    # --------------------------------------------------------
    # 4. Weather compatibility
    # --------------------------------------------------------

    if weather == "SAFE":
        weather_score = 10.0
    else:
        weather_score = 3.0

    # --------------------------------------------------------
    # 5. Resource pressure
    # --------------------------------------------------------

    if resource == "AVAILABLE":
        resource_score = 7.0
    else:
        resource_score = -3.0

    # --------------------------------------------------------
    # 6. Cargo importance
    # --------------------------------------------------------

    cargo_score = min(vessel["cargo"] / 500.0, 8.0)

    # --------------------------------------------------------
    # 7. Service efficiency
    # --------------------------------------------------------

    service_score = max(
        0.0,
        8.0 - vessel["service_time"] / 10.0
    )

    # --------------------------------------------------------
    # Position penalty
    # Prevents the algorithm from blindly repeating
    # the same vessel characteristics.
    # --------------------------------------------------------

    position_penalty = position * 0.7

    total = (
        priority_score
        + urgency_score
        + arrival_score
        + weather_score
        + resource_score
        + cargo_score
        + waiting_score
        + service_score
        - position_penalty
    )

    factors = {
        "priority": priority_score,
        "urgency": urgency_score,
        "arrival": arrival_score,
        "weather": weather_score,
        "resource": resource_score,
        "cargo": cargo_score,
        "waiting": waiting_score,
        "service": service_score
    }

    return total, factors


def optimize_sequence(vessels, waves, resource_state):
    remaining = [dict(v) for v in vessels]

    sequence = []
    current_time = 0

    # Greedy sequence construction:
    # At each step, evaluate every feasible remaining vessel
    # against the current operational state.

    while remaining:

        candidates = []

        for vessel in remaining:

            score, factors = vessel_score(
                vessel,
                waves,
                resource_state,
                len(sequence),
                current_time
            )

            candidates.append(
                {
                    "vessel": vessel,
                    "score": score,
                    "factors": factors,
                    "weather": weather_status(vessel, waves),
                    "resource": resource_availability(
                        vessel["resource"],
                        resource_state
                    )
                }
            )

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        selected = candidates[0]

        sequence.append(selected)

        selected_vessel = selected["vessel"]

        # If vessel cannot currently operate,
        # leave it at the end as a blocked item.
        if selected["score"] < -500:
            current_time += 5
        else:
            current_time = max(
                current_time,
                selected_vessel["eta"]
            )

            current_time += selected_vessel["service_time"]

        remaining.remove(selected_vessel)

    return sequence


def calculate_total_waiting(sequence):
    current_time = 0
    total_waiting = 0

    for item in sequence:

        vessel = item["vessel"]

        start = max(
            current_time,
            vessel["eta"]
        )

        waiting = max(
            0,
            start - vessel["eta"]
        )

        total_waiting += waiting

        current_time = (
            start +
            vessel["service_time"]
        )

    return total_waiting


def calculate_total_service(sequence):
    return sum(
        item["vessel"]["service_time"]
        for item in sequence
        if item["score"] > -500
    )


def count_safe(sequence):
    return sum(
        1
        for item in sequence
        if item["weather"] == "SAFE"
        and item["score"] > -500
    )


def build_reason(item, waves):

    vessel = item["vessel"]

    if item["score"] < -900:
        if item["weather"] == "UNSAFE":
            return (
                f"{vessel['name']} is excluded from the active "
                f"sequence because the current wave height of "
                f"{waves:.1f} m exceeds its operational limit "
                f"of {vessel['weather_limit']:.1f} m."
            )

        return (
            f"{vessel['name']} cannot currently be processed "
            f"because its assigned resource is unavailable."
        )

    reasons = []

    if vessel["priority"] >= 4:
        reasons.append("high operational priority")

    if vessel["urgency"] >= 4:
        reasons.append("high urgency")

    if vessel["eta"] <= 20:
        reasons.append("early arrival")

    if item["weather"] == "RESTRICTED":
        reasons.append("limited weather margin")

    if item["resource"] == "LIMITED":
        reasons.append("resource constraints considered")

    if vessel["service_time"] <= 45:
        reasons.append("short service time")

    if vessel["cargo"] >= 2000:
        reasons.append("large cargo operation")

    if not reasons:
        reasons.append("balanced operational characteristics")

    return (
        f"{vessel['name']} is placed here because the system "
        f"identified {', '.join(reasons)} as the strongest "
        f"combination under the current conditions."
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚓ Maritime Flow")
    st.caption("Vessel Sequencing & Port Decision Support")

    st.divider()

    st.markdown("### Marine conditions")

    wave_height = st.slider(
        "Wave height (m)",
        0.0,
        8.0,
        2.5,
        0.1
    )

    wind_speed = st.slider(
        "Wind speed (kn)",
        0,
        50,
        16,
        1
    )

    visibility = st.slider(
        "Visibility (km)",
        0.5,
        20.0,
        10.0,
        0.5
    )

    st.divider()

    st.markdown("### Port resources")

    crane_a = st.selectbox(
        "Crane A",
        ["Available", "Limited", "Unavailable"]
    )

    crane_b = st.selectbox(
        "Crane B",
        ["Available", "Limited", "Unavailable"]
    )

    terminal_2 = st.selectbox(
        "Terminal 2",
        ["Available", "Limited", "Unavailable"]
    )

    ramp_1 = st.selectbox(
        "Ramp 1",
        ["Available", "Limited", "Unavailable"]
    )

    resource_state = {
        "Crane A": crane_a,
        "Crane B": crane_b,
        "Terminal 2": terminal_2,
        "Ramp 1": ramp_1
    }

    st.divider()

    st.markdown("### System status")

    st.success("OPERATIONAL")

    st.caption(
        "Decision support mode · Human operator remains "
        "the final decision-maker."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">MARITIME FLOW</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Intelligent vessel sequencing for safer and more efficient port operations'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="wave"></div>',
    unsafe_allow_html=True
)


# ============================================================
# LIVE PREVIEW
# ============================================================

preview = optimize_sequence(
    st.session_state.vessels,
    wave_height,
    resource_state
)

blocked = [
    item for item in preview
    if item["score"] < -500
]

restricted = [
    item for item in preview
    if item["weather"] == "RESTRICTED"
]

waiting = calculate_total_waiting(preview)


# ============================================================
# METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Vessels monitored</div>
            <div class="metric-value">
                {len(st.session_state.vessels)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Weather blocked</div>
            <div class="metric-value">
                {len(blocked)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Restricted</div>
            <div class="metric-value">
                {len(restricted)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Estimated waiting</div>
            <div class="metric-value">
                {waiting:.0f} min
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CONDITIONS
# ============================================================

st.markdown(
    '<div class="section-title">Current marine conditions</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:

    if wave_height <= 3:
        st.markdown(
            """
            <div class="success-box">
            <b>SEA STATE · NORMAL</b><br>
            Conditions are compatible with normal operations.
            </div>
            """,
            unsafe_allow_html=True
        )

    elif wave_height <= 5:
        st.markdown(
            """
            <div class="warning-box">
            <b>SEA STATE · CAUTION</b><br>
            Some vessels may require operational restrictions.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            """
            <div class="danger-box">
            <b>SEA STATE · SEVERE</b><br>
            Multiple vessels may become operationally unavailable.
            </div>
            """,
            unsafe_allow_html=True
        )


with c2:

    st.markdown(
        f"""
        <div class="info-box">
        <b>Wind</b><br>
        {wind_speed} kn
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        f"""
        <div class="info-box">
        <b>Visibility</b><br>
        {visibility:.1f} km
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# VESSEL MONITORING
# ============================================================

st.markdown(
    '<div class="section-title">Vessel monitoring</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Operational status of every vessel under the current conditions.'
    '</div>',
    unsafe_allow_html=True
)

for index, vessel in enumerate(st.session_state.vessels):

    weather = weather_status(
        vessel,
        wave_height
    )

    resource = resource_availability(
        vessel["resource"],
        resource_state
    )

    if weather == "SAFE":
        status = "🟢 SAFE"
    elif weather == "RESTRICTED":
        status = "🟡 RESTRICTED"
    else:
        status = "🔴 UNSAFE"

    if resource == "UNAVAILABLE":
        status = "🔴 RESOURCE BLOCKED"

    with st.container(border=True):

        a, b, c, d, e = st.columns(
            [2.4, 1.5, 1.2, 1.3, 1.5]
        )

        with a:
            st.markdown(
                f"**{index + 1}. {vessel['name']}**"
            )
            st.caption(
                f"{vessel['type']} · {vessel['resource']}"
            )

        with b:
            st.write(
                f"Draft: **{vessel['draft']:.1f} m**"
            )

        with c:
            st.write(
                f"ETA: **{vessel['eta']} min**"
            )

        with d:
            st.write(
                f"Priority: **{vessel['priority']}/5**"
            )

        with e:
            st.write(status)


# ============================================================
# OPTIMIZATION
# ============================================================

st.markdown(
    '<div class="section-title">Optimization engine</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'The system evaluates the feasible sequence using operational '
    'priority, urgency, arrival time, weather compatibility, '
    'resource availability, cargo volume and service efficiency.'
    '</div>',
    unsafe_allow_html=True
)

if st.button(
    "⚓ Generate optimal sequence",
    type="primary",
    use_container_width=True
):

    final_plan = optimize_sequence(
        st.session_state.vessels,
        wave_height,
        resource_state
    )

    st.session_state.plan = final_plan

    st.session_state.audit.append(
        {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "type": "SYSTEM OPTIMIZATION",
            "wave": wave_height,
            "sequence": [
                x["vessel"]["name"]
                for x in final_plan
            ]
        }
    )

    st.success(
        "Optimal operational sequence generated."
    )


# ============================================================
# OPTIMIZED SEQUENCE
# ============================================================

if st.session_state.plan is not None:

    plan = st.session_state.plan

    st.markdown(
        '<div class="section-title">Recommended sequence</div>',
        unsafe_allow_html=True
    )

    for position, item in enumerate(
        plan,
        start=1
    ):

        vessel = item["vessel"]

        if item["score"] < -500:

            box = "danger-box"

        elif item["weather"] == "RESTRICTED":

            box = "warning-box"

        else:

            box = "success-box"

        st.markdown(
            f"""
            <div class="vessel-card">

                <div style="display:flex;
                            justify-content:space-between;
                            align-items:center;">

                    <div>
                        <div class="sequence-number">
                            #{position}
                        </div>

                        <div class="vessel-name">
                            {vessel['name']}
                        </div>

                        <div class="vessel-meta">
                            {vessel['type']} ·
                            ETA {vessel['eta']} min ·
                            {vessel['resource']}
                        </div>
                    </div>

                    <div style="text-align:right;">
                        <div class="small-label">
                            Decision score
                        </div>
                        <div class="score">
                            {item['score']:.1f}
                        </div>
                    </div>

                </div>

                <br>

                <div class="{box}">
                    <b>System reasoning</b><br>
                    {build_reason(item, wave_height)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# WHY THIS SEQUENCE
# ============================================================

if st.session_state.plan is not None:

    plan = st.session_state.plan

    operational = [
        x for x in plan
        if x["score"] > -500
    ]

    blocked_vessels = [
        x for x in plan
        if x["score"] <= -500
    ]

    total_wait = calculate_total_waiting(
        plan
    )

    total_service = calculate_total_service(
        plan
    )

    safe_count = count_safe(
        plan
    )

    st.markdown(
        '<div class="section-title">Why this sequence?</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.metric(
            "Feasible vessels",
            len(operational)
        )

    with q2:
        st.metric(
            "Weather-safe",
            safe_count
        )

    with q3:
        st.metric(
            "Expected waiting",
            f"{total_wait:.0f} min"
        )

    with q4:
        st.metric(
            "Service time",
            f"{total_service:.0f} min"
        )

    st.markdown(
        """
        <div class="info-box">
        <b>Multi-factor decision model</b><br>
        The sequence is not determined by a single priority value.
        At every step, the system compares the remaining vessels
        against the current operational state and selects the strongest
        feasible candidate.
        </div>
        """,
        unsafe_allow_html=True
    )

    if blocked_vessels:

        names = ", ".join(
            x["vessel"]["name"]
            for x in blocked_vessels
        )

        st.markdown(
            f"""
            <div class="warning-box">
            <b>Operational constraints</b><br>
            {names} cannot currently enter the active sequence
            because of weather or resource constraints.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# OPERATOR OVERRIDE
# ============================================================

st.markdown(
    '<div class="section-title">Operator override</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'The algorithm supports the operator rather than replacing '
    'operational authority.'
    '</div>',
    unsafe_allow_html=True
)

vessel_names = [
    v["name"]
    for v in st.session_state.vessels
]

manual_order = st.multiselect(
    "Choose vessels for manual priority",
    vessel_names,
    default=st.session_state.manual_order
)

if st.button(
    "Apply operator decision",
    use_container_width=True
):

    if len(manual_order) == 0:

        st.warning(
            "Select at least one vessel."
        )

    else:

        st.session_state.manual_order = manual_order

        st.session_state.audit.append(
            {
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "type": "MANUAL OPERATOR OVERRIDE",
                "wave": wave_height,
                "sequence": manual_order
            }
        )

        st.success(
            "Operator decision recorded in the audit trail."
        )


# ============================================================
# AUDIT TRAIL
# ============================================================

st.markdown(
    '<div class="section-title">Decision audit trail</div>',
    unsafe_allow_html=True
)

if not st.session_state.audit:

    st.info(
        "No decisions have been recorded yet."
    )

else:

    for event in reversed(
        st.session_state.audit
    ):

        sequence = " → ".join(
            event["sequence"]
        )

        st.markdown(
            f"""
            <div class="info-box">
            <b>{event['type']}</b><br>
            {event['timestamp']}<br>
            Wave height: {event['wave']:.1f} m<br>
            Sequence: {sequence}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# REPORT
# ============================================================

if st.session_state.plan is not None:

    st.markdown(
        '<div class="section-title">Operational report</div>',
        unsafe_allow_html=True
    )

    plan = st.session_state.plan

    report_lines = [
        "MARITIME FLOW",
        "VESSEL SEQUENCING & PORT DECISION SUPPORT SYSTEM",
        "",
        "----------------------------------------",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Wave height: {wave_height:.1f} m",
        f"Wind speed: {wind_speed} kn",
        f"Visibility: {visibility:.1f} km",
        "----------------------------------------",
        "",
        "RECOMMENDED OPERATIONAL SEQUENCE",
        ""
    ]

    for i, item in enumerate(
        plan,
        start=1
    ):

        vessel = item["vessel"]

        report_lines.append(
            f"{i}. {vessel['name']}"
        )

        report_lines.append(
            f"   Type: {vessel['type']}"
        )

        report_lines.append(
            f"   ETA: {vessel['eta']} min"
        )

        report_lines.append(
            f"   Priority: {vessel['priority']}/5"
        )

        report_lines.append(
            f"   Resource: {vessel['resource']}"
        )

        report_lines.append(
            f"   Weather status: {item['weather']}"
        )

        report_lines.append(
            f"   Decision score: {item['score']:.2f}"
        )

        report_lines.append("")

    report_lines.extend(
        [
            "----------------------------------------",
            "DECISION PRINCIPLE",
            "",
            "The system evaluates vessel sequences using",
            "multiple operational factors rather than a",
            "single priority score.",
            "",
            "Final operational authority remains with",
            "the human port operator.",
            "----------------------------------------"
        ]
    )

    report = "\n".join(
        report_lines
    )

    st.download_button(
        "Download operational report",
        data=report,
        file_name="maritime_flow_operational_report.txt",
        mime="text/plain",
        use_container_width=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>
    <div style="
        text-align:center;
        color:#7897a5;
        font-size:12px;
        padding:28px 0 12px 0;
    ">
        MARITIME FLOW · Vessel Sequencing Decision Support System
        <br>
        Operational prototype · Human-in-the-loop decision support
    </div>
    """,
    unsafe_allow_html=True
)
