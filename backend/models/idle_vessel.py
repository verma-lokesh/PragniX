from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class IdleVessel(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "idle_vessels"

    decision_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_requests.id"))
    vessel_class: Mapped[str] = mapped_column(String(50))
    idle_probability: Mapped[float] = mapped_column(Float)
    expected_idle_days: Mapped[float] = mapped_column(Float)
    deadhead_distance_nm: Mapped[float] = mapped_column(Float)
    recommended_action: Mapped[str] = mapped_column(String(50))
    estimated_savings: Mapped[float] = mapped_column(Float)

    decision_request: Mapped["DecisionRequest"] = relationship(back_populates="idle_vessels")
