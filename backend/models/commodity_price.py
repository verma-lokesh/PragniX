from datetime import date
from sqlalchemy import String, Float, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class CommodityPrice(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "commodity_prices"

    commodity_id: Mapped[str] = mapped_column(String(36), ForeignKey("commodities.id"))
    price_date: Mapped[date] = mapped_column(Date)
    price_usd_per_ton: Mapped[float] = mapped_column(Float)
