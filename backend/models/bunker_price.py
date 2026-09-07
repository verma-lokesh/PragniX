from datetime import date
from sqlalchemy import String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class BunkerPrice(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "bunker_prices"

    port_name: Mapped[str] = mapped_column(String(100), index=True)
    price_date: Mapped[date] = mapped_column(Date)
    price_usd_per_ton: Mapped[float] = mapped_column(Float)
