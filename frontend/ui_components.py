"""
BloodBridge AI - Interface
Owner: Iqra (Frontend)

Every screen piece is one small function.
These functions only draw things. They never decide a match.

Design notes:
  The donor card reads like the label on a blood bag. The colour block on the
  left carries the group and the rank. Crimson means an exact group match,
  slate means a compatible substitute, so colour carries meaning.

  Urgency is a three way triage control using the colours of real emergency
  triage tags, not a dropdown, because one tap beats three in an emergency.

  The match score is drawn as an arc, the way a monitor shows a reading.

  Two themes. Day is a clinical white ward. Night is a low light control room,
  with the accent brightened so contrast holds on a dark surface.
"""

import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geo import CITY_NAMES

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
URGENCY_LEVELS = ["high", "medium", "low"]
CITIES = CITY_NAMES

URGENCY_WORDS = {
    "high": "Every minute counts",
    "medium": "Needed today",
    "low": "Planned ahead",
}

GAUGE_CIRCUMFERENCE = 113.1  # 2 * pi * r, where r = 18

PALETTES = {
    "light": """
        --canvas: #F5F7F9;
        --surface: #FFFFFF;
        --raised: #FFFFFF;
        --ink: #16242D;
        --body: #51636D;
        --faint: #83969F;
        --line: #DCE3E8;
        --line-soft: #E9EEF1;
        --crimson: #B01218;
        --crimson-deep: #800D12;
        --crimson-wash: #FBEDEE;
        --tag-sub: #16242D;
        --tag-sub-ink: #FFFFFF;
        --amber: #A86400;
        --green: #1F7A4C;
        --shadow: 0 1px 2px rgba(22, 36, 45, 0.06);
    """,
    "dark": """
        --canvas: #0D151C;
        --surface: #15202A;
        --raised: #1B2833;
        --ink: #EDF3F7;
        --body: #A5B6C1;
        --faint: #6F8492;
        --line: #27353F;
        --line-soft: #1E2B35;
        --crimson: #E8474D;
        --crimson-deep: #C02830;
        --crimson-wash: #2A1417;
        --tag-sub: #2E4150;
        --tag-sub-ink: #EDF3F7;
        --amber: #E5A64A;
        --green: #46BE86;
        --shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
    """,
}

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap');

html, body, .stApp, .stMarkdown, input, textarea, button, select {
    font-family: 'IBM Plex Sans', system-ui, sans-serif;
}
.stApp { background: var(--canvas); }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.6rem; padding-bottom: 4rem; max-width: 820px; }
#MainMenu, footer { visibility: hidden; }

/* ---------------- masthead ---------------- */
.bb-logo {
    font-size: 2.1rem; font-weight: 700; color: var(--ink);
    letter-spacing: -0.035em; line-height: 1.05;
}
.bb-logo span { color: var(--crimson); }
.bb-tagline { font-size: 0.97rem; color: var(--body); margin-top: 0.25rem; }

.bb-status {
    display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: center;
    border-top: 1px solid var(--line); border-bottom: 1px solid var(--line);
    margin: 1rem 0 0.2rem 0; padding: 0.6rem 0;
    font-size: 0.79rem; color: var(--faint);
}
.bb-status b { color: var(--ink); font-weight: 600; }
.bb-dot {
    width: 6px; height: 6px; border-radius: 50%; background: var(--green);
    display: inline-block; margin-right: 0.4rem; vertical-align: middle;
}

/* ---------------- section heads ---------------- */
.bb-found {
    display: flex; align-items: baseline; justify-content: space-between;
    gap: 1rem; margin: 1.9rem 0 0.85rem 0;
    border-bottom: 2px solid var(--ink); padding-bottom: 0.45rem;
}
.bb-found__title {
    font-size: 1.28rem; font-weight: 600; color: var(--ink);
    letter-spacing: -0.02em; line-height: 1.2;
}
.bb-found__meta { font-size: 0.8rem; color: var(--faint); white-space: nowrap; }
.bb-sub {
    font-size: 1.02rem; font-weight: 600; color: var(--ink);
    margin: 1.9rem 0 0.4rem 0; letter-spacing: -0.01em;
}

/* ---------------- donor card ---------------- */
.bb-card {
    display: flex; align-items: stretch;
    border: 1px solid var(--line); border-radius: 8px;
    background: var(--surface); box-shadow: var(--shadow);
    overflow: hidden; margin-bottom: 0.65rem;
    animation: bbRise 0.3s cubic-bezier(0.2, 0.7, 0.3, 1) both;
}
@keyframes bbRise {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: none; }
}
@media (prefers-reduced-motion: reduce) {
    .bb-card { animation: none; }
}

.bb-tag {
    flex: 0 0 88px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: var(--crimson); color: #FFFFFF; padding: 0.95rem 0.4rem;
}
.bb-tag--sub { background: var(--tag-sub); color: var(--tag-sub-ink); }
.bb-tag__group { font-size: 1.65rem; font-weight: 700; line-height: 1; letter-spacing: -0.045em; }
.bb-tag__rank { font-size: 0.66rem; margin-top: 0.4rem; opacity: 0.8; font-weight: 500; }

.bb-main { flex: 1 1 auto; padding: 0.85rem 1.1rem; min-width: 0; overflow-wrap: anywhere; }
.bb-name {
    font-size: 1.1rem; font-weight: 600; color: var(--ink);
    margin: 0; letter-spacing: -0.015em;
}
.bb-meta { font-size: 0.87rem; color: var(--body); margin: 0.2rem 0 0 0; }
.bb-why { font-size: 0.81rem; color: var(--faint); margin: 0.3rem 0 0 0; }
.bb-id {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.67rem;
    color: var(--faint); margin: 0.5rem 0 0 0; letter-spacing: 0.03em;
}
.bb-consent { font-family: 'IBM Plex Sans', sans-serif; letter-spacing: 0; margin-left: 0.7rem; }
.bb-free { color: var(--green); font-weight: 600; }

.bb-score {
    flex: 0 0 104px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    border-left: 1px solid var(--line-soft); padding: 0.8rem 0.5rem;
}
.bb-gauge { width: 58px; height: 58px; display: block; }
.bb-gauge__track { fill: none; stroke: var(--line); stroke-width: 4; }
.bb-gauge__fill {
    fill: none; stroke: var(--crimson); stroke-width: 4; stroke-linecap: round;
}
.bb-gauge__num {
    fill: var(--ink); font-size: 13px; font-weight: 700;
    font-family: 'IBM Plex Sans', sans-serif; letter-spacing: -0.03em;
}
.bb-score__lab { font-size: 0.63rem; color: var(--faint); margin-top: 0.3rem; }

@media (max-width: 640px) {
    .bb-card { flex-wrap: wrap; }
    .bb-tag { flex: 0 0 68px; }
    .bb-main { flex: 1 1 0; min-width: 0; padding: 0.75rem 0.9rem; }
    .bb-found { flex-direction: column; align-items: flex-start; gap: 0.1rem; }
    .bb-found__meta { white-space: normal; }
    .bb-score {
        flex: 1 1 100%; flex-direction: row; gap: 0.7rem; justify-content: flex-start;
        border-left: none; border-top: 1px solid var(--line-soft); padding: 0.5rem 1.1rem;
    }
    .bb-gauge { width: 40px; height: 40px; }
    .bb-score__lab { margin-top: 0; }
}

/* ---------------- empty state ---------------- */
.bb-empty {
    border: 1px solid var(--line); border-left: 4px solid var(--amber);
    border-radius: 8px; background: var(--surface); box-shadow: var(--shadow);
    padding: 1.05rem 1.25rem; margin-bottom: 0.6rem;
}
.bb-empty__title { font-size: 1.03rem; font-weight: 600; color: var(--ink); }
.bb-empty p { font-size: 0.87rem; color: var(--body); margin: 0.35rem 0 0 0; }

/* ---------------- what the AI read ---------------- */
.bb-read { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.5rem 0 0.1rem 0; }
.bb-chip {
    border: 1px solid var(--line); border-left-width: 3px; border-radius: 5px;
    background: var(--surface); padding: 0.4rem 0.8rem;
    font-size: 0.88rem; color: var(--ink); font-weight: 600;
}
.bb-chip small { color: var(--faint); display: block; font-size: 0.65rem; font-weight: 400; }
.bb-chip--high { border-left-color: var(--crimson); }
.bb-chip--medium { border-left-color: var(--amber); }
.bb-chip--low { border-left-color: var(--green); }
.bb-chip--plain { border-left-color: var(--line); }

/* ---------------- facility rows ---------------- */
.bb-row {
    display: flex; align-items: flex-start; justify-content: space-between;
    gap: 1rem; padding: 0.72rem 0; border-bottom: 1px solid var(--line-soft);
}
.bb-row__name { font-size: 0.95rem; font-weight: 600; color: var(--ink); margin: 0; }
.bb-row__meta { font-size: 0.81rem; color: var(--body); margin: 0.15rem 0 0 0; }
.bb-row__stock { font-size: 0.77rem; color: var(--faint); margin: 0.2rem 0 0 0; }
.bb-row__far {
    flex: 0 0 auto; font-size: 0.76rem; color: var(--body); font-weight: 500;
    background: var(--raised); border: 1px solid var(--line);
    border-radius: 4px; padding: 0.22rem 0.5rem; white-space: nowrap;
}

/* ---------------- donor message ---------------- */
.bb-sms {
    border: 1px solid var(--line); border-radius: 10px 10px 10px 3px;
    background: var(--raised); padding: 0.9rem 1.1rem;
    font-size: 0.89rem; color: var(--ink); line-height: 1.6;
}
.bb-note { font-size: 0.75rem; color: var(--faint); margin-top: 0.4rem; }

/* ---------------- streamlit widgets ---------------- */
.stButton > button {
    background: var(--crimson); color: #FFFFFF; border: 1px solid var(--crimson);
    border-radius: 6px; font-weight: 600; font-size: 0.95rem; padding: 0.62rem 1rem;
    transition: background 0.15s ease;
}
.stButton > button:hover { background: var(--crimson-deep); border-color: var(--crimson-deep); color: #FFFFFF; }
.stButton > button:active { background: var(--crimson-deep); color: #FFFFFF; }
.stButton > button:focus-visible { outline: 3px solid var(--amber); outline-offset: 2px; }

label, .stMarkdown p, [data-testid="stWidgetLabel"] p { color: var(--body) !important; }

/* widget surfaces, so both themes stay consistent */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInputRootElement"],
[data-testid="stTextArea"] > div > div,
[data-testid="stTextAreaRootElement"],
[data-testid="stTextArea"] > div > div > div,
[data-testid="stNumberInputContainer"],
[data-testid="stNumberInput"] > div > div {
    background-color: var(--surface) !important;
    border-color: var(--line) !important;
}
[data-testid="stSelectbox"] input,
[data-testid="stSelectbox"] > div > div div,
[data-testid="stTextInputField"],
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
    background-color: transparent !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink);
}
[data-testid="stSelectbox"] svg, [data-testid="stNumberInput"] svg { fill: var(--faint) !important; }
[data-testid="stNumberInput"] button { background: var(--raised) !important; border-color: var(--line) !important; }

ul[role="listbox"], [data-baseweb="popover"] > div > div {
    background-color: var(--surface) !important; border: 1px solid var(--line) !important;
}
ul[role="listbox"] li { color: var(--ink) !important; }
ul[role="listbox"] li:hover { background-color: var(--raised) !important; }

/* urgency as a triage control */
[data-testid="stRadio"] [role="radiogroup"] { flex-direction: row; gap: 0.45rem; flex-wrap: wrap; }
[data-testid="stRadioOption"] {
    border: 1px solid var(--line); border-left: 3px solid var(--line);
    border-radius: 6px; background: var(--surface); box-shadow: var(--shadow);
    padding: 0.5rem 0.85rem; margin: 0; cursor: pointer;
    transition: border-color 0.15s ease, background 0.15s ease;
}
[data-testid="stRadioOption"] > div > div > div:first-child { display: none !important; }
[data-testid="stRadioOption"] p { color: var(--body) !important; font-weight: 500; font-size: 0.87rem; }
[data-testid="stRadioOption"]:hover { border-color: var(--faint); }
[data-testid="stRadioOption"]:has(input:checked) { background: var(--raised); border-color: var(--faint); }
[data-testid="stRadioOption"]:has(input:checked) p { color: var(--ink) !important; font-weight: 600; }
[data-testid="stRadioOption"]:nth-of-type(1):has(input:checked) { border-left-color: var(--crimson); }
[data-testid="stRadioOption"]:nth-of-type(2):has(input:checked) { border-left-color: var(--amber); }
[data-testid="stRadioOption"]:nth-of-type(3):has(input:checked) { border-left-color: var(--green); }
[data-testid="stRadioOption"]:has(input:focus-visible) { outline: 3px solid var(--amber); outline-offset: 2px; }

.stTabs [data-baseweb="tab-list"] { gap: 1.7rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] { font-weight: 600; padding: 0.5rem 0; }
.stTabs [data-baseweb="tab"] p { color: var(--body) !important; font-weight: 600; }
.stTabs [aria-selected="true"] p { color: var(--ink) !important; }
.stTabs [data-baseweb="tab-highlight"] { background: var(--crimson); }

[data-testid="stSidebar"] { background: var(--raised); border-right: 1px solid var(--line); }

.bb-foot {
    border-top: 1px solid var(--line); margin-top: 2.4rem; padding-top: 0.75rem;
    font-size: 0.75rem; color: var(--faint);
}
"""


def current_theme():
    """Reads the toggle before the widget draws, so styles land first."""
    return "dark" if st.session_state.get("dark_mode", False) else "light"


def inject_styles(theme="light"):
    palette = PALETTES.get(theme, PALETTES["light"])
    st.markdown(f"<style>:root {{{palette}}}\n{BASE_CSS}</style>", unsafe_allow_html=True)


def show_header(provider="offline", donors=0, banks=0, hospitals=0):
    engine = {"groq": "Llama 3.1 on Groq",
              "huggingface": "Hugging Face Inference",
              "offline": "an offline rule reader"}.get(provider, provider)

    brand, switch = st.columns([5, 2], vertical_alignment="center")

    with brand:
        st.markdown(
            '<div class="bb-logo" role="heading" aria-level="1">BloodBridge <span>AI</span></div>'
            '<div class="bb-tagline">Right blood. Right place. Right time.</div>',
            unsafe_allow_html=True,
        )

    with switch:
        st.toggle("Night mode", key="dark_mode", help="Easier on the eyes in a dark ward")

    st.markdown(
        f"""
        <div class="bb-status">
            <span><span class="bb-dot"></span><b>{donors}</b> donors</span>
            <span><b>{banks}</b> blood banks</span>
            <span><b>{hospitals}</b> hospitals</span>
            <span>Reading requests with <b>{engine}</b></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_request_form():
    """Draws the patient form. Returns what the user chose."""
    col1, col2 = st.columns(2)

    with col1:
        blood_group = st.selectbox("Blood group needed", BLOOD_GROUPS, index=2)
    with col2:
        city = st.selectbox("Patient city", CITIES, index=CITIES.index("Nawabshah"))

    urgency = st.radio(
        "How urgent is it",
        URGENCY_LEVELS,
        horizontal=True,
        format_func=lambda u: f"{u.title()} - {URGENCY_WORDS[u]}",
    )

    col3, col4 = st.columns([3, 1])
    with col3:
        hospital = st.text_input("Hospital or area", "Civil Hospital Nawabshah")
    with col4:
        units = st.number_input("Units", min_value=1, max_value=10, value=1)

    search = st.button("Find donors", type="primary", use_container_width=True)

    return {
        "blood_group": blood_group,
        "urgency": urgency,
        "city": city,
        "units": units,
        "hospital": hospital,
        "search": search,
    }


def show_ai_form():
    """Free text box for the AI request reader."""
    text = st.text_area(
        "Say what you need, in English or Roman Urdu",
        "My brother urgently needs B+ blood at Civil Hospital Nawabshah",
        height=95,
    )
    send = st.button("Read this and find donors", type="primary", use_container_width=True)
    return text, send


def show_parsed_request(parsed):
    """Shows what the AI understood, so the user can check it."""
    urgency = str(parsed.get("urgency", "medium")).lower()
    group = parsed.get("blood_group") or "not found"
    place = parsed.get("location") or "not found"

    st.markdown(
        f"""
        <div class="bb-read">
            <div class="bb-chip bb-chip--plain"><small>Blood group</small>{group}</div>
            <div class="bb-chip bb-chip--{urgency}"><small>Urgency</small>{urgency.title()}</div>
            <div class="bb-chip bb-chip--plain"><small>Location</small>{place}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_result_count(count, city, radius_km=150):
    st.markdown(
        f"""
        <div class="bb-found">
            <div class="bb-found__title" role="heading" aria-level="2">
                {count} {'donor' if count == 1 else 'donors'} ready to help</div>
            <div class="bb-found__meta">within {radius_km} km of {city}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def gauge(score):
    """Match score drawn as an arc, the way a monitor shows a reading."""
    filled = max(0.0, min(float(score), 100.0)) / 100 * GAUGE_CIRCUMFERENCE
    return f"""
    <svg class="bb-gauge" viewBox="0 0 44 44" role="img" aria-label="match score {score} out of 100">
        <circle class="bb-gauge__track" cx="22" cy="22" r="18"></circle>
        <circle class="bb-gauge__fill" cx="22" cy="22" r="18"
                stroke-dasharray="{filled:.1f} {GAUGE_CIRCUMFERENCE}"
                transform="rotate(-90 22 22)"></circle>
        <text class="bb-gauge__num" x="22" y="26" text-anchor="middle">{round(float(score))}</text>
    </svg>"""


def show_donor_results(results, patient_group="", show_contact=False):
    """Draws the ranked donor cards."""
    for position, donor in enumerate(results, start=1):
        exact = str(donor.get("blood_group", "")).upper() == str(patient_group).upper()
        tag_class = "bb-tag" if exact else "bb-tag bb-tag--sub"
        contact = donor.get("contact", "") if show_contact else "awaiting donor consent"
        delay = (position - 1) * 0.05

        st.markdown(
            f"""
            <div class="bb-card" style="animation-delay:{delay:.2f}s">
                <div class="{tag_class}">
                    <span class="bb-tag__group">{donor['blood_group']}</span>
                    <span class="bb-tag__rank">no. {position}</span>
                </div>
                <div class="bb-main">
                    <p class="bb-name">{donor['name']}</p>
                    <p class="bb-meta">{donor['distance_km']} km away in {donor.get('city', '')}
                        <span class="bb-free">&nbsp;free now</span></p>
                    <p class="bb-why">{donor.get('reason', '')}</p>
                    <p class="bb-id">{donor.get('donor_id', '')}<span class="bb-consent">{contact}</span></p>
                </div>
                <div class="bb-score">
                    {gauge(donor.get('score', 0))}
                    <span class="bb-score__lab">match score</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_no_donor(city, radius_km=150):
    st.markdown(
        f"""
        <div class="bb-found">
            <div class="bb-found__title" role="heading" aria-level="2">
                No donor free within {radius_km} km</div>
            <div class="bb-found__meta">searched around {city}</div>
        </div>
        <div class="bb-empty">
            <div class="bb-empty__title" role="heading" aria-level="3">Go to a blood bank instead</div>
            <p>The blood banks below hold stock this patient can receive.
            Call ahead to confirm units before travelling.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_blood_banks(banks):
    if not banks:
        return

    st.markdown('<p class="bb-sub">Blood banks holding usable stock</p>', unsafe_allow_html=True)
    rows = ""

    for bank in banks[:4]:
        hours = "open 24 hours" if bank["open_24h"] else "day hours only"
        away = bank.get("distance_km")
        far = f"{away} km" if away else "in this city"
        rows += f"""<div class="bb-row"><div>
            <p class="bb-row__name">{bank['name']}</p>
            <p class="bb-row__meta">{bank['location']} &nbsp;&nbsp; {bank['available_units']} units &nbsp;&nbsp; {hours}</p>
            <p class="bb-row__stock">Usable groups {', '.join(bank['usable_groups'])} &nbsp;&nbsp; {bank['contact']}</p>
            </div><span class="bb-row__far">{far}</span></div>"""

    st.markdown(rows, unsafe_allow_html=True)


def show_hospitals(hospitals):
    if not hospitals:
        return

    st.markdown('<p class="bb-sub">Emergency units open now</p>', unsafe_allow_html=True)
    rows = ""

    for hospital in hospitals[:4]:
        away = hospital.get("distance_km")
        far = f"{away} km" if away else "in this city"
        rows += f"""<div class="bb-row"><div>
            <p class="bb-row__name">{hospital['name']}</p>
            <p class="bb-row__meta">{hospital['location']} &nbsp;&nbsp; {hospital['beds_free']} beds free</p>
            <p class="bb-row__stock">{hospital['contact']}</p>
            </div><span class="bb-row__far">{far}</span></div>"""

    st.markdown(rows, unsafe_allow_html=True)


def show_sms_preview(message):
    st.markdown('<p class="bb-sub">Message ready for the donor</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="bb-sms">{message}</div>'
        '<p class="bb-note">Written by the AI. In the full version this goes out '
        'by SMS or WhatsApp.</p>',
        unsafe_allow_html=True,
    )


def show_footer(provider="offline"):
    st.markdown(
        '<div class="bb-foot">Demo data. A qualified blood bank must confirm every '
        'donor before any donation takes place.</div>',
        unsafe_allow_html=True,
    )
