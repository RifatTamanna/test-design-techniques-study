"""Test cases and the code that decides whether a case passes against an implementation."""
from dataclasses import dataclass
from typing import Tuple, Union

from sut.order import InvalidTransition


@dataclass(frozen=True)
class ShipCase:
    weight: float
    distance: float
    member: bool
    expected: Union[float, str]  # a number, or the string "ValueError"


@dataclass(frozen=True)
class OrderCase:
    prefix: Tuple[str, ...]  # events applied first to reach a state
    event: str               # the event under test
    expected: str            # resulting state, or "INVALID" (must raise and keep the state)


def passes_ship(impl, c):
    try:
        got = impl(c.weight, c.distance, c.member)
    except ValueError:
        return c.expected == "ValueError"
    except Exception:
        return False
    if isinstance(c.expected, str):
        return False
    return abs(got - c.expected) < 0.005


def passes_order(order_cls, c):
    o = order_cls()
    try:
        for e in c.prefix:
            o.apply(e)
    except Exception:
        return False
    before = o.state
    try:
        o.apply(c.event)
    except InvalidTransition:
        return c.expected == "INVALID" and o.state == before
    except Exception:
        return False
    return c.expected != "INVALID" and o.state == c.expected


def suite_kills(cases, impl, passes):
    """A suite 'kills' an implementation if at least one case fails on it."""
    return any(not passes(impl, c) for c in cases)
