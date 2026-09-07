from datetime import date
from sqlalchemy import String, Float, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class FreightForecast(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "freight_forecasts"

    decision_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_requests.id"))
    vessel_class: Mapped[str] = mapped_column(String(50))
    horizon_days: Mapped[int] = mapped_column()
    predicted_rate: Mapped[float] = mapped_column(Float)
    lower_bound: Mapped[float] = mapped_column(Float)
    upper_bound: Mapped[float] = mapped_column(Float)
    direction: Mapped[str] = mapped_column(String(20))
    confidence: Mapped[float] = mapped_column(Float)
    forecast_date: Mapped[date] = mapped_column(Date)
    model_name: Mapped[str] = mapped_column(String(100))
    model_version: Mapped[str] = mapped_column(String(50))
    model_type: Mapped[str] = mapped_column(String(20), default="fallback")

    decision_request: Mapped["DecisionRequest"] = relationship(back_populates="forecasts")
