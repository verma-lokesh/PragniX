from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from core.services.risk_service import get_risks_for_decision

router = APIRouter(prefix="/api/risk", tags=["risk"])


@router.get("/{decision_id}")
def get_risk(decision_id: str, db: Session = Depends(get_db_session)):
    rows = get_risks_for_decision(db, decision_id)
    return [{
        "risk_type": r.risk_type, "risk_level": r.risk_level, "probability": r.probability,
        "impact": r.impact, "score": r.score, "description": r.description, "mitigation": r.mitigation,
    } for r in rows]
