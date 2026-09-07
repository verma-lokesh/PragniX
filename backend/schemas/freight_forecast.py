from datetime import date
from pydantic import BaseModel


class ForecastOut(BaseModel):
    vessel_class: str
    horizon_days: int
    predicted_rate: float
    lower_bound: float
    upper_bound: float
    direction: str
    confidence: float
    forecast_date: date
    model_name: str
    model_version: str
    model_type: str
