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
from services.data_loader import SEARCH_RADIUS_KM, attach_distances, load_blood_banks, load_donors, load_hospitals

st.set_page_config(page_title="BloodBridge AI", page_icon="🩸", layout="centered")


@st.cache_data
def get_data():
    return load_donors(), load_blood_banks(), load_hospitals()


def run_search(blood_group, urgency, city, hospital, donors, banks, hospitals, explain=False):
    """One search run, used by both tabs."""
    nearby = attach_distances(donors, city)
    matches = find_best_matches(blood_group, urgency, nearby, top_n=5)

    if matches:
        if explain:
            matches[0]["reason"] = explain_match(matches[0], blood_group, urgency)

        ui.show_result_count(len(matches), city, SEARCH_RADIUS_KM)
        ui.show_donor_results(matches, patient_group=blood_group)
        ui.show_sms_preview(
            generate_donor_message(matches[0]["name"], blood_group, urgency, hospital)
        )
    else:
        ui.show_no_donor(city, SEARCH_RADIUS_KM)

    ui.show_blood_banks(find_blood_banks(blood_group, banks, city))
    ui.show_hospitals(find_emergency_hospitals(hospitals, city))


def main():
    donors, banks, hospitals = get_data()
    provider = get_provider()

    ui.show_header(provider, len(donors), len(banks), len(hospitals))

    tab_form, tab_ai = st.tabs(["Quick request", "Describe it in words"])

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
                st.error("No blood group found in that message. Please write it, for example B+.")
            else:
                place = parsed.get("location") or "Nawabshah"
                run_search(
                    parsed["blood_group"], parsed.get("urgency", "medium"), place, place,
                    donors, banks, hospitals, explain=True,
                )

    ui.show_footer(provider)


if __name__ == "__main__":
    main()
