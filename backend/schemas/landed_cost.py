from pydantic import BaseModel


class LandedCostOut(BaseModel):
    vessel_class: str
    freight_cost: float
    port_charges: float
    insurance: float
    levies: float
    bunker_cost: float
    other_costs: float
    total_cost: float
    cost_per_ton: float
    currency: str
