from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from repositories.idle_vessel_repository import IdleVesselRepository

router = APIRouter(prefix="/api/idle-vessel", tags=["idle-vessel"])


@router.get("/{decision_id}")
def get_idle_vessel(decision_id: str, db: Session = Depends(get_db_session)):
    repo = IdleVesselRepository(db)
    rows = db.query(repo.model).filter_by(decision_request_id=decision_id).all()
    return [{
        "vessel_class": r.vessel_class, "idle_probability": r.idle_probability,
        "expected_idle_days": r.expected_idle_days, "deadhead_distance_nm": r.deadhead_distance_nm,
        "recommended_action": r.recommended_action, "estimated_savings": r.estimated_savings,
    } for r in rows]
