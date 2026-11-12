"""Shipping test suites, each built by following the named ISTQB technique mechanically.
Expected values are written by hand from the specification (not copied from the code)."""
import random

from harness import ShipCase
from oracle import expected_fee

VE = "ValueError"
N = 3.0  # nominal weight (band 2), nominal distance 20 km (local), non-member

# Equivalence partitioning: one representative per class, everything else nominal.
EP = [
    ShipCase(-3, 20, False, VE),        # weight <= 0
    ShipCase(0.5, 20, False, 5.0),      # (0,1]
    ShipCase(3, 20, False, 8.0),        # (1,5]
    ShipCase(10, 20, False, 15.0),      # (5,20]
    ShipCase(35, 20, False, 30.0),      # (20,50]
    ShipCase(60, 20, False, VE),        # weight > 50
    ShipCase(3, -10, False, VE),        # distance < 0
    ShipCase(3, 200, False, 12.0),      # regional
    ShipCase(3, 800, False, 18.0),      # national
    ShipCase(3, 20, True, 7.2),         # member
]

# Boundary value analysis: values on and just outside every boundary.
BVA = [
    ShipCase(0, 20, False, VE),
    ShipCase(0.01, 20, False, 5.0),
    ShipCase(1, 20, False, 5.0),
    ShipCase(1.01, 20, False, 8.0),
    ShipCase(5, 20, False, 8.0),
    ShipCase(5.01, 20, False, 15.0),
    ShipCase(20, 20, False, 15.0),
    ShipCase(20.01, 20, False, 30.0),
    ShipCase(50, 20, False, 30.0),
    ShipCase(50.01, 20, False, VE),
    ShipCase(3, -0.01, False, VE),
    ShipCase(3, 0, False, 8.0),
    ShipCase(3, 50, False, 8.0),
    ShipCase(3, 50.01, False, 12.0),
    ShipCase(3, 500, False, 12.0),
    ShipCase(3, 500.01, False, 18.0),
]

# Decision table: member (Y/N) x zone (local/regional/national), plus the two invalid-input rules.
DECISION_TABLE = [
    ShipCase(3, 20, False, 8.0),
    ShipCase(3, 200, False, 12.0),
    ShipCase(3, 800, False, 18.0),
    ShipCase(3, 20, True, 7.2),
    ShipCase(3, 200, True, 10.8),
    ShipCase(3, 800, True, 16.2),
    ShipCase(-1, 20, False, VE),
    ShipCase(3, -1, False, VE),
]

# Full combination: every weight band x every zone x member/non-member (4 x 3 x 2 = 24 cases).
_BAND_REPS = [0.5, 3, 10, 35]
_ZONE_REPS = [20, 200, 800]
FULL_COMBINATION = [
    ShipCase(w, d, m, expected_fee(w, d, m))
    for w in _BAND_REPS for d in _ZONE_REPS for m in (False, True)
]


def random_suite(n, seed):
    """n random inputs (weight -5..60, distance -20..700, member 50/50); oracle supplies expected."""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        w = rng.uniform(-5, 60)
        d = rng.uniform(-20, 700)
        m = rng.random() < 0.5
        out.append(ShipCase(w, d, m, expected_fee(w, d, m)))
    return out


TECHNIQUES = {
    "Equivalence partitioning": EP,
    "Boundary value analysis": BVA,
    "Decision table": DECISION_TABLE,
    "Full combination": FULL_COMBINATION,
    "EP + BVA + decision table": list(dict.fromkeys(EP + BVA + DECISION_TABLE)),
}
