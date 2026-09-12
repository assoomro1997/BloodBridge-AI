"""
BloodBridge AI - Shared Helpers
Owner: Anees

Small functions used by more than one module.
"""


def title_case_city(city):
    return str(city).strip().title()


def format_distance(km):
    try:
        return f"{float(km):.1f} km"
    except (TypeError, ValueError):
        return "unknown"


def short_list(items, limit=3):
    return items[:limit]
