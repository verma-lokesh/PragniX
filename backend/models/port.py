from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class Port(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "ports"

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    country: Mapped[str] = mapped_column(String(100))
    max_draft: Mapped[float] = mapped_column(Float)
    max_loa: Mapped[float] = mapped_column(Float)
    max_beam: Mapped[float] = mapped_column(Float)
    berth_count: Mapped[int] = mapped_column(default=1)
    cargo_handling_rate_tons_per_day: Mapped[float] = mapped_column(Float, default=20000.0)
    storage_capacity_tons: Mapped[float] = mapped_column(Float, default=500000.0)
    congestion_baseline: Mapped[float] = mapped_column(Float, default=0.3)
