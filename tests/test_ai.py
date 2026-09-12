"""
BloodBridge AI - AI Module Tests
Owner: Fizza

Run from the project folder:
    python tests/test_ai.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.ai_module import analyze_request, generate_donor_message, get_provider

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


print("Provider in use:", get_provider(), "\n")

case1 = analyze_request("My brother urgently needs B+ blood near Nawabshah")
check("blood group read correctly", case1["blood_group"] == "B+")
check("urgency read as high", case1["urgency"] == "high")
check("city read correctly", case1["location"] == "Nawabshah")

case2 = analyze_request("Mujhe O negative blood chahiye Sakrand mein")
check("O negative written in words is read", case2["blood_group"] == "O-")

case3 = analyze_request("Accident case, AB positive khoon ki foran zarurat hai Daur mein")
check("roman urdu urgency word works", case3["urgency"] == "high")
check("AB positive is read", case3["blood_group"] == "AB+")

case4 = analyze_request("I need help")
check("missing blood group returns None", case4["blood_group"] is None)

case5 = analyze_request("")
check("empty message does not crash", case5["blood_group"] is None)

sms = generate_donor_message("Ali Raza", "B+", "high", "Civil Hospital Nawabshah")
check("sms is generated", len(sms) > 30)
check("sms names the donor", "Ali Raza" in sms or "ali raza" in sms.lower())

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
