from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from core.services.forecast_service import get_forecasts_for_decision

router = APIRouter(prefix="/api/forecast", tags=["forecast"])


@router.get("/{decision_id}")
def get_forecast(decision_id: str, db: Session = Depends(get_db_session)):
    rows = get_forecasts_for_decision(db, decision_id)
    return [{
        "vessel_class": r.vessel_class, "horizon_days": r.horizon_days, "predicted_rate": r.predicted_rate,
        "lower_bound": r.lower_bound, "upper_bound": r.upper_bound, "direction": r.direction,
        "confidence": r.confidence, "model_version": r.model_version, "model_type": r.model_type,
    } for r in rows]
