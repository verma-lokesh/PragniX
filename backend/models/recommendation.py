from sqlalchemy import String, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class Recommendation(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "recommendations"

    decision_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_requests.id"))
    landed_cost_id: Mapped[str] = mapped_column(String(36), ForeignKey("landed_costs.id"), nullable=True)
    vessel_class: Mapped[str] = mapped_column(String(50))
    origin_port: Mapped[str] = mapped_column(String(100))
    destination_port: Mapped[str] = mapped_column(String(100))
    route_id: Mapped[str] = mapped_column(String(36), ForeignKey("routes.id"), nullable=True)
    charter_strategy: Mapped[str] = mapped_column(String(30))
    rank: Mapped[int] = mapped_column()
    score: Mapped[float] = mapped_column(Float)
    is_feasible: Mapped[bool] = mapped_column(Boolean, default=True)
    rejection_reason: Mapped[str] = mapped_column(String(500), nullable=True)

    decision_request: Mapped["DecisionRequest"] = relationship(back_populates="recommendations")
