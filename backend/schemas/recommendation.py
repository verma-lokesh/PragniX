from typing import Optional
from pydantic import BaseModel
from schemas.landed_cost import LandedCostOut


class RecommendationOut(BaseModel):
    vessel_class: str
    origin_port: str
    destination_port: str
    charter_strategy: str
    rank: int
    score: float
    is_feasible: bool
    rejection_reason: Optional[str] = None
    landed_cost: Optional[LandedCostOut] = None
