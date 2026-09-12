"""
BloodBridge AI - Blood Bank and Hospital Lookup
Owner: Anees (integration)

If no donor is found, the patient still needs an option.
This file gives the blood bank and hospital fallback.
"""

from backend.matching import BLOOD_COMPATIBILITY, normalise_group


def find_blood_banks(patient_blood_group, blood_banks, city=None):
    """Blood banks that hold a blood group the patient can receive."""
    patient = normalise_group(patient_blood_group)
    usable = BLOOD_COMPATIBILITY.get(patient, [])
    results = []

    for bank in blood_banks:
        stock = [group for group in bank["blood_groups_available"] if group in usable]

        if not stock:
            continue

        row = dict(bank)
        row["usable_groups"] = stock
        row["same_city"] = bool(city) and city.strip().lower() == bank["location"].strip().lower()
        results.append(row)

    results.sort(key=lambda item: (not item["same_city"], -item["available_units"]))
    return results


def find_emergency_hospitals(hospitals, city=None):
    """Hospitals with an open emergency unit, nearest city first."""
    results = []

    for hospital in hospitals:
        if not hospital["emergency_available"]:
            continue

        row = dict(hospital)
        row["same_city"] = bool(city) and city.strip().lower() == hospital["location"].strip().lower()
        results.append(row)

    results.sort(key=lambda item: (not item["same_city"], -item["beds_free"]))
    return results
