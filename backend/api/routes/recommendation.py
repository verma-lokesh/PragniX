from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from core.services.recommendation_service import get_recommendations_for_decision

router = APIRouter(prefix="/api/recommendation", tags=["recommendation"])


@router.get("/{decision_id}")
def get_recommendation(decision_id: str, db: Session = Depends(get_db_session)):
    rows = get_recommendations_for_decision(db, decision_id)
    return [{
        "vessel_class": r.vessel_class, "charter_strategy": r.charter_strategy, "rank": r.rank,
        "score": r.score, "is_feasible": r.is_feasible, "rejection_reason": r.rejection_reason,
    } for r in rows]
