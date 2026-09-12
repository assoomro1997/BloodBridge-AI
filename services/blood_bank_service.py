"""
BloodBridge AI - Blood Bank and Hospital Lookup
Owner: Anees (integration)

If no donor is found, the patient still needs an option.
This file gives the blood bank and hospital fallback.
"""

from backend.matching import BLOOD_COMPATIBILITY, normalise_group
from geo import city_distance

# Blood banks are worth travelling further for than a single donor.
FACILITY_RADIUS_KM = 400


def find_blood_banks(patient_blood_group, blood_banks, city=None,
                     radius_km=FACILITY_RADIUS_KM):
    """Blood banks near the patient that hold a group they can receive."""
    patient = normalise_group(patient_blood_group)
    usable = BLOOD_COMPATIBILITY.get(patient, [])
    results = []

    for bank in blood_banks:
        stock = [group for group in bank["blood_groups_available"] if group in usable]

        if not stock:
            continue

        away = city_distance(bank["location"], city) if city else None

        if away is not None and away > radius_km:
            continue

        row = dict(bank)
        row["usable_groups"] = stock
        row["distance_km"] = away
        row["same_city"] = away == 0
        results.append(row)

    results.sort(key=lambda item: (
        item["distance_km"] if item["distance_km"] is not None else 9999,
        -item["available_units"],
    ))
    return results


def find_emergency_hospitals(hospitals, city=None, radius_km=FACILITY_RADIUS_KM):
    """Hospitals with an open emergency unit, nearest first."""
    results = []

    for hospital in hospitals:
        if not hospital["emergency_available"]:
            continue

        away = city_distance(hospital["location"], city) if city else None

        if away is not None and away > radius_km:
            continue

        row = dict(hospital)
        row["distance_km"] = away
        row["same_city"] = away == 0
        results.append(row)

    results.sort(key=lambda item: (
        item["distance_km"] if item["distance_km"] is not None else 9999,
        -item["beds_free"],
    ))
    return results
