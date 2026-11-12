"""Sanity checks that keep the experiment honest. Run with: pytest"""
import itertools

import pytest

from harness import passes_order, passes_ship, suite_kills
from mutants import ORDER_MUTANTS, SHIPPING_MUTANTS, order_impls, shipping_impls
from oracle import expected_fee
from sut.order import EVENTS, PATH_TO, STATES, InvalidTransition, make_order
from sut.shipping import make_shipping
from suites import order_suites, shipping_suites

WEIGHTS = [-1, 0, 0.001, 0.5, 1, 1.01, 3, 5, 5.01, 10, 20, 20.01, 35, 50, 50.01, 100]
DISTANCES = [-1, -0.01, 0, 10, 50, 50.01, 100, 500, 500.01, 1000]


def outcome(fn, *args):
    try:
        return ("ok", fn(*args))
    except ValueError:
        return ("ValueError",)


def test_oracle_matches_reference_on_grid():
    ref = make_shipping()
    for w, d, m in itertools.product(WEIGHTS, DISTANCES, (False, True)):
        exp = expected_fee(w, d, m)
        got = outcome(ref, w, d, m)
        assert (got == ("ValueError",)) == (exp == "ValueError"), (w, d, m)
        if exp != "ValueError":
            assert abs(got[1] - exp) < 0.005, (w, d, m)


@pytest.mark.parametrize("suite_name", list(shipping_suites.TECHNIQUES))
def test_shipping_suites_pass_on_reference(suite_name):
    ref = make_shipping()
    assert not suite_kills(shipping_suites.TECHNIQUES[suite_name], ref, passes_ship)


@pytest.mark.parametrize("suite_name", list(order_suites.TECHNIQUES))
def test_order_suites_pass_on_reference(suite_name):
    ref = make_order()
    assert not suite_kills(order_suites.TECHNIQUES[suite_name], ref, passes_order)


def test_random_suites_pass_on_reference():
    assert not suite_kills(shipping_suites.random_suite(200, 1), make_shipping(), passes_ship)
    assert not suite_kills(order_suites.random_suite(50, 1), make_order(), passes_order)


@pytest.mark.parametrize("mid", list(SHIPPING_MUTANTS))
def test_shipping_mutant_is_not_equivalent(mid):
    """Every shipping mutant must behave differently from the reference somewhere on the grid."""
    ref, mut = make_shipping(), shipping_impls()[mid]
    for w, d, m in itertools.product(WEIGHTS, DISTANCES, (False, True)):
        a, b = outcome(ref, w, d, m), outcome(mut, w, d, m)
        if a[0] != b[0] or (a[0] == "ok" and abs(a[1] - b[1]) > 0.005):
            return
    pytest.fail(f"{mid} behaves like the reference: it can never be killed")


@pytest.mark.parametrize("mid", list(ORDER_MUTANTS))
def test_order_mutant_is_not_equivalent(mid):
    ref_cls, mut_cls = make_order(), order_impls()[mid]
    for s, e in itertools.product(STATES, EVENTS):
        def run(cls):
            o = cls()
            for ev in PATH_TO[s]:
                o.apply(ev)
            try:
                o.apply(e)
                return ("ok", o.state)
            except InvalidTransition:
                return ("invalid", o.state)
        if run(ref_cls) != run(mut_cls):
            return
    pytest.fail(f"{mid} behaves like the reference")
