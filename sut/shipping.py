"""Shipping fee calculator: system under test #1.

SPECIFICATION  shipping_fee(weight_kg, distance_km, is_member=False)
  1. weight must satisfy 0 < weight <= 50, otherwise raise ValueError.
  2. distance must be >= 0, otherwise raise ValueError.
  3. Base fee by weight:   (0,1] -> 5   (1,5] -> 8   (5,20] -> 15   (20,50] -> 30
  4. Zone surcharge:       [0,50] -> 0  (50,500] -> 4   above 500 -> 10
  5. total = base + surcharge
  6. Members get 10% off the total.
  7. The result is rounded to 2 decimals.
"""

DEFAULTS = dict(
    w_min_inclusive=False,
    w_max_inclusive=True,
    band_limits=(1, 5, 20),
    band_inclusive=(True, True, True),
    base_fees=(5.0, 8.0, 15.0, 30.0),
    zone_limits=(50, 500),
    zone_inclusive=(True, True),
    surcharges=(0.0, 4.0, 10.0),
    discount=0.10,
    discount_on="total",
    check_negative_distance=True,
    no_discount_zone=None,
    no_discount_band=None,
)


def make_shipping(**overrides):
    """Reference implementation when called with no overrides; a mutant otherwise."""
    cfg = {**DEFAULTS, **overrides}

    def shipping_fee(weight_kg, distance_km, is_member=False):
        lo_ok = weight_kg >= 0 if cfg["w_min_inclusive"] else weight_kg > 0
        hi_ok = weight_kg <= 50 if cfg["w_max_inclusive"] else weight_kg < 50
        if not (lo_ok and hi_ok):
            raise ValueError("weight out of range")
        if cfg["check_negative_distance"] and distance_km < 0:
            raise ValueError("distance out of range")

        band = 3
        for i, (lim, inc) in enumerate(zip(cfg["band_limits"], cfg["band_inclusive"])):
            if weight_kg < lim or (inc and weight_kg == lim):
                band = i
                break
        zone = 2
        for i, (lim, inc) in enumerate(zip(cfg["zone_limits"], cfg["zone_inclusive"])):
            if distance_km < lim or (inc and distance_km == lim):
                zone = i
                break

        base = cfg["base_fees"][band]
        surcharge = cfg["surcharges"][zone]
        total = base + surcharge
        if is_member and not (cfg["no_discount_zone"] == zone or cfg["no_discount_band"] == band):
            if cfg["discount_on"] == "total":
                total = total * (1 - cfg["discount"])
            else:  # bug variant: discount applied to the base fee only
                total = base * (1 - cfg["discount"]) + surcharge
        return round(total, 2)

    return shipping_fee
