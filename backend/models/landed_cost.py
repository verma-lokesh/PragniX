from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class LandedCost(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "landed_costs"

    decision_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_requests.id"))
    vessel_class: Mapped[str] = mapped_column(String(50))
    freight_cost: Mapped[float] = mapped_column(Float)
    port_charges: Mapped[float] = mapped_column(Float)
    insurance: Mapped[float] = mapped_column(Float)
    levies: Mapped[float] = mapped_column(Float)
    bunker_cost: Mapped[float] = mapped_column(Float)
    other_costs: Mapped[float] = mapped_column(Float, default=0.0)
    total_cost: Mapped[float] = mapped_column(Float)
    cost_per_ton: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(10), default="USD")

    decision_request: Mapped["DecisionRequest"] = relationship(back_populates="landed_costs")
