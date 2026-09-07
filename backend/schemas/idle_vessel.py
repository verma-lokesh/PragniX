from pydantic import BaseModel


class IdleVesselOut(BaseModel):
    vessel_class: str
    idle_probability: float
    expected_idle_days: float
    deadhead_distance_nm: float
    recommended_action: str
    estimated_savings: float
