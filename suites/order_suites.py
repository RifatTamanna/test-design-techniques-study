"""Order state-machine suites built from state-transition testing."""
import random

from harness import OrderCase
from sut.order import EVENTS, PATH_TO, REFERENCE_TRANSITIONS, STATES


def _case(state, event):
    target = REFERENCE_TRANSITIONS.get((event, state), "INVALID")
    return OrderCase(PATH_TO[state], event, target)


# 0-switch coverage: every VALID transition once (5 cases).
VALID_TRANSITIONS = [_case(s, e) for (e, s) in REFERENCE_TRANSITIONS]

# Every INVALID (state, event) pair once (15 cases).
INVALID_TRANSITIONS = [_case(s, e) for s in STATES for e in EVENTS if (e, s) not in REFERENCE_TRANSITIONS]

# Every state x event pair (20 cases): the full state/event table.
ALL_PAIRS = [_case(s, e) for s in STATES for e in EVENTS]


def random_suite(n, seed):
    """n random (state, event) pairs sampled with replacement from the 20 possible pairs."""
    rng = random.Random(seed)
    return [_case(rng.choice(STATES), rng.choice(EVENTS)) for _ in range(n)]


TECHNIQUES = {
    "Valid transitions only": VALID_TRANSITIONS,
    "Invalid transitions only": INVALID_TRANSITIONS,
    "All state/event pairs": ALL_PAIRS,
}
