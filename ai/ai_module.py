"""
BloodBridge AI - AI / LLM Module
Owner: Fizza (AI / Generative AI)

What the AI does:
  1. Read a normal sentence and pull out blood group, urgency, city.
  2. Write the SMS text that goes to the donor.
  3. Write a short line explaining why a donor was picked.

What the AI does NOT do:
  It never decides blood compatibility. That is the backend job.

If no API key is set, the rule based fallback runs instead,
so the demo never breaks in front of the judges.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.geo import CITY_NAMES

GROQ_MODEL = "llama-3.1-8b-instant"
HF_MODEL = "meta-llama/Llama-3.2-3B-Instruct"

VALID_GROUPS = ["AB+", "AB-", "A+", "A-", "B+", "B-", "O+", "O-"]

HIGH_WORDS = ["urgent", "emergency", "critical", "immediately", "abhi", "foran", "fauran",
              "jaldi", "serious", "accident", "surgery", "operation", "now"]
LOW_WORDS = ["planned", "routine", "next week", "scheduled", "baad mein", "koi jaldi nahi"]

CITIES = CITY_NAMES

SYSTEM_PROMPT = """You are the request reader for a blood donation app.
Read the user message and return ONLY a JSON object, no other text.
Keys: blood_group, urgency, location, patient_note.
blood_group must be one of A+, A-, B+, B-, AB+, AB-, O+, O- or null.
urgency must be high, medium or low.
location is a city name or null.
patient_note is a short summary in one line."""


def get_provider():
    """Which AI service is available right now."""
    if os.getenv("GROQ_API_KEY"):
        return "groq"
    if os.getenv("HF_TOKEN"):
        return "huggingface"
    return "offline"


def clean_json(text):
    """LLMs sometimes wrap JSON in code fences. Strip them off."""
    text = text.strip()
    text = re.sub(r"^```[a-zA-Z]*", "", text).strip()
    text = re.sub(r"```$", "", text).strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return None

    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


def call_groq(messages):
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=400,
    )
    return response.choices[0].message.content


def call_huggingface(messages):
    from huggingface_hub import InferenceClient

    client = InferenceClient(api_key=os.getenv("HF_TOKEN"))
    response = client.chat_completion(
        model=HF_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=400,
    )
    return response.choices[0].message.content


def ask_llm(messages):
    """Try the available service. Return None if nothing works."""
    provider = get_provider()

    try:
        if provider == "groq":
            return call_groq(messages)
        if provider == "huggingface":
            return call_huggingface(messages)
    except Exception:
        return None

    return None


def rule_based_analyze(text):
    """Simple keyword reader. Runs when no API key is set."""
    upper = text.upper()
    lower = text.lower()

    blood_group = None
    for group in VALID_GROUPS:
        pattern = group.replace("+", r"\s*\+").replace("-", r"\s*-")
        if re.search(r"\b" + pattern, upper):
            blood_group = group
            break

    if not blood_group:
        word_match = re.search(r"\b(A|B|AB|O)\s*(POSITIVE|NEGATIVE)\b", upper)
        if word_match:
            sign = "+" if word_match.group(2) == "POSITIVE" else "-"
            blood_group = word_match.group(1) + sign

    urgency = "medium"
    if any(word in lower for word in HIGH_WORDS):
        urgency = "high"
    elif any(word in lower for word in LOW_WORDS):
        urgency = "low"

    location = None
    for city in sorted(CITIES, key=len, reverse=True):
        if city.lower() in lower:
            location = city
            break

    return {
        "blood_group": blood_group,
        "urgency": urgency,
        "location": location,
        "patient_note": text.strip()[:120],
        "source": "offline",
    }


def analyze_request(text):
    """
    Input : "My brother urgently needs B+ blood near Nawabshah"
    Output: {"blood_group": "B+", "urgency": "high", "location": "Nawabshah"}
    """
    if not text or not text.strip():
        return rule_based_analyze("")

    reply = ask_llm([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ])

    data = clean_json(reply) if reply else None

    if not data:
        return rule_based_analyze(text)

    group = str(data.get("blood_group", "")).upper().replace(" ", "")

    return {
        "blood_group": group if group in VALID_GROUPS else None,
        "urgency": str(data.get("urgency", "medium")).lower(),
        "location": data.get("location"),
        "patient_note": data.get("patient_note", text.strip()[:120]),
        "source": get_provider(),
    }


def generate_donor_message(donor_name, blood_group, urgency, hospital="the nearest hospital"):
    """The SMS or WhatsApp text sent to the donor."""
    prompt = (
        f"Write one short SMS (under 220 characters) asking {donor_name} to donate "
        f"{blood_group} blood. Urgency is {urgency}. Location is {hospital}. "
        "Be polite, calm and clear. No emojis. Return only the SMS text."
    )

    reply = ask_llm([{"role": "user", "content": prompt}])

    if reply and len(reply.strip()) > 20:
        return reply.strip().strip('"')

    speed = "urgently" if urgency == "high" else "soon"
    return (
        f"Assalam o Alaikum {donor_name}. A patient at {hospital} needs {blood_group} blood {speed}. "
        "If you are free and fit to donate, please reply YES. Thank you. BloodBridge AI"
    )


def explain_match(donor, patient_blood_group, urgency):
    """One line for the results screen."""
    prompt = (
        f"In one short sentence, tell a patient why donor {donor.get('name')} "
        f"with blood group {donor.get('blood_group')} at {donor.get('distance_km')} km "
        f"is a good match for a {patient_blood_group} request of {urgency} urgency. "
        "Do not give medical advice. Return only the sentence."
    )

    reply = ask_llm([{"role": "user", "content": prompt}])

    if reply and len(reply.strip()) > 15:
        return reply.strip().strip('"')

    return donor.get("reason", "Compatible donor, close by and available.")


if __name__ == "__main__":
    print("Provider:", get_provider())

    tests = [
        "My brother urgently needs B+ blood near Nawabshah",
        "Mujhe kal O negative blood chahiye Sakrand mein, koi jaldi nahi",
        "Accident case, AB positive khoon ki foran zarurat hai Daur mein",
    ]

    for line in tests:
        print(line)
        print("  ->", analyze_request(line))

    print(generate_donor_message("Ali Raza", "B+", "high", "Civil Hospital Nawabshah"))
