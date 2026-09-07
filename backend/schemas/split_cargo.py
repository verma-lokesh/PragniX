from typing import Any
from pydantic import BaseModel


class SplitCargoOptionOut(BaseModel):
    option_label: str
    vessel_composition: list[dict[str, Any]]
    total_cost: float
    is_recommended: bool


class SplitCargoOut(BaseModel):
    options: list[SplitCargoOptionOut]
    recommended_option: str
