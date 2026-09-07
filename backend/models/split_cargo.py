from sqlalchemy import String, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class SplitCargo(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "split_cargos"

    decision_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_requests.id"))
    option_label: Mapped[str] = mapped_column(String(50))
    vessel_composition: Mapped[str] = mapped_column(Text)
    total_cost: Mapped[float] = mapped_column(Float)
    is_recommended: Mapped[bool] = mapped_column(Boolean, default=False)

    decision_request: Mapped["DecisionRequest"] = relationship(back_populates="split_cargos")
