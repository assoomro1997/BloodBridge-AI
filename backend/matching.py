"""
BloodBridge AI - Matching Engine
Owner: Laiba (Backend / Python)

This file decides WHICH donor is the best match.
It uses only plain Python. No AI, no Streamlit here.
"""

BLOOD_COMPATIBILITY = {
    "A+": ["A+", "A-", "O+", "O-"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
    "AB-": ["A-", "B-", "AB-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
}

MIN_DAYS_BETWEEN_DONATIONS = 90

# Urgency changes what we care about most.
# High urgency = distance matters more, because we need blood fast.
URGENCY_WEIGHTS = {
    "high": {"match": 0.30, "distance": 0.50, "readiness": 0.20},
    "medium": {"match": 0.40, "distance": 0.35, "readiness": 0.25},
    "low": {"match": 0.50, "distance": 0.20, "readiness": 0.30},
}


def normalise_group(blood_group):
    return str(blood_group).strip().upper().replace(" ", "")


def is_compatible(patient_blood_group, donor_blood_group):
    """True if this donor can give blood to this patient."""
    patient = normalise_group(patient_blood_group)
    donor = normalise_group(donor_blood_group)

    if patient not in BLOOD_COMPATIBILITY:
        return False

    return donor in BLOOD_COMPATIBILITY[patient]


def is_eligible(donor):
    """
    Donor must be marked eligible AND must have waited 90 days
    since the last donation. A blood bank still does the final check.
    """
    if not donor.get("eligible", False):
        return False

    days = donor.get("last_donation_days", MIN_DAYS_BETWEEN_DONATIONS)
    return int(days) >= MIN_DAYS_BETWEEN_DONATIONS


def find_compatible_donors(patient_blood_group, donors):
    """Keep only donors who are compatible, available and eligible."""
    shortlist = []

    for donor in donors:
        if not is_compatible(patient_blood_group, donor.get("blood_group", "")):
            continue
        if not donor.get("available", False):
            continue
        if not is_eligible(donor):
            continue

        shortlist.append(dict(donor))

    return shortlist


def match_points(patient_blood_group, donor_blood_group):
    """Same group is the first choice. Compatible group is second choice."""
    if normalise_group(patient_blood_group) == normalise_group(donor_blood_group):
        return 100
    return 70


def distance_points(distance_km):
    """0 km gives 100 points. 25 km or more gives 0 points."""
    try:
        distance = float(distance_km)
    except (TypeError, ValueError):
        return 0

    if distance <= 0:
        return 100
    if distance >= 25:
        return 0

    return round(100 - (distance * 4), 2)


def readiness_points(donor):
    """A donor who donated long ago is more ready to donate now."""
    days = donor.get("last_donation_days", MIN_DAYS_BETWEEN_DONATIONS)

    try:
        days = int(days)
    except (TypeError, ValueError):
        days = MIN_DAYS_BETWEEN_DONATIONS

    if days >= 365:
        return 100
    if days >= 180:
        return 80
    if days >= 120:
        return 60
    return 40


def calculate_score(donor, patient_blood_group, urgency):
    """
    Final score out of 100.
    Urgency decides how much each part counts.
    """
    level = str(urgency).strip().lower()
    weights = URGENCY_WEIGHTS.get(level, URGENCY_WEIGHTS["medium"])

    score = (
        match_points(patient_blood_group, donor.get("blood_group", "")) * weights["match"]
        + distance_points(donor.get("distance_km", 999)) * weights["distance"]
        + readiness_points(donor) * weights["readiness"]
    )

    return round(score, 1)


def build_reason(donor, patient_blood_group, urgency):
    """Short plain text line so the user knows why this donor is on top."""
    same_group = normalise_group(patient_blood_group) == normalise_group(donor.get("blood_group", ""))
    group_text = "exact blood group" if same_group else "compatible blood group"
    distance = donor.get("distance_km", "?")

    return f"{group_text}, {distance} km away, available now"


def rank_donors(donors, patient_blood_group, urgency):
    """Give every donor a score, then sort from best to worst."""
    ranked = []

    for donor in donors:
        row = dict(donor)
        row["score"] = calculate_score(row, patient_blood_group, urgency)
        row["reason"] = build_reason(row, patient_blood_group, urgency)
        ranked.append(row)

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked


def find_best_matches(patient_blood_group, urgency, donors, top_n=5):
    """
    The one function the rest of the project calls.

    Patient request -> compatibility -> available -> eligible
    -> distance and urgency ranking -> best matches
    """
    shortlist = find_compatible_donors(patient_blood_group, donors)
    ranked = rank_donors(shortlist, patient_blood_group, urgency)
    return ranked[:top_n]


if __name__ == "__main__":
    sample_donors = [
        {"name": "Ali", "blood_group": "B+", "available": True, "eligible": True,
         "distance_km": 3, "last_donation_days": 200},
        {"name": "Ahmed", "blood_group": "O+", "available": True, "eligible": True,
         "distance_km": 8, "last_donation_days": 120},
        {"name": "Bilal", "blood_group": "B+", "available": False, "eligible": True,
         "distance_km": 1, "last_donation_days": 150},
    ]

    print("BloodBridge AI - matching engine test")
    for donor in find_best_matches("B+", "high", sample_donors):
        print(donor["name"], donor["blood_group"], donor["score"], "|", donor["reason"])
