from sqlalchemy import String, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class RiskAssessment(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "risk_assessments"

    decision_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_requests.id"))
    risk_type: Mapped[str] = mapped_column(String(50))
    risk_level: Mapped[str] = mapped_column(String(20))
    probability: Mapped[float] = mapped_column(Float)
    impact: Mapped[float] = mapped_column(Float)
    score: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)
    mitigation: Mapped[str] = mapped_column(Text)

    decision_request: Mapped["DecisionRequest"] = relationship(back_populates="risks")
