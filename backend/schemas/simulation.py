from typing import Optional
from pydantic import BaseModel


class SimulationRequest(BaseModel):
    decision_id: str
    scenario_name: str
    freight_rate_pct_change: Optional[float] = None
    port_congestion_pct_change: Optional[float] = None
    bunker_price_pct_change: Optional[float] = None
    demand_pct_change: Optional[float] = None
    delivery_delay_days: Optional[float] = None


class SimulationOut(BaseModel):
    scenario_name: str
    baseline_cost: float
    scenario_cost: float
    cost_delta: float
    delay_impact_days: float
    risk_impact: str
    recommendation_impact: Optional[str] = None
