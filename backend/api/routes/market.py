from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from repositories.market_signal_repository import MarketSignalRepository
from core.engines.market_entry.signal_analyzer import analyze_signals

router = APIRouter(prefix="/api/market", tags=["market"])


@router.get("/brief")
def market_brief(db: Session = Depends(get_db_session)):
    repo = MarketSignalRepository(db)
    signals = db.query(repo.model).order_by(repo.model.signal_date.desc()).limit(10).all()
    summary = analyze_signals(signals)
    return {
        "avg_sentiment": summary["avg_sentiment"],
        "avg_impact": summary["avg_impact"],
        "notable_signals": summary["notable"],
        "signal_count": len(signals),
    }


@router.get("/signals")
def market_signals(db: Session = Depends(get_db_session)):
    repo = MarketSignalRepository(db)
    rows = db.query(repo.model).order_by(repo.model.signal_date.desc()).limit(50).all()
    return [{
        "signal_date": r.signal_date, "category": r.category, "description": r.description,
        "sentiment_score": r.sentiment_score, "impact_score": r.impact_score,
    } for r in rows]
