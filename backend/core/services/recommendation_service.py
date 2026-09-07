from sqlalchemy.orm import Session
from repositories.recommendation_repository import RecommendationRepository


def get_recommendations_for_decision(db: Session, decision_id: str) -> list:
    repo = RecommendationRepository(db)
    return (
        db.query(repo.model)
        .filter_by(decision_request_id=decision_id)
        .order_by(repo.model.rank.asc())
        .all()
    )
