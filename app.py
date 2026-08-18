import streamlit as st
from datetime import datetime, timedelta
import math

# ============================================================
# MARITIME VESSEL SEQUENCING SYSTEM
# Streamlit application
# ============================================================

st.set_page_config(
    page_title="Maritime Flow",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STYLE
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
        margin-bottom: 28px;
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
        min-height: 110px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }

    .metric-label {
        color: #8eafbd;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        color: #f3fbff;
        font-size: 30px;
        font-weight: 750;
        margin-top: 6px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 750;
        margin-top: 30px;
        margin-bottom: 12px;
        color: #f4fbff;
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
# DATA
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
        "crane": "Heavy",
        "weather_limit": 6.0,
        "resource": "Crane A",
        "urgency": 5
    },
    {
        "name": "Northern Star",
        "type": "Bulk Carrier",
        "loa": 210,
        "draft": 10.4,
        "priority": 4,
        "eta": 10,
        "cargo": 3200,
        "crane": "Heavy",
        "weather_limit": 5.0,
        "resource": "Crane B",
        "urgency": 4
    },
    {
        "name": "Aurora",
        "type": "Tanker",
        "loa": 185,
        "draft": 8.7,
        "priority": 5,
        "eta": 55,
        "cargo": 2400,
        "crane": "Medium",
        "weather_limit": 4.5,
        "resource": "Terminal 2",
        "urgency": 5
    },
    {
        "name": "Ocean Pearl",
        "type": "Container",
        "loa": 160,
        "draft": 7.9,
        "priority": 3,
        "eta": 20,
        "cargo": 1100,
        "crane": "Medium",
        "weather_limit": 7.0,
        "resource": "Crane A",
        "urgency": 3
    },
    {
        "name": "Blue Meridian",
        "type": "Ro-Ro",
        "loa": 195,
        "draft": 8.1,
        "priority": 3,
        "eta": 5,
        "cargo": 850,
        "crane": "Light",
        "weather_limit": 8.0,
        "resource": "Ramp 1",
        "urgency": 3
    },
    {
        "name": "Sea Falcon",
        "type": "General Cargo",
        "loa": 145,
        "draft": 7.4,
        "priority": 2,
        "eta": 15,
        "cargo": 900,
        "crane": "Medium",
        "weather_limit": 6.5,
        "resource": "Crane B",
        "urgency": 2
    }
]

# ============================================================
# SESSION STATE
# ============================================================

if "vessels" not in st.session_state:
    st.session_state.vessels = [dict(v) for v in VESSELS]

if "last_plan" not in st.session_state:
    st.session_state.last_plan = None

if "manual_order" not in st.session_state:
    st.session_state.manual_order = []

if "audit" not in st.session_state:
    st.session_state.audit = []


# ============================================================
# FUNCTIONS
# ============================================================

def weather_status(vessel, wave_height):
    limit = vessel["weather_limit"]

    if wave_height > limit:
        return "UNSAFE", 0

    margin = limit - wave_height

    if margin < 1.0:
        return "RESTRICTED", 0.5

    return "SAFE", 1.0


def calculate_score(vessel, wave_height, resource_pressure):
    """
    The system evaluates vessels using several operational factors.

    Higher score = stronger candidate for earlier service.

    Factors:
    - priority
    - urgency
    - waiting time / ETA
    - weather compatibility
    - resource compatibility
    - cargo volume
    """

    status, weather_factor = weather_status(vessel, wave_height)

    if status == "UNSAFE":
        return -999, {
            "priority": 0,
            "urgency": 0,
            "waiting": 0,
            "weather": 0,
            "resource": 0,
            "cargo": 0
        }

    waiting_score = max(0, 30 - vessel["eta"]) / 6
    priority_score = vessel["priority"] * 2.4
    urgency_score = vessel["urgency"] * 2.0
    weather_score = weather_factor * 8

    if resource_pressure.get(vessel["resource"], 0) >= 2:
        resource_score = -5
    else:
        resource_score = 5

    cargo_score = min(vessel["cargo"] / 1000, 4)

    total = (
        priority_score
        + urgency_score
        + waiting_score
        + weather_score
        + resource_score
        + cargo_score
    )

    return total, {
        "priority": priority_score,
        "urgency": urgency_score,
        "waiting": waiting_score,
        "weather": weather_score,
        "resource": resource_score,
        "cargo": cargo_score
    }


def generate_plan(vessels, wave_height):
    resource_pressure = {}

    for vessel in vessels:
        resource = vessel["resource"]
        resource_pressure[resource] = resource_pressure.get(resource, 0) + 1

    results = []

    for vessel in vessels:
        score, factors = calculate_score(
            vessel,
            wave_height,
            resource_pressure
        )

        status, _ = weather_status(vessel, wave_height)

        results.append({
            "vessel": vessel,
            "score": score,
            "factors": factors,
            "status": status
        })

    results.sort(
        key=lambda x: (
            x["score"],
            x["vessel"]["priority"],
            -x["vessel"]["eta"]
        ),
        reverse=True
    )

    return results


def build_explanation(item, wave_height):
    vessel = item["vessel"]

    if item["status"] == "UNSAFE":
        return (
            f"{vessel['name']} is temporarily excluded because "
            f"the current wave height ({wave_height:.1f} m) exceeds "
            f"the vessel's operational limit ({vessel['weather_limit']:.1f} m)."
        )

    reasons = []

    if vessel["priority"] >= 4:
        reasons.append("high operational priority")

    if vessel["urgency"] >= 4:
        reasons.append("high urgency")

    if vessel["eta"] <= 20:
        reasons.append("short waiting time")

    if item["status"] == "RESTRICTED":
        reasons.append("limited weather margin")

    if vessel["cargo"] >= 2000:
        reasons.append("large cargo operation")

    if not reasons:
        reasons.append("balanced operational characteristics")

    return (
        f"{vessel['name']} is ranked here because of "
        + ", ".join(reasons)
        + "."
    )


def calculate_waiting_time(plan):
    current_time = 0
    total_waiting = 0

    for item in plan:
        eta = item["vessel"]["eta"]

        start = max(current_time, eta)
        waiting = max(0, start - eta)

        total_waiting += waiting

        current_time = start + 30

    return total_waiting


def create_audit(plan, wave_height):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "timestamp": timestamp,
        "wave_height": wave_height,
        "sequence": [x["vessel"]["name"] for x in plan]
    }


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚓ Maritime Flow")
    st.caption("Vessel Sequencing & Port Operations")

    st.divider()

    st.markdown("### Operational conditions")

    wave_height = st.slider(
        "Wave height (m)",
        min_value=0.0,
        max_value=8.0,
        value=2.5,
        step=0.1
    )

    wind_speed = st.slider(
        "Wind speed (kn)",
        min_value=0,
        max_value=50,
        value=16,
        step=1
    )

    visibility = st.slider(
        "Visibility (km)",
        min_value=0.5,
        max_value=20.0,
        value=10.0,
        step=0.5
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

    st.divider()

    st.caption("System mode")
    st.success("Operational")


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

st.markdown('<div class="wave"></div>', unsafe_allow_html=True)


# ============================================================
# TOP METRICS
# ============================================================

plan_preview = generate_plan(
    st.session_state.vessels,
    wave_height
)

unsafe_count = sum(
    1 for x in plan_preview
    if x["status"] == "UNSAFE"
)

restricted_count = sum(
    1 for x in plan_preview
    if x["status"] == "RESTRICTED"
)

total_wait = calculate_waiting_time(plan_preview)


m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Vessels</div>
            <div class="metric-value">{len(st.session_state.vessels)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Weather blocked</div>
            <div class="metric-value">{unsafe_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Restricted</div>
            <div class="metric-value">{restricted_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Estimated waiting</div>
            <div class="metric-value">{total_wait:.0f} min</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CURRENT CONDITIONS
# ============================================================

st.markdown(
    '<div class="section-title">Current marine conditions</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    if wave_height <= 3:
        st.markdown(
            '<div class="success-box">'
            '<b>SEA STATE: NORMAL</b><br>'
            'Current wave conditions are compatible with normal operations.'
            '</div>',
            unsafe_allow_html=True
        )
    elif wave_height <= 5:
        st.markdown(
            '<div class="warning-box">'
            '<b>SEA STATE: CAUTION</b><br>'
            'Some vessels may require operational restrictions.'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="warning-box">'
            '<b>SEA STATE: SEVERE</b><br>'
            'Several vessels may become unavailable for operations.'
            '</div>',
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
# VESSEL TABLE
# ============================================================

st.markdown(
    '<div class="section-title">Vessel queue</div>',
    unsafe_allow_html=True
)

for index, vessel in enumerate(st.session_state.vessels):

    status, _ = weather_status(vessel, wave_height)

    if status == "SAFE":
        status_text = "🟢 SAFE"
    elif status == "RESTRICTED":
        status_text = "🟡 RESTRICTED"
    else:
        status_text = "🔴 UNSAFE"

    with st.container(border=True):

        col1, col2, col3, col4, col5 = st.columns(
            [2.2, 1.5, 1.3, 1.3, 1.4]
        )

        with col1:
            st.markdown(
                f"**{index + 1}. {vessel['name']}**"
            )
            st.caption(vessel["type"])

        with col2:
            st.write(f"Draft: **{vessel['draft']:.1f} m**")

        with col3:
            st.write(f"ETA: **{vessel['eta']} min**")

        with col4:
            st.write(f"Priority: **{vessel['priority']}/5**")

        with col5:
            st.write(status_text)


# ============================================================
# PLAN GENERATION
# ============================================================

st.markdown(
    '<div class="section-title">Recommended sequence</div>',
    unsafe_allow_html=True
)

st.write(
    "The system evaluates the vessels as a sequence rather than "
    "using a single priority number. Weather, urgency, waiting time, "
    "resource pressure and operational suitability are considered together."
)

if st.button(
    "⚓ Generate optimal sequence",
    type="primary",
    use_container_width=True
):

    plan = generate_plan(
        st.session_state.vessels,
        wave_height
    )

    st.session_state.last_plan = plan

    st.session_state.audit.append(
        create_audit(plan, wave_height)
    )

    st.success("Operational sequence generated successfully.")


# ============================================================
# SHOW PLAN
# ============================================================

if st.session_state.last_plan is not None:

    plan = st.session_state.last_plan

    for position, item in enumerate(plan, start=1):

        vessel = item["vessel"]

        if item["status"] == "UNSAFE":
            border_class = "warning-box"
        elif item["status"] == "RESTRICTED":
            border_class = "warning-box"
        else:
            border_class = "success-box"

        st.markdown(
            f"""
            <div class="vessel-card">
                <div class="vessel-name">
                    #{position} — {vessel['name']}
                </div>
                <div class="vessel-meta">
                    {vessel['type']} · ETA {vessel['eta']} min ·
                    Priority {vessel['priority']}/5 ·
                    Resource: {vessel['resource']}
                </div>
                <br>
                <div class="{border_class}">
                    <b>System reasoning</b><br>
                    {build_explanation(item, wave_height)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DECISION SUPPORT
# ============================================================

if st.session_state.last_plan is not None:

    st.markdown(
        '<div class="section-title">Decision support</div>',
        unsafe_allow_html=True
    )

    plan = st.session_state.last_plan

    available = [
        x for x in plan
        if x["status"] != "UNSAFE"
    ]

    blocked = [
        x for x in plan
        if x["status"] == "UNSAFE"
    ]

    if blocked:
        names = ", ".join(
            x["vessel"]["name"]
            for x in blocked
        )

        st.markdown(
            f"""
            <div class="warning-box">
            <b>Weather restriction detected</b><br>
            {names} cannot currently be placed into the active
            operational sequence because the wave height exceeds
            their operating limit.
            </div>
            """,
            unsafe_allow_html=True
        )

    if available:

        best = available[0]["vessel"]

        st.markdown(
            f"""
            <div class="success-box">
            <b>Recommended next vessel</b><br>
            {best['name']} should be considered first among the
            currently feasible vessels.
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# MANUAL OVERRIDE
# ============================================================

st.markdown(
    '<div class="section-title">Operator override</div>',
    unsafe_allow_html=True
)

st.write(
    "The system provides a recommendation, but the final decision "
    "remains with the port operator."
)

vessel_names = [
    v["name"] for v in st.session_state.vessels
]

manual_order = st.multiselect(
    "Select vessels for manual priority order",
    vessel_names,
    default=st.session_state.manual_order
)

if st.button(
    "Apply operator sequence",
    use_container_width=True
):

    if not manual_order:

        st.warning(
            "Select at least one vessel before applying a manual sequence."
        )

    else:

        st.session_state.manual_order = manual_order

        st.session_state.audit.append(
            {
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "wave_height": wave_height,
                "sequence": manual_order,
                "type": "MANUAL OVERRIDE"
            }
        )

        st.success(
            "Manual operator sequence recorded."
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

    for event in reversed(st.session_state.audit):

        event_type = event.get(
            "type",
            "SYSTEM RECOMMENDATION"
        )

        sequence = " → ".join(
            event["sequence"]
        )

        st.markdown(
            f"""
            <div class="info-box">
            <b>{event_type}</b><br>
            {event['timestamp']}<br>
            Wave height: {event['wave_height']:.1f} m<br>
            Sequence: {sequence}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# EXPORT
# ============================================================

st.markdown(
    '<div class="section-title">Export decision</div>',
    unsafe_allow_html=True
)

if st.session_state.last_plan is not None:

    lines = [
        "MARITIME FLOW — OPERATIONAL SEQUENCE",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Wave height: {wave_height:.1f} m",
        f"Wind speed: {wind_speed} kn",
        f"Visibility: {visibility:.1f} km",
        "",
        "RECOMMENDED SEQUENCE:",
    ]

    for i, item in enumerate(
        st.session_state.last_plan,
        start=1
    ):

        vessel = item["vessel"]

        lines.append(
            f"{i}. {vessel['name']} | "
            f"{vessel['type']} | "
            f"Status: {item['status']} | "
            f"Score: {item['score']:.2f}"
        )

    lines.extend(
        [
            "",
            "This recommendation is decision support.",
            "Final operational authority remains with the port operator."
        ]
    )

    report = "\n".join(lines)

    st.download_button(
        label="Download operational report",
        data=report,
        file_name="maritime_flow_report.txt",
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
        padding:25px 0 10px 0;
    ">
        MARITIME FLOW · Vessel Sequencing Decision Support System
    </div>
    """,
    unsafe_allow_html=True
)
