from datetime import date
from sqlalchemy import String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class FreightRate(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "freight_rates"

    vessel_class: Mapped[str] = mapped_column(String(50), index=True)
    origin: Mapped[str] = mapped_column(String(100), index=True)
    destination: Mapped[str] = mapped_column(String(100), index=True)
    rate_date: Mapped[date] = mapped_column(Date, index=True)
    rate_usd_per_ton: Mapped[float] = mapped_column(Float)
