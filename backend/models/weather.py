from datetime import date
from sqlalchemy import String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class Weather(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "weather_records"

    region: Mapped[str] = mapped_column(String(100), index=True)
    observed_date: Mapped[date] = mapped_column(Date)
    cyclone_risk_index: Mapped[float] = mapped_column(Float, default=0.0)
    rough_sea_index: Mapped[float] = mapped_column(Float, default=0.0)
