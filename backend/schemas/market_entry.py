from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class MarketEntryOut(BaseModel):
    recommended_action: str
    ideal_entry_window_start: Optional[date] = None
    ideal_entry_window_end: Optional[date] = None
    expected_rate_change_pct: float
    confidence: float
    reasons: List[str]
    risk_factors: List[str] = []
