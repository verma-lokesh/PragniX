from datetime import date
from sqlalchemy import String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class MarketSignal(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "market_signals"

    signal_date: Mapped[date] = mapped_column(Date)
    category: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    sentiment_score: Mapped[float] = mapped_column(Float, default=0.0)
    impact_score: Mapped[float] = mapped_column(Float, default=0.0)
