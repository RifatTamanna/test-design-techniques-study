"""Seeded bugs ("mutants"). Each is the reference implementation with ONE deliberate defect.

BLIND PROTOCOL: if you write your own test suite for the study, write it from the specification
in sut/*.py BEFORE reading this file, otherwise the result is biased.
"""
from sut.order import REFERENCE_TRANSITIONS, make_order
from sut.shipping import make_shipping

SHIPPING_MUTANTS = {
    "S01": ("weight 0 is accepted (should be rejected)", dict(w_min_inclusive=True)),
    "S02": ("weight 50 is rejected (should be accepted)", dict(w_max_inclusive=False)),
    "S03": ("weight 1 is charged as band 2", dict(band_inclusive=(False, True, True))),
    "S04": ("weight 5 is charged as band 3", dict(band_inclusive=(True, False, True))),
    "S05": ("weight 20 is charged as band 4", dict(band_inclusive=(True, True, False))),
    "S06": ("band 3 base fee is 16 instead of 15", dict(base_fees=(5.0, 8.0, 16.0, 30.0))),
    "S07": ("distance 50 is charged as regional", dict(zone_inclusive=(False, True))),
    "S08": ("distance 500 is charged as national", dict(zone_inclusive=(True, False))),
    "S09": ("national surcharge is 9 instead of 10", dict(surcharges=(0.0, 4.0, 9.0))),
    "S10": ("member discount is 15% instead of 10%", dict(discount=0.15)),
    "S11": ("member discount applied to base fee only", dict(discount_on="base")),
    "S12": ("negative distance is accepted", dict(check_negative_distance=False)),
    "S13": ("members get no discount in the national zone", dict(no_discount_zone=2)),
    "S14": ("members get no discount in the heaviest band", dict(no_discount_band=3)),
}


def _with(add=None, remove=None, change=None):
    t = dict(REFERENCE_TRANSITIONS)
    for k, v in (add or {}).items():
        t[k] = v
    for k in remove or []:
        del t[k]
    for k, v in (change or {}).items():
        t[k] = v
    return t


ORDER_MUTANTS = {
    "O01": ("cancel allowed from SHIPPED", _with(add={("cancel", "SHIPPED"): "CANCELLED"})),
    "O02": ("ship allowed from NEW (skips payment)", _with(add={("ship", "NEW"): "SHIPPED"})),
    "O03": ("pay allowed twice", _with(add={("pay", "PAID"): "PAID"})),
    "O04": ("deliver allowed from PAID (skips shipping)", _with(add={("deliver", "PAID"): "DELIVERED"})),
    "O05": ("cancel NOT allowed from PAID (valid transition missing)", _with(remove=[("cancel", "PAID")])),
    "O06": ("cancel allowed from DELIVERED", _with(add={("cancel", "DELIVERED"): "CANCELLED"})),
    "O07": ("pay leads to SHIPPED instead of PAID", _with(change={("pay", "NEW"): "SHIPPED"})),
    "O08": ("ship allowed from CANCELLED", _with(add={("ship", "CANCELLED"): "SHIPPED"})),
    "O09": ("pay allowed from CANCELLED", _with(add={("pay", "CANCELLED"): "PAID"})),
    "O10": ("cancel allowed from CANCELLED", _with(add={("cancel", "CANCELLED"): "CANCELLED"})),
}


def shipping_impls():
    return {k: make_shipping(**ov) for k, (_, ov) in SHIPPING_MUTANTS.items()}


def order_impls():
    return {k: make_order(t) for k, (_, t) in ORDER_MUTANTS.items()}
