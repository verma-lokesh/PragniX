from sqlalchemy.orm import Session
from repositories.risk_repository import RiskAssessmentRepository


def get_risks_for_decision(db: Session, decision_id: str) -> list:
    repo = RiskAssessmentRepository(db)
    return db.query(repo.model).filter_by(decision_request_id=decision_id).all()
