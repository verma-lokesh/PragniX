from sqlalchemy import String, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class DecisionAudit(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "decision_audits"

    decision_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_requests.id"))
    execution_id: Mapped[str] = mapped_column(String(36))
    engine: Mapped[str] = mapped_column(String(50))
    input_summary: Mapped[str] = mapped_column(Text)
    output_summary: Mapped[str] = mapped_column(Text)
    model_version: Mapped[str] = mapped_column(String(50), nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=True)
    decision: Mapped[str] = mapped_column(Text, nullable=True)
    explanation: Mapped[str] = mapped_column(Text, nullable=True)

    decision_request: Mapped["DecisionRequest"] = relationship(back_populates="audits")
