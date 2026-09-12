"""
BloodBridge AI - Interface
Owner: Iqra (Frontend)

Every screen piece is one small function.
These functions only draw things. They never decide a match.

Design notes:
  The donor card is built to read like the label on a blood bag.
  The colour block on the left carries the group and the rank.
  Crimson means an exact group match. Slate means a compatible substitute.
  Urgency uses the colours of real emergency triage tags.
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
    "high": "every minute counts",
    "medium": "needed today",
    "low": "planned in advance",
}

STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap');

:root {
    --ink: #1B2A33;
    --body: #56666F;
    --faint: #8496A0;
    --crimson: #A4161A;
    --crimson-dark: #7D1114;
    --paper: #EEF1F3;
    --line: #D5DDE1;
    --amber: #9C5D00;
    --green: #2C6E49;
}

html, body, .stApp, .stMarkdown { font-family: 'IBM Plex Sans', system-ui, sans-serif; }
.block-container { padding-top: 2.2rem; padding-bottom: 4rem; max-width: 780px; }
#MainMenu, footer { visibility: hidden; }

.bb-mast { margin-bottom: 1.5rem; }
.bb-logo {
    font-size: 2.25rem; font-weight: 700; color: var(--ink);
    letter-spacing: -0.03em; line-height: 1.1;
}
.bb-logo span { color: var(--crimson); }
.bb-mast p { font-size: 1rem; color: var(--body); margin: 0.35rem 0 0 0; }
.bb-status {
    display: flex; gap: 1.4rem; flex-wrap: wrap;
    border-top: 1px solid var(--line); margin-top: 1rem; padding-top: 0.7rem;
    font-size: 0.8rem; color: var(--faint);
}
.bb-status b { color: var(--ink); font-weight: 600; }

.bb-found {
    display: flex; align-items: baseline; justify-content: space-between;
    gap: 1rem; margin: 2rem 0 0.9rem 0;
    border-bottom: 2px solid var(--ink); padding-bottom: 0.5rem;
}
.bb-found__title {
    font-size: 1.3rem; font-weight: 600; color: var(--ink);
    letter-spacing: -0.02em; line-height: 1.2;
}
.bb-found span { font-size: 0.82rem; color: var(--faint); white-space: nowrap; }

.bb-card {
    display: flex; align-items: stretch;
    border: 1px solid var(--line); border-radius: 6px;
    background: #FFFFFF; overflow: hidden; margin-bottom: 0.7rem;
}
.bb-tag {
    flex: 0 0 82px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: var(--crimson); color: #FFFFFF; padding: 0.9rem 0.4rem;
}
.bb-tag--sub { background: var(--ink); }
.bb-tag__group { font-size: 1.6rem; font-weight: 700; line-height: 1; letter-spacing: -0.04em; }
.bb-tag__rank { font-size: 0.68rem; margin-top: 0.35rem; opacity: 0.78; font-weight: 500; }

.bb-main { flex: 1 1 auto; padding: 0.85rem 1.1rem; min-width: 0; overflow-wrap: anywhere; }
.bb-name { font-size: 1.12rem; font-weight: 600; color: var(--ink); margin: 0; letter-spacing: -0.01em; }
.bb-meta { font-size: 0.88rem; color: var(--body); margin: 0.2rem 0 0 0; }
.bb-why { font-size: 0.82rem; color: var(--faint); margin: 0.35rem 0 0 0; }
.bb-id {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem;
    color: var(--faint); margin: 0.5rem 0 0 0; letter-spacing: 0.03em;
}
.bb-consent {
    font-family: 'IBM Plex Sans', sans-serif; letter-spacing: 0;
    margin-left: 0.7rem;
}

.bb-score {
    flex: 0 0 96px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    border-left: 1px solid var(--line); padding: 0.9rem 0.5rem;
}
.bb-score__num { font-size: 1.7rem; font-weight: 700; color: var(--ink); line-height: 1; letter-spacing: -0.03em; }
.bb-score__lab { font-size: 0.64rem; color: var(--faint); margin-top: 0.25rem; }
.bb-meter {
    display: block; width: 58px; height: 3px; background: var(--line);
    margin-top: 0.5rem; border-radius: 2px; overflow: hidden;
}
.bb-meter i { display: block; height: 100%; background: var(--crimson); }

@media (max-width: 520px) {
    .bb-card { flex-wrap: wrap; }
    .bb-score { flex: 1 1 100%; flex-direction: row; gap: 0.6rem;
                border-left: none; border-top: 1px solid var(--line); padding: 0.55rem; }
    .bb-meter { margin-top: 0; }
}

.bb-empty {
    border: 1px solid var(--line); border-left: 4px solid var(--amber);
    border-radius: 6px; background: #FFFFFF; padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
}
.bb-empty__title { font-size: 1.05rem; font-weight: 600; color: var(--ink); }
.bb-empty p { font-size: 0.88rem; color: var(--body); margin: 0.4rem 0 0 0; }

.bb-read { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.3rem 0 0.2rem 0; }
.bb-chip {
    border: 1px solid var(--line); border-radius: 4px; background: #FFFFFF;
    padding: 0.42rem 0.75rem; font-size: 0.88rem; color: var(--ink); font-weight: 600;
}
.bb-chip small { color: var(--faint); display: block; font-size: 0.66rem; font-weight: 400; }
.bb-chip--high { border-left: 3px solid var(--crimson); }
.bb-chip--medium { border-left: 3px solid var(--amber); }
.bb-chip--low { border-left: 3px solid var(--green); }

.bb-sub {
    font-size: 1.05rem; font-weight: 600; color: var(--ink);
    margin: 1.8rem 0 0.5rem 0; letter-spacing: -0.01em;
}
.bb-row {
    display: flex; align-items: flex-start; justify-content: space-between;
    gap: 1rem; padding: 0.75rem 0; border-bottom: 1px solid var(--line);
}
.bb-row__name { font-size: 0.96rem; font-weight: 600; color: var(--ink); margin: 0; }
.bb-row__meta { font-size: 0.82rem; color: var(--body); margin: 0.18rem 0 0 0; }
.bb-row__stock { font-size: 0.78rem; color: var(--faint); margin: 0.22rem 0 0 0; }
.bb-row__far {
    flex: 0 0 auto; font-size: 0.78rem; color: var(--body);
    background: var(--paper); border-radius: 3px; padding: 0.25rem 0.5rem; white-space: nowrap;
}

.bb-sms {
    border: 1px solid var(--line); border-radius: 6px 6px 6px 2px;
    background: var(--paper); padding: 0.9rem 1.1rem;
    font-size: 0.9rem; color: var(--ink); line-height: 1.55;
}
.bb-note { font-size: 0.76rem; color: var(--faint); margin-top: 0.45rem; }

.stButton > button {
    background: var(--crimson); color: #FFFFFF; border: none; border-radius: 5px;
    font-weight: 600; font-size: 0.95rem; padding: 0.6rem 1rem;
    font-family: 'IBM Plex Sans', sans-serif;
}
.stButton > button:hover { background: var(--crimson-dark); color: #FFFFFF; }
.stButton > button:focus-visible { outline: 3px solid var(--amber); outline-offset: 2px; }

.stTabs [data-baseweb="tab-list"] { gap: 1.6rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] { font-weight: 600; color: var(--faint); padding: 0.5rem 0; }
.stTabs [aria-selected="true"] { color: var(--ink); }

[data-testid="stSidebar"] { background: var(--paper); border-right: 1px solid var(--line); }

.bb-foot {
    border-top: 1px solid var(--line); margin-top: 2.6rem; padding-top: 0.8rem;
    font-size: 0.76rem; color: var(--faint);
}
</style>
"""


def inject_styles():
    st.markdown(STYLES, unsafe_allow_html=True)


def show_header(provider="offline", donors=0, banks=0, hospitals=0):
    inject_styles()
    engine = {"groq": "Llama 3.1 on Groq",
              "huggingface": "Hugging Face Inference",
              "offline": "an offline rule reader"}.get(provider, provider)

    st.markdown(
        f"""
        <div class="bb-mast">
            <div class="bb-logo" role="heading" aria-level="1">BloodBridge <span>AI</span></div>
            <p>Right blood. Right place. Right time.</p>
            <div class="bb-status">
                <span><b>{donors}</b> donors</span>
                <span><b>{banks}</b> blood banks</span>
                <span><b>{hospitals}</b> hospitals</span>
                <span>Reading requests with <b>{engine}</b></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_request_form():
    """Draws the patient form. Returns what the user chose."""
    col1, col2 = st.columns(2)

    with col1:
        blood_group = st.selectbox("Blood group needed", BLOOD_GROUPS, index=2)
        city = st.selectbox("Patient city", CITIES, index=CITIES.index("Nawabshah"))

    with col2:
        urgency = st.selectbox("How urgent", URGENCY_LEVELS,
                               format_func=lambda u: f"{u.title()}, {URGENCY_WORDS[u]}")
        units = st.number_input("Units needed", min_value=1, max_value=10, value=1)

    hospital = st.text_input("Hospital or area", "Civil Hospital Nawabshah")
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
        height=90,
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
            <div class="bb-chip"><small>Blood group</small>{group}</div>
            <div class="bb-chip bb-chip--{urgency}"><small>Urgency</small>{urgency.title()}</div>
            <div class="bb-chip"><small>Location</small>{place}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_result_count(count, city, radius_km=150):
    st.markdown(
        f"""
        <div class="bb-found">
            <div class="bb-found__title" role="heading" aria-level="2">{count} {'donor' if count == 1 else 'donors'} ready to help</div>
            <span>within {radius_km} km of {city}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_donor_results(results, patient_group="", show_contact=False):
    """Draws the ranked donor cards."""
    for position, donor in enumerate(results, start=1):
        exact = str(donor.get("blood_group", "")).upper() == str(patient_group).upper()
        tag_class = "bb-tag" if exact else "bb-tag bb-tag--sub"
        score = float(donor.get("score", 0))
        contact = donor.get("contact", "") if show_contact else "awaiting donor consent"

        st.markdown(
            f"""
            <div class="bb-card">
                <div class="{tag_class}">
                    <span class="bb-tag__group">{donor['blood_group']}</span>
                    <span class="bb-tag__rank">no. {position}</span>
                </div>
                <div class="bb-main">
                    <p class="bb-name">{donor['name']}</p>
                    <p class="bb-meta">{donor['distance_km']} km away in {donor.get('city', '')}</p>
                    <p class="bb-why">{donor.get('reason', '')}</p>
                    <p class="bb-id">{donor.get('donor_id', '')}<span class="bb-consent">{contact}</span></p>
                </div>
                <div class="bb-score">
                    <span class="bb-score__num">{donor.get('score', 0)}</span>
                    <span class="bb-score__lab">match score</span>
                    <span class="bb-meter"><i style="width:{min(score, 100)}%"></i></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_no_donor(city, radius_km=150):
    st.markdown(
        f"""
        <div class="bb-found">
            <div class="bb-found__title" role="heading" aria-level="2">No donor free within {radius_km} km</div>
            <span>searched around {city}</span>
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
        far = f'<span class="bb-row__far">{away} km</span>' if away else '<span class="bb-row__far">in city</span>'
        rows += f"""<div class="bb-row"><div>
            <p class="bb-row__name">{bank['name']}</p>
            <p class="bb-row__meta">{bank['location']} &nbsp;&nbsp; {bank['available_units']} units &nbsp;&nbsp; {hours}</p>
            <p class="bb-row__stock">Usable groups {', '.join(bank['usable_groups'])} &nbsp;&nbsp; {bank['contact']}</p>
            </div>{far}</div>"""

    st.markdown(rows, unsafe_allow_html=True)


def show_hospitals(hospitals):
    if not hospitals:
        return

    st.markdown('<p class="bb-sub">Emergency units open now</p>', unsafe_allow_html=True)
    rows = ""

    for hospital in hospitals[:4]:
        away = hospital.get("distance_km")
        far = f'<span class="bb-row__far">{away} km</span>' if away else '<span class="bb-row__far">in city</span>'
        rows += f"""<div class="bb-row"><div>
            <p class="bb-row__name">{hospital['name']}</p>
            <p class="bb-row__meta">{hospital['location']} &nbsp;&nbsp; {hospital['beds_free']} beds free</p>
            <p class="bb-row__stock">{hospital['contact']}</p>
            </div>{far}</div>"""

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
