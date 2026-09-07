from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class Commodity(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "commodities"

    name: Mapped[str] = mapped_column(String(100), unique=True)
    category: Mapped[str] = mapped_column(String(50), default="bulk")
