import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from repositories.split_cargo_repository import SplitCargoRepository

router = APIRouter(prefix="/api/split-cargo", tags=["split-cargo"])


@router.get("/{decision_id}")
def get_split_cargo(decision_id: str, db: Session = Depends(get_db_session)):
    repo = SplitCargoRepository(db)
    rows = db.query(repo.model).filter_by(decision_request_id=decision_id).all()
    return [{
        "option_label": r.option_label,
        "vessel_composition": json.loads(r.vessel_composition),
        "total_cost": r.total_cost,
        "is_recommended": r.is_recommended,
    } for r in rows]
