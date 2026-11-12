"""An independent, deliberately simple oracle for the shipping spec (a lookup table, no loops).
Used for the full-combination and random suites, and cross-checked against the reference in tests."""

BASE = {0: 5.0, 1: 8.0, 2: 15.0, 3: 30.0}
SURCHARGE = {0: 0.0, 1: 4.0, 2: 10.0}


def band_of(w):
    if w <= 1:
        return 0
    if w <= 5:
        return 1
    if w <= 20:
        return 2
    return 3


def zone_of(d):
    if d <= 50:
        return 0
    if d <= 500:
        return 1
    return 2


def expected_fee(w, d, member):
    """Return the expected fee, or the string 'ValueError' for invalid input."""
    if not (0 < w <= 50) or d < 0:
        return "ValueError"
    total = BASE[band_of(w)] + SURCHARGE[zone_of(d)]
    if member:
        total *= 0.9
    return round(total, 2)
