from models.risk_assessment import RiskAssessment
from repositories.base import BaseRepository


class RiskAssessmentRepository(BaseRepository[RiskAssessment]):
    model = RiskAssessment
