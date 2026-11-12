"""Order lifecycle: system under test #2 (a state machine).

SPECIFICATION
  States: NEW, PAID, SHIPPED, DELIVERED, CANCELLED   (an order starts in NEW)
  Events: pay, ship, deliver, cancel
  The ONLY valid transitions are:
      pay     NEW     -> PAID
      ship    PAID    -> SHIPPED
      deliver SHIPPED -> DELIVERED
      cancel  NEW     -> CANCELLED
      cancel  PAID    -> CANCELLED
  Any other (event, state) pair must raise InvalidTransition and leave the state unchanged.
"""


class InvalidTransition(Exception):
    pass


STATES = ["NEW", "PAID", "SHIPPED", "DELIVERED", "CANCELLED"]
EVENTS = ["pay", "ship", "deliver", "cancel"]

REFERENCE_TRANSITIONS = {
    ("pay", "NEW"): "PAID",
    ("ship", "PAID"): "SHIPPED",
    ("deliver", "SHIPPED"): "DELIVERED",
    ("cancel", "NEW"): "CANCELLED",
    ("cancel", "PAID"): "CANCELLED",
}

# The shortest event sequence that reaches each state from NEW.
PATH_TO = {
    "NEW": (),
    "PAID": ("pay",),
    "SHIPPED": ("pay", "ship"),
    "DELIVERED": ("pay", "ship", "deliver"),
    "CANCELLED": ("cancel",),
}


def make_order(transitions=None):
    """Build an Order class from a transition table (the reference table by default)."""
    table = dict(REFERENCE_TRANSITIONS if transitions is None else transitions)

    class Order:
        def __init__(self):
            self.state = "NEW"

        def apply(self, event):
            key = (event, self.state)
            if key not in table:
                raise InvalidTransition(f"{event} not allowed in {self.state}")
            self.state = table[key]

    return Order
