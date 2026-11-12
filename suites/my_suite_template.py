"""YOUR OWN suite (the human condition in the study).

1. Copy this file to suites/my_suite.py
2. Write cases from the SPECIFICATION in sut/shipping.py and sut/order.py.
   Do NOT read mutants.py first; otherwise the comparison is biased.
3. Run: python run_study.py   (a row called "Your suite" appears in the results)
"""
from harness import OrderCase, ShipCase

# ShipCase(weight, distance, member, expected)  -> expected is a number or "ValueError"
SHIPPING_CASES = [
    ShipCase(3, 20, False, 8.0),   # example row: replace with your own cases
]

# OrderCase(prefix_events, event, expected)     -> expected is a state name or "INVALID"
ORDER_CASES = [
    OrderCase((), "pay", "PAID"),  # example row: replace with your own cases
]
