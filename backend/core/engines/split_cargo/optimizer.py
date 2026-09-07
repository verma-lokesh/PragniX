import math
from config.constants import VESSEL_SPECS


def build_single_vessel_option(vessel_class: str, cargo_quantity: float, cost_per_ton: float) -> dict:
    return {
        "option_label": "Option A - Single Vessel",
        "vessel_composition": [{"vessel_class": vessel_class, "count": 1, "quantity_tons": cargo_quantity}],
        "total_cost": round(cost_per_ton * cargo_quantity, 2),
    }


def build_multi_vessel_option(vessel_class: str, cargo_quantity: float, cost_per_ton_multi: float) -> dict:
    capacity = VESSEL_SPECS[vessel_class]["dwt"] * 0.9
    count = max(2, math.ceil(cargo_quantity / capacity))
    per_vessel_qty = round(cargo_quantity / count, 1)
    return {
        "option_label": "Option B - Split Cargo",
        "vessel_composition": [{"vessel_class": vessel_class, "count": count, "quantity_tons": per_vessel_qty}],
        "total_cost": round(cost_per_ton_multi * cargo_quantity, 2),
    }
