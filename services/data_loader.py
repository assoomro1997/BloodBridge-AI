"""
BloodBridge AI - Data Loader
Owner: Anees (integration) with Laiba (data)

Reads the CSV files from data/ and turns them into Python lists
that the matching engine can use.
"""

import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.geo import city_distance

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

TRUE_WORDS = ["true", "yes", "1", "y"]


def to_bool(value):
    return str(value).strip().lower() in TRUE_WORDS


def to_float(value, fallback=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def to_int(value, fallback=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return fallback


def read_csv(file_name):
    path = os.path.join(DATA_DIR, file_name)

    if not os.path.exists(path):
        return []

    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_donors():
    donors = []

    for row in read_csv("donors.csv"):
        donors.append({
            "donor_id": row.get("donor_id", ""),
            "name": row.get("name", ""),
            "blood_group": row.get("blood_group", "").strip().upper(),
            "available": to_bool(row.get("available")),
            "eligible": to_bool(row.get("eligible")),
            "distance_km": to_float(row.get("distance_km"), 999),
            "city": row.get("city", ""),
            "contact": row.get("contact", ""),
            "last_donation_days": to_int(row.get("last_donation_days"), 90),
        })

    return donors


def load_blood_banks():
    banks = []

    for row in read_csv("blood_banks.csv"):
        groups = [g.strip().upper() for g in row.get("blood_groups_available", "").split(",") if g.strip()]
        banks.append({
            "bank_id": row.get("bank_id", ""),
            "name": row.get("name", ""),
            "blood_groups_available": groups,
            "location": row.get("location", ""),
            "available_units": to_int(row.get("available_units")),
            "contact": row.get("contact", ""),
            "open_24h": to_bool(row.get("open_24h")),
        })

    return banks


def load_hospitals():
    hospitals = []

    for row in read_csv("hospitals.csv"):
        hospitals.append({
            "hospital_id": row.get("hospital_id", ""),
            "name": row.get("name", ""),
            "location": row.get("location", ""),
            "contact": row.get("contact", ""),
            "emergency_available": to_bool(row.get("emergency_available")),
            "beds_free": to_int(row.get("beds_free")),
        })

    return hospitals


UNKNOWN_CITY_PENALTY = 999

# A donor 1000 km away cannot help in an emergency.
# Anything past this radius is dropped and the blood bank layer takes over.
SEARCH_RADIUS_KM = 150


def attach_distances(donors, patient_city, radius_km=SEARCH_RADIUS_KM):
    """
    Turn each donor's local distance into a real distance from the patient.

    Same city  -> the donor's own local distance
    Other city -> city to city distance plus the local distance

    Donors past the search radius are dropped. The matching engine still
    reads distance_km, so nothing else changes.
    """
    if city_distance(patient_city, patient_city) is None:
        # City not in our list. Fall back to local distances only.
        return [dict(donor) for donor in donors]

    updated = []

    for donor in donors:
        row = dict(donor)
        local = to_float(row.get("distance_km"), 0)
        between = city_distance(row.get("city"), patient_city)

        if between is None:
            row["distance_km"] = UNKNOWN_CITY_PENALTY
        else:
            row["distance_km"] = round(between + local, 1)

        row["local_km"] = local

        if row["distance_km"] <= radius_km:
            updated.append(row)

    return updated


if __name__ == "__main__":
    print("Donors loaded:", len(load_donors()))
    print("Blood banks loaded:", len(load_blood_banks()))
    print("Hospitals loaded:", len(load_hospitals()))
