from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class Vessel(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "vessels"

    name: Mapped[str] = mapped_column(String(150))
    vessel_class: Mapped[str] = mapped_column(String(50), index=True)
    dwt: Mapped[float] = mapped_column(Float)
    loa: Mapped[float] = mapped_column(Float)
    beam: Mapped[float] = mapped_column(Float)
    draft: Mapped[float] = mapped_column(Float)
    current_position: Mapped[str] = mapped_column(String(150), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="AVAILABLE")
