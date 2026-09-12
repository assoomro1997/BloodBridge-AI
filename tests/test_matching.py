"""
BloodBridge AI - Backend Tests
Owner: Laiba

Run from the project folder:
    python tests/test_matching.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.matching import (find_best_matches, find_compatible_donors,
                              is_compatible, is_eligible)
from services.data_loader import attach_distances, load_donors
from geo import PAKISTAN_CITIES, city_distance, find_city

passed = 0
failed = 0


def check(name, condition):
    global passed, failed
    if condition:
        passed += 1
        print(f"PASS  {name}")
    else:
        failed += 1
        print(f"FAIL  {name}")


donors = load_donors()

check("donors.csv loaded", len(donors) >= 20)

check("O- can give to anyone", is_compatible("AB+", "O-"))
check("A+ cannot give to O+", not is_compatible("O+", "A+"))
check("O- patient takes O- only", is_compatible("O-", "O-") and not is_compatible("O-", "O+"))
check("AB+ accepts all eight groups", len([g for g in
      ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"] if is_compatible("AB+", g)]) == 8)
check("lower case input works", is_compatible("b+", "o-"))
check("wrong group returns False", not is_compatible("X+", "O-"))

check("donor with 30 day gap is not eligible",
      not is_eligible({"eligible": True, "last_donation_days": 30}))
check("donor with 200 day gap is eligible",
      is_eligible({"eligible": True, "last_donation_days": 200}))

shortlist = find_compatible_donors("B+", donors)
check("unavailable donors removed", all(d["available"] for d in shortlist))
check("ineligible donors removed", all(d["eligible"] for d in shortlist))
check("only compatible groups remain",
      all(d["blood_group"] in ["B+", "B-", "O+", "O-"] for d in shortlist))

for group in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
    result = find_best_matches(group, "high", donors)
    check(f"{group} search runs without error", isinstance(result, list))

high = find_best_matches("B+", "high", donors)
low = find_best_matches("B+", "low", donors)
check("high urgency returns results", len(high) > 0)
check("scores are sorted high to low",
      all(high[i]["score"] >= high[i + 1]["score"] for i in range(len(high) - 1)))
check("urgency changes the ranking or the scores",
      [d["name"] for d in high] != [d["name"] for d in low]
      or high[0]["score"] != low[0]["score"])
check("high urgency puts the nearest donor first",
      high[0]["distance_km"] <= 6)

# Geography
check("city list covers all provinces", len(PAKISTAN_CITIES) >= 40)
check("Karachi to Lahore is about 1030 km", 1000 <= city_distance("Karachi", "Lahore") <= 1070)
check("same city is zero km", city_distance("Lahore", "Lahore") == 0.0)
check("unknown city returns None", city_distance("Atlantis", "Lahore") is None)
check("loose city match works", find_city("nawabshah, sindh") == "Nawabshah")

local = attach_distances(donors, "Karachi")
check("far donors dropped from the radius", all(d["distance_km"] <= 150 for d in local))
check("Karachi search keeps Karachi donors",
      any(d["city"] == "Karachi" for d in local))
check("Karachi search drops Quetta donors",
      not any(d["city"] == "Quetta" for d in local))
check("unknown patient city does not drop everyone",
      len(attach_distances(donors, "Atlantis")) == len(donors))

far = find_best_matches("O-", "high", attach_distances(donors, "Karachi"))
check("nationwide search still returns a match", len(far) > 0)
check("matched donor is inside the radius", far[0]["distance_km"] <= 150)

empty = find_best_matches("B+", "high", [])
check("no donors gives an empty list", empty == [])

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
