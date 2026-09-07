from core.engines.landed_cost.cost_components import port_charges, insurance, levies, bunker_cost
from utils.units import per_ton


def calculate_landed_cost(
    vessel_class: str,
    freight_rate_usd_per_ton: float,
    cargo_quantity: float,
    port_name: str,
    distance_nm: float,
    bunker_price: float,
    commodity_price_usd_per_ton: float,
) -> dict:
    freight_cost = round(freight_rate_usd_per_ton * cargo_quantity, 2)
    cargo_value = commodity_price_usd_per_ton * cargo_quantity
    charges = port_charges(cargo_quantity, port_name)
    ins = insurance(freight_cost, cargo_value)
    lev = levies(cargo_quantity)
    bunker = bunker_cost(distance_nm, vessel_class, bunker_price)
    other = round(freight_cost * 0.01, 2)

    total = round(freight_cost + charges + ins + lev + bunker + other, 2)

    return {
        "vessel_class": vessel_class,
        "freight_cost": freight_cost,
        "port_charges": charges,
        "insurance": ins,
        "levies": lev,
        "bunker_cost": bunker,
        "other_costs": other,
        "total_cost": total,
        "cost_per_ton": per_ton(total, cargo_quantity),
        "currency": "USD",
    }
