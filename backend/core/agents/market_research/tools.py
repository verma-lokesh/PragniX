from sqlalchemy.orm import Session
from repositories.market_signal_repository import MarketSignalRepository
from core.engines.market_entry.signal_analyzer import analyze_signals


def collect_signals(db: Session) -> list:
    repo = MarketSignalRepository(db)
    return db.query(repo.model).order_by(repo.model.signal_date.desc()).limit(20).all()


def filter_signals(signals: list, min_abs_impact: float = 0.2) -> list:
    return [s for s in signals if abs(s.impact_score) >= min_abs_impact]


def analyze(signals: list) -> dict:
    return analyze_signals(signals)
