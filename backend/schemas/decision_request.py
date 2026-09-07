from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class DecisionRequestCreate(BaseModel):
    commodity: str
    cargo_quantity: float = Field(gt=0)
    origin: str
    destination: str
    earliest_loading_date: date
    latest_delivery_date: date
    contract_preference: str = "AUTO"
    contract_duration_days: Optional[int] = None
    expected_voyages: Optional[int] = None
    preferred_vessel_type: Optional[str] = None
    target_freight_rate: Optional[float] = None
    max_budget: Optional[float] = None
    currency: str = "USD"
    notes: Optional[str] = None

    @field_validator("latest_delivery_date")
    @classmethod
    def delivery_after_loading(cls, v, info):
        loading = info.data.get("earliest_loading_date")
        if loading and v < loading:
            raise ValueError("latest_delivery_date must be >= earliest_loading_date")
        return v

    @field_validator("destination")
    @classmethod
    def origin_diff_destination(cls, v, info):
        origin = info.data.get("origin")
        if origin and v.strip().lower() == origin.strip().lower():
            raise ValueError("origin and destination must differ")
        return v


class DecisionRequestOut(DecisionRequestCreate):
    id: str
    status: str
