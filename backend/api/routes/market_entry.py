from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from repositories.market_entry_repository import MarketEntryRepository

router = APIRouter(prefix="/api/market-entry", tags=["market-entry"])


@router.get("/{decision_id}")
def get_market_entry(decision_id: str, db: Session = Depends(get_db_session)):
    repo = MarketEntryRepository(db)
    row = db.query(repo.model).filter_by(decision_request_id=decision_id).first()
    if not row:
        return None
    return {
        "recommended_action": row.recommended_action,
        "ideal_entry_window_start": row.ideal_entry_window_start,
        "ideal_entry_window_end": row.ideal_entry_window_end,
        "expected_rate_change_pct": row.expected_rate_change_pct,
        "confidence": row.confidence,
        "reasons": row.reasons.split("; ") if row.reasons else [],
    }
