from sqlalchemy import String, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class Simulation(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "simulations"

    decision_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_requests.id"))
    scenario_name: Mapped[str] = mapped_column(String(100))
    scenario_params: Mapped[str] = mapped_column(Text)
    baseline_cost: Mapped[float] = mapped_column(Float)
    scenario_cost: Mapped[float] = mapped_column(Float)
    cost_delta: Mapped[float] = mapped_column(Float)
    delay_impact_days: Mapped[float] = mapped_column(Float, default=0.0)
    risk_impact: Mapped[str] = mapped_column(String(20), default="LOW")
    recommendation_impact: Mapped[str] = mapped_column(Text, nullable=True)

    decision_request: Mapped["DecisionRequest"] = relationship(back_populates="simulations")
