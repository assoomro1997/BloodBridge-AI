"""
BloodBridge AI - Pakistan Geography
Owner: Anees

City coordinates and real distance between two cities.
Used to turn a local donor distance into a national one.
"""

from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371

# Major cities across all four provinces, AJK, Gilgit-Baltistan and the capital.
PAKISTAN_CITIES = {
    # Sindh
    "Karachi": (24.8607, 67.0011),
    "Hyderabad": (25.3960, 68.3578),
    "Sukkur": (27.7052, 68.8574),
    "Larkana": (27.5590, 68.2120),
    "Nawabshah": (26.2442, 68.4100),
    "Khairpur": (27.5295, 68.7592),
    "Mirpur Khas": (25.5276, 69.0122),
    "Jacobabad": (28.2769, 68.4514),
    "Shikarpur": (27.9556, 68.6382),
    "Dadu": (26.7300, 67.7767),

    # Punjab
    "Lahore": (31.5204, 74.3587),
    "Faisalabad": (31.4504, 73.1350),
    "Rawalpindi": (33.5651, 73.0169),
    "Multan": (30.1575, 71.5249),
    "Gujranwala": (32.1877, 74.1945),
    "Sialkot": (32.4945, 74.5229),
    "Bahawalpur": (29.3956, 71.6836),
    "Sargodha": (32.0836, 72.6711),
    "Sahiwal": (30.6682, 73.1114),
    "Rahim Yar Khan": (28.4212, 70.2989),
    "Dera Ghazi Khan": (30.0489, 70.6455),
    "Gujrat": (32.5740, 74.0789),
    "Jhang": (31.2781, 72.3317),
    "Sheikhupura": (31.7131, 73.9783),
    "Kasur": (31.1187, 74.4507),
    "Okara": (30.8138, 73.4534),
    "Chiniot": (31.7167, 72.9833),
    "Wah Cantt": (33.7715, 72.7495),
    "Attock": (33.7660, 72.3600),

    # Khyber Pakhtunkhwa
    "Peshawar": (34.0151, 71.5249),
    "Mardan": (34.1989, 72.0231),
    "Abbottabad": (34.1688, 73.2215),
    "Kohat": (33.5869, 71.4414),
    "Nowshera": (34.0153, 71.9747),
    "Dera Ismail Khan": (31.8313, 70.9017),
    "Mingora": (34.7795, 72.3614),
    "Chitral": (35.8518, 71.7864),

    # Balochistan
    "Quetta": (30.1798, 66.9750),
    "Turbat": (26.0023, 63.0450),
    "Gwadar": (25.1264, 62.3225),
    "Khuzdar": (27.8120, 66.6100),
    "Sibi": (29.5430, 67.8773),

    # Capital, AJK and Gilgit-Baltistan
    "Islamabad": (33.6844, 73.0479),
    "Muzaffarabad": (34.3700, 73.4711),
    "Mirpur AJK": (33.1478, 73.7519),
    "Gilgit": (35.9208, 74.3144),
    "Skardu": (35.2971, 75.6333),
}

CITY_NAMES = sorted(PAKISTAN_CITIES.keys())


def find_city(name):
    """Match a city name loosely. Returns the official name or None."""
    if not name:
        return None

    target = str(name).strip().lower()

    for city in PAKISTAN_CITIES:
        if city.lower() == target:
            return city

    for city in PAKISTAN_CITIES:
        if target in city.lower() or city.lower() in target:
            return city

    return None


def haversine(lat1, lon1, lat2, lon2):
    """Straight line distance in km between two points on earth."""
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return round(2 * EARTH_RADIUS_KM * asin(sqrt(a)), 1)


def city_distance(city_a, city_b):
    """
    Distance in km between two Pakistani cities.
    Returns None if either city is unknown.
    """
    a = find_city(city_a)
    b = find_city(city_b)

    if not a or not b:
        return None

    if a == b:
        return 0.0

    lat1, lon1 = PAKISTAN_CITIES[a]
    lat2, lon2 = PAKISTAN_CITIES[b]
    return haversine(lat1, lon1, lat2, lon2)


if __name__ == "__main__":
    print("Cities loaded:", len(PAKISTAN_CITIES))
    for pair in [("Karachi", "Lahore"), ("Nawabshah", "Hyderabad"),
                 ("Islamabad", "Peshawar"), ("Quetta", "Gwadar")]:
        print(f"{pair[0]} to {pair[1]}: {city_distance(*pair)} km")
