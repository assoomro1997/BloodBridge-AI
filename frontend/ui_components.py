"""
BloodBridge AI - Streamlit UI Components
Owner: Iqra (Frontend)

Every screen piece lives here as one small function.
These functions only draw things. They never do matching.
"""

import streamlit as st

from utils.geo import CITY_NAMES

BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
URGENCY_LEVELS = ["high", "medium", "low"]
CITIES = CITY_NAMES

MEDAL = {1: "1st", 2: "2nd", 3: "3rd"}

CUSTOM_CSS = """
<style>
.bb-card {
    background: #FFFFFF;
    border: 1px solid #E6E6E6;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.bb-rank {
    display: inline-block;
    background: #990011;
    color: #FFFFFF;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 12px;
    font-weight: 700;
}
.bb-name { font-size: 19px; font-weight: 700; color: #1A1A1A; margin-top: 6px; }
.bb-line { font-size: 14px; color: #555555; margin-top: 4px; }
.bb-score { float: right; font-size: 26px; font-weight: 700; color: #990011; }
</style>
"""


def show_header():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.title("BloodBridge AI")
    st.caption("Right blood. Right place. Right time.")


def show_request_form():
    """Draws the patient form. Returns what the user typed."""
    col1, col2 = st.columns(2)

    with col1:
        blood_group = st.selectbox("Patient blood group", BLOOD_GROUPS, index=2)
        city = st.selectbox("Patient city", CITIES, index=CITIES.index("Nawabshah"))

    with col2:
        urgency = st.selectbox("Urgency", URGENCY_LEVELS)
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
        "Describe the emergency in your own words",
        "My brother urgently needs B+ blood at Civil Hospital Nawabshah",
        height=90,
    )
    send = st.button("Read request with AI", type="primary", use_container_width=True)
    return text, send


def show_parsed_request(parsed):
    col1, col2, col3 = st.columns(3)
    col1.metric("Blood group", parsed.get("blood_group") or "not found")
    col2.metric("Urgency", str(parsed.get("urgency", "medium")).title())
    col3.metric("Location", parsed.get("location") or "not found")


def show_donor_results(results, show_contact=False):
    """Draws the ranked donor cards."""
    if not results:
        st.warning("No matching donor found. Check the blood bank list below.")
        return

    st.subheader(f"Top {len(results)} matching donors")

    for position, donor in enumerate(results, start=1):
        rank = MEDAL.get(position, f"{position}th")
        contact = donor.get("contact", "") if show_contact else "hidden until donor accepts"

        st.markdown(
            f"""
            <div class="bb-card">
                <span class="bb-score">{donor['score']}</span>
                <span class="bb-rank">{rank} match</span>
                <div class="bb-name">{donor['name']} &nbsp; ({donor['blood_group']})</div>
                <div class="bb-line">{donor['distance_km']} km away &nbsp;|&nbsp; {donor.get('city', '')}
                &nbsp;|&nbsp; contact: {contact}</div>
                <div class="bb-line">{donor.get('reason', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def show_blood_banks(banks):
    if not banks:
        st.info("No blood bank stock found for this group.")
        return

    st.subheader("Blood banks with usable stock")

    for bank in banks[:4]:
        open_text = "Open 24 hours" if bank["open_24h"] else "Day hours only"
        away = bank.get("distance_km")
        place = bank["location"] if not away else f"{bank['location']} ({away} km)"
        st.markdown(
            f"**{bank['name']}** - {place}  \n"
            f"Usable groups: {', '.join(bank['usable_groups'])}  \n"
            f"{bank['available_units']} units | {open_text} | {bank['contact']}"
        )


def show_hospitals(hospitals):
    if not hospitals:
        st.info("No emergency hospital found.")
        return

    st.subheader("Emergency hospitals")

    for hospital in hospitals[:4]:
        away = hospital.get("distance_km")
        place = hospital["location"] if not away else f"{hospital['location']} ({away} km)"
        st.markdown(
            f"**{hospital['name']}** - {place}  \n"
            f"{hospital['beds_free']} emergency beds free | {hospital['contact']}"
        )


def show_sms_preview(message):
    st.subheader("Message for the donor")
    st.code(message, language=None)
    st.caption("In the full version this goes out by SMS or WhatsApp.")


def show_footer(provider):
    label = {"groq": "Groq Llama 3.1", "huggingface": "Hugging Face Inference", "offline": "Offline rules"}
    st.divider()
    st.caption(f"AI engine: {label.get(provider, provider)} | Data: demo CSV files | Built for the hackathon")
