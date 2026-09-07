from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class Route(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "routes"

    origin: Mapped[str] = mapped_column(String(100), index=True)
    destination: Mapped[str] = mapped_column(String(100), index=True)
    distance_nm: Mapped[float] = mapped_column(Float)
    typical_transit_days: Mapped[float] = mapped_column(Float)
    piracy_risk_index: Mapped[float] = mapped_column(Float, default=0.1)
