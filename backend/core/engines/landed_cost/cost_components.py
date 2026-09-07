def port_charges(cargo_quantity: float, port_name: str) -> float:
    per_ton = 3.5
    return round(cargo_quantity * per_ton, 2)


def insurance(freight_cost: float, cargo_value: float) -> float:
    return round((freight_cost + cargo_value) * 0.0035, 2)


def levies(cargo_quantity: float) -> float:
    return round(cargo_quantity * 0.8, 2)


def bunker_cost(distance_nm: float, vessel_class: str, bunker_price_usd_per_ton: float) -> float:
    consumption_per_day = {"Handysize": 18, "Supramax": 24, "Panamax": 30, "Capesize": 45}
    speed_knots = 12.5
    days = distance_nm / (speed_knots * 24)
    tons_consumed = days * consumption_per_day.get(vessel_class, 25)
    return round(tons_consumed * bunker_price_usd_per_ton, 2)
