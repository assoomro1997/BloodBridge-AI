"""
BloodBridge AI - End to End Test
Owner: Anees

This is the full journey:
    sentence -> AI -> backend -> data -> results

Run from the project folder:
    python tests/test_integration.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.ai_module import analyze_request, generate_donor_message
from backend.matching import find_best_matches
from services.blood_bank_service import find_blood_banks, find_emergency_hospitals
from services.data_loader import attach_distances, load_blood_banks, load_donors, load_hospitals

SCENARIOS = [
    "My brother urgently needs B+ blood near Nawabshah",
    "O negative blood required in Lahore, routine case next week",
    "Accident, AB negative khoon foran chahiye Peshawar mein",
    "Patient needs A- blood in Quetta, serious condition",
    "Urgent B+ blood required at Gilgit",
]

donors = load_donors()
banks = load_blood_banks()
hospitals = load_hospitals()

print("Loaded:", len(donors), "donors,", len(banks), "blood banks,", len(hospitals), "hospitals\n")

failed = 0

for number, sentence in enumerate(SCENARIOS, start=1):
    print("=" * 60)
    print(f"SCENARIO {number}: {sentence}")
    print("=" * 60)

    parsed = analyze_request(sentence)
    print("AI read:", parsed["blood_group"], "|", parsed["urgency"], "|", parsed["location"])

    if not parsed["blood_group"]:
        print("RESULT: blood group not found, asking user to retype")
        failed += 1
        continue

    city = parsed["location"] or "Nawabshah"
    nearby = attach_distances(donors, city)
    print(f"Donors inside {city} search radius: {len(nearby)}")
    matches = find_best_matches(parsed["blood_group"], parsed["urgency"], nearby)

    if matches:
        print(f"\nTop {len(matches)} donors:")
        for position, donor in enumerate(matches, start=1):
            print(f"  {position}. {donor['name']:<20} {donor['blood_group']:<4} "
                  f"{donor['city']:<12} {donor['distance_km']:>6} km   score {donor['score']}")
        print("\nSMS:", generate_donor_message(matches[0]["name"], parsed["blood_group"], parsed["urgency"]))
    else:
        print("\nNo donor found. Falling back to blood banks.")

    bank_list = find_blood_banks(parsed["blood_group"], banks, parsed["location"])
    print(f"\nBlood banks with usable stock: {len(bank_list)}")
    for bank in bank_list[:2]:
        print(f"  {bank['name']} - {bank['available_units']} units - {bank['location']}")

    emergency = find_emergency_hospitals(hospitals, parsed["location"])
    print(f"Emergency hospitals open: {len(emergency)}")
    print()

print("=" * 60)
print(f"{len(SCENARIOS) - failed} of {len(SCENARIOS)} scenarios completed end to end")
sys.exit(1 if failed else 0)
