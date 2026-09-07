from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from schemas.freight_forecast import ForecastOut
from schemas.recommendation import RecommendationOut
from schemas.risk_assessment import RiskOut
from schemas.market_entry import MarketEntryOut
from schemas.split_cargo import SplitCargoOut
from schemas.idle_vessel import IdleVesselOut
from schemas.decision_audit import DecisionAuditOut


class FeasibilityOut(BaseModel):
    feasible_vessels: List[str]
    infeasible_vessels: List[Dict[str, Any]]
    port_compatible: bool
    route_compatible: bool


class ExplanationFactor(BaseModel):
    factor: str
    impact: str
    direction: str
    explanation: str


class ExplanationOut(BaseModel):
    model_version: str
    data_timestamp: str
    factors: List[ExplanationFactor]
    confidence: float


class EngineStatusOut(BaseModel):
    engine: str
    state: str
    duration_ms: Optional[float] = None
    error: Optional[str] = None


class DecisionResponse(BaseModel):
    request_id: str
    status: str

    feasibility: Optional[FeasibilityOut] = None
    forecast: Optional[List[ForecastOut]] = None
    landed_cost: Optional[List[Dict[str, Any]]] = None
    recommendation: Optional[List[RecommendationOut]] = None
    market_entry: Optional[MarketEntryOut] = None
    risks: Optional[List[RiskOut]] = None
    split_cargo: Optional[SplitCargoOut] = None
    idle_vessel: Optional[List[IdleVesselOut]] = None
    simulation: Optional[Dict[str, Any]] = None
    explanation: Optional[ExplanationOut] = None
    audit: Optional[List[DecisionAuditOut]] = None

    engine_statuses: List[EngineStatusOut] = []
