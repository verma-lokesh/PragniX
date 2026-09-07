from datetime import date
from sqlalchemy import String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class PortCongestion(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "port_congestions"

    port_name: Mapped[str] = mapped_column(String(100), index=True)
    observed_date: Mapped[date] = mapped_column(Date)
    congestion_index: Mapped[float] = mapped_column(Float)
    avg_wait_days: Mapped[float] = mapped_column(Float, default=0.0)
