from pydantic import BaseModel


class RiskOut(BaseModel):
    risk_type: str
    risk_level: str
    probability: float
    impact: float
    score: float
    description: str
    mitigation: str
