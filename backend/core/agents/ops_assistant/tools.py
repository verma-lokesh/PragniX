from sqlalchemy.orm import Session
from repositories.decision_request_repository import DecisionRequestRepository
from core.services.forecast_service import get_forecasts_for_decision
from core.services.recommendation_service import get_recommendations_for_decision
from core.services.risk_service import get_risks_for_decision
from repositories.landed_cost_repository import LandedCostRepository
from repositories.market_entry_repository import MarketEntryRepository
from core.services.simulation_service import run_simulation
from schemas.simulation import SimulationRequest


def get_decision_status(db: Session, decision_id: str) -> dict:
    repo = DecisionRequestRepository(db)
    dr = repo.get(decision_id)
    if not dr:
        return {"error": f"Decision {decision_id} not found."}
    return {"decision_id": dr.id, "status": dr.status}


def get_forecast(db: Session, decision_id: str) -> list:
    return [{
        "vessel_class": f.vessel_class, "predicted_rate": f.predicted_rate,
        "direction": f.direction, "confidence": f.confidence,
    } for f in get_forecasts_for_decision(db, decision_id)]


def get_recommendation(db: Session, decision_id: str) -> list:
    recs = get_recommendations_for_decision(db, decision_id)
    return [{
        "vessel_class": r.vessel_class, "rank": r.rank, "score": r.score,
        "is_feasible": r.is_feasible, "rejection_reason": r.rejection_reason,
        "charter_strategy": r.charter_strategy,
    } for r in recs]


def get_risk(db: Session, decision_id: str) -> list:
    return [{
        "risk_type": r.risk_type, "risk_level": r.risk_level, "description": r.description,
    } for r in get_risks_for_decision(db, decision_id)]


def get_landed_cost(db: Session, decision_id: str) -> list:
    repo = LandedCostRepository(db)
    rows = db.query(repo.model).filter_by(decision_request_id=decision_id).all()
    return [{"vessel_class": r.vessel_class, "total_cost": r.total_cost, "cost_per_ton": r.cost_per_ton} for r in rows]


def get_market_entry(db: Session, decision_id: str) -> dict | None:
    repo = MarketEntryRepository(db)
    row = db.query(repo.model).filter_by(decision_request_id=decision_id).first()
    if not row:
        return None
    return {
        "recommended_action": row.recommended_action,
        "confidence": row.confidence,
        "reasons": row.reasons.split("; ") if row.reasons else [],
    }


def run_what_if(db: Session, decision_id: str, freight_rate_pct_change: float = 0.0) -> dict:
    req = SimulationRequest(decision_id=decision_id, scenario_name="assistant_query", freight_rate_pct_change=freight_rate_pct_change)
    return run_simulation(db, req)


TOOLS = {
    "get_decision_status": get_decision_status,
    "get_forecast": get_forecast,
    "get_recommendation": get_recommendation,
    "get_risk": get_risk,
    "get_landed_cost": get_landed_cost,
    "get_market_entry": get_market_entry,
    "run_simulation": run_what_if,
}
