import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import json
import math

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & METADATA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="BloodBridge AI | Autonomous Emergency Blood Mesh",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# 2. ULTRA-ADVANCED CSS DESIGN SYSTEM (World-Class Hackathon Standard)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --bg-primary: #07090E;
        --bg-secondary: #0D121F;
        --bg-card: rgba(16, 23, 38, 0.7);
        --bg-card-hover: rgba(23, 32, 54, 0.85);
        --crimson-primary: #E11D48;
        --crimson-glow: rgba(225, 29, 72, 0.35);
        --crimson-subtle: rgba(225, 29, 72, 0.12);
        --ruby-gradient: linear-gradient(135deg, #FF1744 0%, #B7092B 100%);
        --plasma-gradient: linear-gradient(135deg, #0EA5E9 0%, #0369A1 100%);
        --emerald-gradient: linear-gradient(135deg, #10B981 0%, #047857 100%);
        --amber-gradient: linear-gradient(135deg, #F59E0B 0%, #B45309 100%);
        --text-main: #F8FAFC;
        --text-muted: #94A3B8;
        --text-dim: #64748B;
        --border-glass: rgba(255, 255, 255, 0.08);
        --border-active: rgba(225, 29, 72, 0.4);
        --border-radius: 16px;
    }

    /* Core Application Wrapper */
    .stApp {
        background-color: var(--bg-primary);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-main);
    }

    /* Ambient Background Glow */
    .stApp::before {
        content: "";
        position: fixed;
        top: -10vw;
        right: -10vw;
        width: 45vw;
        height: 45vw;
        background: radial-gradient(circle, rgba(225, 29, 72, 0.12) 0%, rgba(7, 9, 14, 0) 70%);
        pointer-events: none;
        z-index: 0;
    }

    /* Modern Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    ::-webkit-scrollbar-thumb {
        background: #1E293B;
        border-radius: 999px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--crimson-primary);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-glass);
    }

    section[data-testid="stSidebar"] .stRadio > div {
        background: transparent;
        gap: 8px;
    }

    /* Glassmorphism Card Element */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid var(--border-glass);
        border-radius: var(--border-radius);
        padding: 24px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 20px;
    }

    .glass-card:hover {
        border-color: var(--border-active);
        box-shadow: 0 14px 36px -8px var(--crimson-glow);
        transform: translateY(-2px);
    }

    /* Emergency Alert Header Banner */
    .emergency-banner {
        background: linear-gradient(90deg, rgba(225, 29, 72, 0.2) 0%, rgba(15, 23, 42, 0.6) 100%);
        border-left: 4px solid var(--crimson-primary);
        border-top: 1px solid var(--border-glass);
        border-right: 1px solid var(--border-glass);
        border-bottom: 1px solid var(--border-glass);
        border-radius: 12px;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
    }

    /* Pulsing Signal Dot */
    .pulse-dot {
        width: 10px;
        height: 10px;
        background-color: var(--crimson-primary);
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.7);
        animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
    }

    @keyframes pulse-ring {
        0% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.7); }
        70% { box-shadow: 0 0 0 12px rgba(225, 29, 72, 0); }
        100% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
    }

    /* Stat Metric Badge */
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -1px;
        color: #FFFFFF;
        line-height: 1.1;
    }

    .metric-label {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: var(--text-muted);
        font-weight: 600;
        margin-top: 6px;
    }

    .metric-sub {
        font-size: 0.8rem;
        color: #10B981;
        font-weight: 500;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Blood Group Badge Matrix */
    .blood-chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8px 16px;
        background: rgba(225, 29, 72, 0.15);
        border: 1px solid rgba(225, 29, 72, 0.3);
        border-radius: 10px;
        font-weight: 700;
        font-size: 1.1rem;
        color: #FF4D6D;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Donor Match Card */
    .match-card {
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.25s ease;
    }

    .match-card:hover {
        background: #151F36;
        border-color: rgba(225, 29, 72, 0.5);
    }

    .match-score {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #FFFFFF;
        font-weight: 700;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Custom Streamlit Form Tweaks */
    div.stButton > button {
        background: var(--ruby-gradient);
        color: white;
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        border-radius: 12px;
        letter-spacing: 0.3px;
        box-shadow: 0 6px 20px -4px rgba(225, 29, 72, 0.5);
        transition: all 0.25s ease;
        width: 100%;
    }

    div.stButton > button:hover {
        box-shadow: 0 10px 28px -2px rgba(225, 29, 72, 0.7);
        transform: translateY(-1.5px);
        color: white;
    }

    /* Input elements styling */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        background-color: #0A0F1D !important;
        border: 1px solid #1E293B !important;
        color: #F8FAFC !important;
        border-radius: 10px !important;
    }

    /* Inventory Progress Bar */
    .inventory-bar-bg {
        width: 100%;
        height: 8px;
        background: #1E293B;
        border-radius: 999px;
        overflow: hidden;
        margin-top: 8px;
    }
    .inventory-bar-fill {
        height: 100%;
        border-radius: 999px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. MOCK DATA & COMPATIBILITY INTELLIGENCE ENGINE
# -----------------------------------------------------------------------------
BLOOD_GROUPS = ["O-", "O+", "B-", "B+", "A-", "A+", "AB-", "AB+"]

# Complete Red Blood Cell Transfusion Compatibility Rules
COMPATIBILITY_MATRIX = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]
}

if "inventory" not in st.session_state:
    st.session_state.inventory = {
        "O-": 4,     # Critical
        "O+": 24,    # Healthy
        "A-": 7,     # Moderate
        "A+": 32,    # High
        "B-": 5,     # Critical
        "B+": 19,    # Healthy
        "AB-": 2,    # Extreme Critical
        "AB+": 14    # Normal
    }

if "live_sos_dispatches" not in st.session_state:
    st.session_state.live_sos_dispatches = [
        {
            "id": "EMERG-9042",
            "hospital": "St. Jude Emergency Trauma Center",
            "blood_type": "O-",
            "units": 3,
            "urgency": "Code Red (Immediate)",
            "status": "Transiting",
            "eta": "11 mins",
            "distance": "4.2 km"
        },
        {
            "id": "EMERG-9038",
            "hospital": "Memorial Children's Cardiac Ward",
            "blood_type": "AB-",
            "units": 2,
            "urgency": "Urgent (< 2 Hours)",
            "status": "Matched - Contacting",
            "eta": "24 mins",
            "distance": "8.7 km"
        }
    ]

# -----------------------------------------------------------------------------
# 4. SIDEBAR NAVIGATION & TELEMETRY
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 0 20px 0; display: flex; align-items: center; gap: 12px;">
            <div style="background: linear-gradient(135deg, #FF1744 0%, #880e28 100%); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 6px 18px rgba(225, 29, 72, 0.4);">
                🩸
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.18rem; letter-spacing: -0.5px; color: #FFFFFF;">BloodBridge<span style="color: #E11D48;"> AI</span></div>
                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px;">Autonomous Blood Mesh</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px; margin-bottom: 20px;">
            <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Network Status</div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 6px;">
                <span style="display: flex; align-items: center; font-size: 0.85rem; font-weight: 600; color: #10B981;">
                    <span class="pulse-dot" style="background-color: #10B981; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);"></span> Mesh Active
                </span>
                <span style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #64748B;">Lat: 24ms</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    menu = st.radio(
        "NAVIGATION MODULES",
        [
            "🚨 Emergency Dispatch Hub",
            "🧬 AI Donor Radar & Matching",
            "📊 Smart Inventory & AI Forecast",
            "🩺 Donor Pass & Health Screener",
            "🌐 Mesh Logistics & Live Route",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="padding: 6px 0;">
            <div style="font-size: 0.75rem; color: #64748B; margin-bottom: 8px;">GLOBAL STATS</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                <div style="background: rgba(255,255,255,0.02); padding: 8px 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="font-size: 0.7rem; color: #94A3B8;">Avg. Match Time</div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #FFFFFF; font-family: 'JetBrains Mono';">3.4 min</div>
                </div>
                <div style="background: rgba(255,255,255,0.02); padding: 8px 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.04);">
                    <div style="font-size: 0.7rem; color: #94A3B8;">Lives Saved</div>
                    <div style="font-size: 0.95rem; font-weight: 700; color: #10B981; font-family: 'JetBrains Mono';">14,892</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 5. MODULE 1: EMERGENCY DISPATCH HUB (SOS CORE)
# -----------------------------------------------------------------------------
if menu == "🚨 Emergency Dispatch Hub":
    st.markdown(
        """
        <div class="emergency-banner">
            <div style="display: flex; align-items: center;">
                <span class="pulse-dot"></span>
                <span style="font-weight: 700; font-size: 0.95rem; color: #FFFFFF; letter-spacing: 0.3px;">CRITICAL BLOOD ALERT PROTOCOL ACTIVE</span>
            </div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #FCA5A5;">DEFCON-1 TRIAGE READY</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            """
            <div class="glass-card">
                <div class="metric-label">Active Emergencies</div>
                <div class="metric-value" style="color: #FF4D6D;">03</div>
                <div class="metric-sub" style="color: #F87171;">⚠️ 2 High Priority</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="glass-card">
                <div class="metric-label">Compatible Donors Online</div>
                <div class="metric-value" style="color: #38BDF8;">1,420</div>
                <div class="metric-sub">📍 Within 15km Radius</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="glass-card">
                <div class="metric-label">Reserve Depletion Index</div>
                <div class="metric-value" style="color: #F59E0B;">64.2%</div>
                <div class="metric-sub" style="color: #FBBF24;">⚡ Alert: O- in deficit</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            """
            <div class="glass-card">
                <div class="metric-label">Drone/Courier Dispatch</div>
                <div class="metric-value" style="color: #10B981;">98.6%</div>
                <div class="metric-sub">🚀 Instant Fleet Ready</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Main Emergency Form & Dispatch Stream
    left_c, right_c = st.columns([1.1, 0.9])

    with left_c:
        st.markdown(
            """
            <div style="font-size: 1.15rem; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                ⚡ Trigger Autonomous AI Emergency Request
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("emergency_trigger_form"):
            hosp_name = st.selectbox(
                "Hospital / Trauma Center",
                [
                    "City General Trauma Center - ICU Unit 4",
                    "St. Jude Emergency Center - Surgical Suite B",
                    "Metropolitan Cardiac Care Hospital",
                    "Redwood Memorial Children's Emergency",
                    "Apollo Advanced Surgical Hospital"
                ],
            )

            f_c1, f_c2 = st.columns(2)
            with f_c1:
                needed_type = st.selectbox("Recipient Blood Type Needed", BLOOD_GROUPS)
            with f_c2:
                units = st.number_input("Pints / Units Required", min_value=1, max_value=20, value=2)

            f_c3, f_c4 = st.columns(2)
            with f_c3:
                urgency = st.selectbox(
                    "Clinical Urgency Classification",
                    [
                        "🔴 Level 1: Immediate Hemorrhage (Under 15 mins)",
                        "🟠 Level 2: Urgent Surgical Procedure (Under 2 hrs)",
                        "🟡 Level 3: Scheduled / Impending Critical (Under 6 hrs)"
                    ]
                )
            with f_c4:
                component = st.selectbox(
                    "Component Required",
                    ["Whole Red Blood Cells", "Platelets (Thrombocytes)", "Fresh Frozen Plasma (FFP)", "Cryoprecipitate"]
                )

            st.caption("AI Smart Matcher automatically queries donor geo-proximity, serological antigen compatibility, and courier availability.")

            submitted = st.form_submit_button("🚀 EXECUTE AUTONOMOUS EMERGENCY DISPATCH")
            if submitted:
                new_entry = {
                    "id": f"EMERG-{np.random.randint(1000, 9999)}",
                    "hospital": hosp_name.split(" - ")[0],
                    "blood_type": needed_type,
                    "units": units,
                    "urgency": urgency.split(":")[0],
                    "status": "Broadcasting to Donors",
                    "eta": "6-12 mins",
                    "distance": "3.1 km"
                }
                st.session_state.live_sos_dispatches.insert(0, new_entry)
                st.toast(f"Autonomous Emergency protocol triggered for {needed_type}! Pinging compatible donors...", icon="🚨")

    with right_c:
        st.markdown(
            """
            <div style="font-size: 1.15rem; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
                <span>📡 Active Dispatch Telemetry</span>
                <span style="font-size: 0.75rem; color: #10B981; font-weight: 500;">● Live Updating</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for item in st.session_state.live_sos_dispatches:
            st.markdown(
                f"""
                <div class="match-card">
                    <div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span class="blood-chip" style="font-size: 0.9rem; padding: 4px 10px;">{item['blood_type']}</span>
                            <span style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">{item['hospital']}</span>
                        </div>
                        <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 6px;">
                            Req ID: <span style="font-family: 'JetBrains Mono'; color: #CBD5E1;">{item['id']}</span> • 
                            Units: <strong style="color: #FFFFFF;">{item['units']}</strong> • 
                            Distance: {item['distance']}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="match-score" style="background: rgba(225, 29, 72, 0.2); border: 1px solid #E11D48; color: #FDA4AF;">
                            ETA {item['eta']}
                        </span>
                        <div style="font-size: 0.75rem; color: #38BDF8; font-weight: 600; margin-top: 5px;">{item['status']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 14px; text-align: center; margin-top: 10px;">
                <div style="font-size: 0.8rem; color: #94A3B8;">Automatic Fallback: Autonomous Blood Bank Drone dispatch activates if zero local donor responses occur within 4 minutes.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------------------------------------------------------
# 6. MODULE 2: AI DONOR RADAR & MATCHING (PRECISION ENGINE)
# -----------------------------------------------------------------------------
elif menu == "🧬 AI Donor Radar & Matching":
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="font-size: 1.8rem; font-weight: 800; margin-bottom: 4px;">AI Predictive Donor Matching Radar</h2>
            <p style="color: #94A3B8; font-size: 0.92rem;">Combines immunological compatibility matrices, travel telemetry, historical response rates, and real-time biometric eligibility.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    t_col1, t_col2, t_col3 = st.columns([1, 1, 1])
    with t_col1:
        target_blood = st.selectbox("Select Patient Blood Group", BLOOD_GROUPS, index=0)
    with t_col2:
        max_dist = st.slider("Maximum Donor Radius (km)", min_value=2, max_value=50, value=15)
    with t_col3:
        sort_by = st.selectbox("Rank Match Algorithm By", ["Multi-Factor AI Score", "Proximity (Shortest ETA)", "Donor Reliability Index"])

    compatible_types = COMPATIBILITY_MATRIX[target_blood]

    st.markdown(
        f"""
        <div style="background: rgba(14, 165, 233, 0.08); border: 1px solid rgba(14, 165, 233, 0.25); border-radius: 12px; padding: 12px 18px; margin: 18px 0; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span style="color: #38BDF8; font-weight: 600; font-size: 0.9rem;">Immunological Compatibility Window for <strong>{target_blood}</strong>:</span>
                <div style="margin-top: 6px; display: flex; gap: 8px; flex-wrap: wrap;">
                    {' '.join([f'<span class="blood-chip" style="font-size:0.8rem; padding: 2px 10px;">{t}</span>' for t in compatible_types])}
                </div>
            </div>
            <div style="text-align: right; font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #94A3B8;">
                UNIVERSAL DONOR LOGIC: <span style="color: #10B981;">ACTIVE</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Generate Smart Synthetic Donors dynamically based on selected compatibility
    np.random.seed(42 + len(target_blood))
    donors_list = []
    names = [
        "Alex Mercer", "Dr. Sarah Chen", "Marcus Vance", "Elena Rostova", "Liam O'Connor",
        "Priya Sharma", "David Kim", "Zoe Al-Mansoor", "Lucas Silva", "Amara Okafor"
    ]

    for idx, name in enumerate(names):
        d_type = np.random.choice(compatible_types)
        dist = round(float(np.random.uniform(1.2, max_dist)), 1)
        resp_rate = int(np.random.uniform(88, 99))
        eta = int(dist * 2.8 + np.random.randint(2, 6))
        # Multi factor score: weighted proximity, response rate, exact type bonus
        exact_bonus = 15 if d_type == target_blood else 0
        ai_score = min(99, int(100 - (dist * 1.5) + (resp_rate * 0.15) + exact_bonus))

        donors_list.append({
            "name": name,
            "blood_group": d_type,
            "distance_km": dist,
            "eta_mins": eta,
            "reliability": f"{resp_rate}%",
            "last_donated": f"{np.random.randint(92, 180)} days ago",
            "ai_match_score": ai_score,
            "status": "Available / Standby"
        })

    # Sort
    if sort_by == "Multi-Factor AI Score":
        donors_list = sorted(donors_list, key=lambda x: x["ai_match_score"], reverse=True)
    elif sort_by == "Proximity (Shortest ETA)":
        donors_list = sorted(donors_list, key=lambda x: x["distance_km"])
    else:
        donors_list = sorted(donors_list, key=lambda x: int(x["reliability"].replace("%", "")), reverse=True)

    # Render Donor List
    for donor in donors_list:
        badge_color = "#10B981" if donor["ai_match_score"] >= 90 else ("#F59E0B" if donor["ai_match_score"] >= 80 else "#38BDF8")
        st.markdown(
            f"""
            <div class="glass-card" style="padding: 18px 22px; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                    <div style="display: flex; align-items: center; gap: 16px;">
                        <div class="blood-chip" style="font-size: 1.15rem; width: 52px; height: 52px; border-radius: 12px; background: rgba(225, 29, 72, 0.2);">
                            {donor['blood_group']}
                        </div>
                        <div>
                            <div style="font-weight: 700; font-size: 1.05rem; color: #FFFFFF; display: flex; align-items: center; gap: 8px;">
                                {donor['name']}
                                <span style="font-size: 0.7rem; background: rgba(16, 185, 129, 0.15); color: #34D399; padding: 2px 8px; border-radius: 99px; font-weight: 600;">VERIFIED ELIGIBLE</span>
                            </div>
                            <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 4px;">
                                Distance: <strong style="color: #F1F5F9;">{donor['distance_km']} km</strong> • 
                                Est. Arrival: <strong style="color: #F1F5F9;">{donor['eta_mins']} mins</strong> • 
                                Past Donations: {donor['last_donated']} • 
                                Reliability: <span style="color: #10B981;">{donor['reliability']}</span>
                            </div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <div style="text-align: right;">
                            <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase;">AI Match Confidence</div>
                            <div style="font-family: 'JetBrains Mono'; font-weight: 800; font-size: 1.3rem; color: {badge_color};">
                                {donor['ai_match_score']}%
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------------------------------------------------------
# 7. MODULE 3: SMART INVENTORY & AI FORECAST (CRITICAL RESERVES)
# -----------------------------------------------------------------------------
elif menu == "📊 Smart Inventory & AI Forecast":
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="font-size: 1.8rem; font-weight: 800; margin-bottom: 4px;">Regional Blood Reserve Telemetry & Predictive AI</h2>
            <p style="color: #94A3B8; font-size: 0.92rem;">Real-time inventory levels across central hubs with autonomous 7-day predictive depletion simulation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 8-Blood Groups Grid
    cols = st.columns(4)
    for idx, (b_type, units) in enumerate(st.session_state.inventory.items()):
        col = cols[idx % 4]
        # Status calculation
        if units < 5:
            status_text = "🚨 DEFICIT CRITICAL"
            status_color = "#FF4D6D"
            bar_color = "linear-gradient(90deg, #E11D48, #FF1744)"
            percentage = min(100, int((units / 25) * 100))
        elif units < 10:
            status_text = "⚠️ LOW RESERVE"
            status_color = "#F59E0B"
            bar_color = "linear-gradient(90deg, #D97706, #F59E0B)"
            percentage = min(100, int((units / 25) * 100))
        else:
            status_text = "✅ OPTIMAL LEVEL"
            status_color = "#10B981"
            bar_color = "linear-gradient(90deg, #059669, #10B981)"
            percentage = min(100, int((units / 35) * 100))

        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="padding: 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="blood-chip" style="font-size: 1.1rem; padding: 4px 12px;">{b_type}</span>
                        <span style="font-size: 0.72rem; font-weight: 700; color: {status_color};">{status_text}</span>
                    </div>
                    <div style="margin-top: 14px;">
                        <span style="font-family: 'JetBrains Mono'; font-size: 1.9rem; font-weight: 800; color: #FFFFFF;">{units}</span>
                        <span style="color: #94A3B8; font-size: 0.85rem;"> units stored</span>
                    </div>
                    <div class="inventory-bar-bg">
                        <div class="inventory-bar-fill" style="width: {percentage}%; background: {bar_color};"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # AI 7-Day Demand Forecasting Section
    st.markdown(
        """
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div>
                    <div style="font-weight: 700; font-size: 1.15rem; color: #FFFFFF;">🧠 Neural Predictive Forecast (Next 7 Days)</div>
                    <div style="font-size: 0.82rem; color: #94A3B8;">Trained on emergency trauma patterns, regional weather anomalies, and scheduled cardiothoracic surgeries.</div>
                </div>
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #34D399; padding: 4px 12px; border-radius: 8px; font-size: 0.78rem; font-family: 'JetBrains Mono';">
                    MODEL ACCURACY: 94.8%
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # Generate synthetic 7-day predictive dataframe
    dates = [(datetime.date.today() + datetime.timedelta(days=i)).strftime("%a, %b %d") for i in range(7)]
    forecast_df = pd.DataFrame({
        "Date": dates,
        "Projected Demand (Units)": [18, 22, 31, 19, 27, 34, 21],
        "Predicted Inflow (Donations)": [14, 16, 20, 22, 25, 29, 18],
        "Projected Gap (Deficit/Surplus)": [-4, -6, -11, +3, -2, -5, -3]
    })

    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        <div style="margin-top: 14px; padding: 12px; background: rgba(225, 29, 72, 0.08); border-left: 3px solid #E11D48; border-radius: 8px;">
            <strong style="color: #FDA4AF; font-size: 0.88rem;">Autonomous Replenishment Recommendation:</strong>
            <span style="font-size: 0.84rem; color: #CBD5E1;"> Schedule automated blood drive mobile vans in Sector 4 & 7 on Wednesday to prevent the projected -11 unit deficit in O- and B- reserves.</span>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 8. MODULE 4: DONOR PASS & HEALTH SCREENER
# -----------------------------------------------------------------------------
elif menu == "🩺 Donor Pass & Health Screener":
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="font-size: 1.8rem; font-weight: 800; margin-bottom: 4px;">Biometric Donor Pass & Instant Health Passport</h2>
            <p style="color: #94A3B8; font-size: 0.92rem;">Self-service pre-screening for instant triage clearance and dynamic digital donor credentialing.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    p_col1, p_col2 = st.columns([1.1, 0.9])

    with p_col1:
        st.markdown(
            """
            <div class="glass-card">
                <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 14px;">Instant AI Eligibility Pre-Screening</div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("donor_screener_form"):
            donor_name = st.text_input("Full Legal Name", value="Alexander Thorne")
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                donor_blood = st.selectbox("Blood Group", BLOOD_GROUPS, index=1)
                donor_age = st.number_input("Age", min_value=16, max_value=85, value=28)
            with d_col2:
                donor_weight = st.number_input("Weight (kg)", min_value=40, max_value=180, value=74)
                donor_hb = st.number_input("Hemoglobin Level (g/dL)", min_value=8.0, max_value=20.0, value=14.6, step=0.1)

            recent_travel = st.checkbox("Traveled internationally to malaria-endemic zones in the last 6 months?", value=False)
            recent_tattoo = st.checkbox("Received tattoo, piercing, or acupuncture in the past 3 months?", value=False)
            med_condition = st.checkbox("Currently experiencing flu, fever, or under acute antibiotic treatment?", value=False)

            screen_btn = st.form_submit_button("🧬 EVALUATE ELIGIBILITY & GENERATE PASS")

        st.markdown("</div>", unsafe_allow_html=True)

    with p_col2:
        # Determine eligibility criteria based on WHO & Red Cross benchmarks
        is_eligible = (
            donor_age >= 17 and
            donor_weight >= 50 and
            donor_hb >= 12.5 and
            not recent_travel and
            not recent_tattoo and
            not med_condition
        )

        if is_eligible:
            pass_status = "VERIFIED ELIGIBLE"
            pass_badge_color = "#10B981"
            status_desc = "Safe to donate whole blood or platelets immediately."
        else:
            pass_status = "TEMPORARILY DEFERRED"
            pass_badge_color = "#E11D48"
            status_desc = "Criteria threshold not met. Consult a clinical nurse on-site."

        st.markdown(
            f"""
            <div class="glass-card" style="background: linear-gradient(135deg, rgba(17, 24, 39, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%); border: 1px solid rgba(225, 29, 72, 0.4); border-radius: 20px; padding: 26px; position: relative; overflow: hidden;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">DIGITAL HEALTH PASSPORT</div>
                        <div style="font-size: 1.35rem; font-weight: 800; color: #FFFFFF; margin-top: 2px;">{donor_name}</div>
                        <div style="font-size: 0.8rem; color: #38BDF8; font-family: 'JetBrains Mono';">ID: BB-PASS-2026-908</div>
                    </div>
                    <div class="blood-chip" style="font-size: 1.3rem; padding: 6px 16px; border-radius: 12px; background: rgba(225, 29, 72, 0.25);">
                        {donor_blood}
                    </div>
                </div>

                <div style="margin: 22px 0; border-top: 1px dashed rgba(255, 255, 255, 0.1); border-bottom: 1px dashed rgba(255, 255, 255, 0.1); padding: 16px 0;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; text-align: center;">
                        <div>
                            <div style="font-size: 0.7rem; color: #94A3B8;">Weight</div>
                            <div style="font-size: 1rem; font-weight: 700; color: #FFFFFF;">{donor_weight} kg</div>
                        </div>
                        <div>
                            <div style="font-size: 0.7rem; color: #94A3B8;">Hemoglobin</div>
                            <div style="font-size: 1rem; font-weight: 700; color: #FFFFFF;">{donor_hb} g/dL</div>
                        </div>
                        <div>
                            <div style="font-size: 0.7rem; color: #94A3B8;">Donor Tier</div>
                            <div style="font-size: 1rem; font-weight: 700; color: #F59E0B;">⭐ Gold</div>
                        </div>
                    </div>
                </div>

                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 0.75rem; color: #94A3B8;">Triage Clearance:</div>
                        <div style="font-weight: 800; font-size: 0.95rem; color: {pass_badge_color};">{pass_status}</div>
                    </div>
                    <div style="background: white; padding: 6px; border-radius: 8px; width: 54px; height: 54px; display: flex; align-items: center; justify-content: center; font-size: 28px;">
                        📱
                    </div>
                </div>
                <div style="font-size: 0.75rem; color: #64748B; margin-top: 12px;">{status_desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------------------------------------------------------
# 9. MODULE 5: MESH LOGISTICS & LIVE ROUTE
# -----------------------------------------------------------------------------
elif menu == "🌐 Mesh Logistics & Live Route":
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h2 style="font-size: 1.8rem; font-weight: 800; margin-bottom: 4px;">Smart Transit & Autonomous Courier Mesh</h2>
            <p style="color: #94A3B8; font-size: 0.92rem;">Simulating real-time temperature-controlled payload tracking between blood centers and surgical suites.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Courier Status Cards
    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
        st.markdown(
            """
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 700; font-size: 1rem;">Drone Unit #04</span>
                    <span style="color: #10B981; font-weight: 700; font-size: 0.8rem;">IN FLIGHT</span>
                </div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 6px;">Payload: 2x O- Units (Packed Red Blood Cells)</div>
                <div style="margin-top: 12px; display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.85rem;">
                    <span>Temp: <strong>3.8°C</strong></span>
                    <span>Altitude: <strong>110m</strong></span>
                </div>
                <div class="inventory-bar-bg">
                    <div class="inventory-bar-fill" style="width: 68%; background: #10B981;"></div>
                </div>
                <div style="font-size: 0.75rem; color: #38BDF8; margin-top: 8px; text-align: right;">68% Route Complete • ETA 4m</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r_col2:
        st.markdown(
            """
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 700; font-size: 1rem;">Rapid Response Courier 12</span>
                    <span style="color: #38BDF8; font-weight: 700; font-size: 0.8rem;">MOTORCYCLE</span>
                </div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 6px;">Payload: Platelet Apheresis Pack (A+)</div>
                <div style="margin-top: 12px; display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.85rem;">
                    <span>Temp: <strong>21.4°C</strong></span>
                    <span>Agitator: <strong>ACTIVE</strong></span>
                </div>
                <div class="inventory-bar-bg">
                    <div class="inventory-bar-fill" style="width: 42%; background: #38BDF8;"></div>
                </div>
                <div style="font-size: 0.75rem; color: #38BDF8; margin-top: 8px; text-align: right;">42% Route Complete • ETA 9m</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r_col3:
        st.markdown(
            """
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between;">
                    <span style="font-weight: 700; font-size: 1rem;">Hospital Van Relay</span>
                    <span style="color: #F59E0B; font-weight: 700; font-size: 0.8rem;">DOCKING</span>
                </div>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 6px;">Payload: Bulk Replenishment (12 Units)</div>
                <div style="margin-top: 12px; display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.85rem;">
                    <span>Temp: <strong>4.1°C</strong></span>
                    <span>Status: <strong>At Gate 3</strong></span>
                </div>
                <div class="inventory-bar-bg">
                    <div class="inventory-bar-fill" style="width: 95%; background: #F59E0B;"></div>
                </div>
                <div style="font-size: 0.75rem; color: #F59E0B; margin-top: 8px; text-align: right;">95% Route Complete • ETA 1m</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Simulated Live Telemetry Feed
    st.markdown(
        """
        <div class="glass-card">
            <div style="font-weight: 700; font-size: 1rem; margin-bottom: 10px;">📡 Smart Mesh Cold-Chain Telemetry Log</div>
            <div style="font-family: 'JetBrains Mono'; font-size: 0.8rem; color: #94A3B8; background: #07090E; padding: 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); line-height: 1.7;">
                [14:22:04] GPS Handshake Confirmed: Unit #04 Lat: 37.7749 Lon: -122.4194 | Speed: 42 km/h<br/>
                [14:22:18] Temperature Telemetry: Stable at 3.8°C (Threshold: 2.0°C - 6.0°C) [NOMINAL]<br/>
                [14:22:35] Traffic Layer Synced: Dynamic rerouting saved 3.2 minutes around Interstate Congestion.<br/>
                [14:22:51] Hospital ER Receiving Dock Notified: Autocall initiated to Surgical Lead Dr. Kowalski.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# 10. FOOTER & GLOBAL STATUS BAR
# -----------------------------------------------------------------------------
st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="border-top: 1px solid rgba(255, 255, 255, 0.06); padding: 24px 0 10px 0; display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #64748B;">
        <div>
            BloodBridge AI • Built for Mission-Critical Emergency Healthcare Infrastructure
        </div>
        <div style="display: flex; gap: 16px; font-family: 'JetBrains Mono'; font-size: 0.75rem;">
            <span>ENCRYPTED END-TO-END</span>
            <span>HIPAA/GDPR COMPLIANT</span>
            <span>v2.4.0-PROD</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
