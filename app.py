"""
BloodBridge AI - Main Application
Owner: Anees (Technical Lead / Integration)

This file connects the four modules:
    frontend  -> what the user sees
    ai        -> reads the request
    backend   -> decides the best donors
    services  -> loads data, finds blood banks and hospitals
"""

import streamlit as st

from ai.ai_module import analyze_request, explain_match, generate_donor_message, get_provider
from backend.matching import find_best_matches
from frontend import ui_components as ui
from services.blood_bank_service import find_blood_banks, find_emergency_hospitals
from services.data_loader import load_blood_banks, load_donors, load_hospitals

st.set_page_config(page_title="BloodBridge AI", page_icon="🩸", layout="centered")


@st.cache_data
def get_data():
    return load_donors(), load_blood_banks(), load_hospitals()


def run_search(blood_group, urgency, city, hospital, donors, banks, hospitals, use_ai_text=False):
    """One search run, used by both tabs."""
    matches = find_best_matches(blood_group, urgency, donors, top_n=5)

    if matches and use_ai_text:
        matches[0]["reason"] = explain_match(matches[0], blood_group, urgency)

    ui.show_donor_results(matches)

    if matches:
        message = generate_donor_message(matches[0]["name"], blood_group, urgency, hospital)
        ui.show_sms_preview(message)

    ui.show_blood_banks(find_blood_banks(blood_group, banks, city))
    ui.show_hospitals(find_emergency_hospitals(hospitals, city))


def main():
    donors, banks, hospitals = get_data()
    ui.show_header()

    with st.sidebar:
        st.header("System status")
        st.write(f"Donors in database: {len(donors)}")
        st.write(f"Blood banks: {len(banks)}")
        st.write(f"Hospitals: {len(hospitals)}")
        st.write(f"AI provider: {get_provider()}")
        st.divider()
        st.caption("Demo data only. A blood bank must confirm every donor before donation.")

    tab_form, tab_ai = st.tabs(["Quick request", "AI request"])

    with tab_form:
        form = ui.show_request_form()

        if form["search"]:
            run_search(
                form["blood_group"], form["urgency"], form["city"], form["hospital"],
                donors, banks, hospitals,
            )

    with tab_ai:
        text, send = ui.show_ai_form()

        if send:
            with st.spinner("Reading the request..."):
                parsed = analyze_request(text)

            ui.show_parsed_request(parsed)

            if not parsed.get("blood_group"):
                st.error("Blood group not found in the message. Please write it, for example B+.")
            else:
                run_search(
                    parsed["blood_group"],
                    parsed.get("urgency", "medium"),
                    parsed.get("location") or "Nawabshah",
                    parsed.get("location") or "the nearest hospital",
                    donors, banks, hospitals,
                    use_ai_text=True,
                )

    ui.show_footer(get_provider())


if __name__ == "__main__":
    main()
