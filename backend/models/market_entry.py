from datetime import date
from sqlalchemy import String, Float, ForeignKey, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class MarketEntry(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "market_entries"

    decision_request_id: Mapped[str] = mapped_column(String(36), ForeignKey("decision_requests.id"))
    recommended_action: Mapped[str] = mapped_column(String(20))
    ideal_entry_window_start: Mapped[date] = mapped_column(Date, nullable=True)
    ideal_entry_window_end: Mapped[date] = mapped_column(Date, nullable=True)
    expected_rate_change_pct: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)
    reasons: Mapped[str] = mapped_column(Text)

    decision_request: Mapped["DecisionRequest"] = relationship(back_populates="market_entries")
