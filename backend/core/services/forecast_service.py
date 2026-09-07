from sqlalchemy.orm import Session
from repositories.forecast_repository import FreightForecastRepository


def get_forecasts_for_decision(db: Session, decision_id: str) -> list:
    repo = FreightForecastRepository(db)
    return db.query(repo.model).filter_by(decision_request_id=decision_id).all()
