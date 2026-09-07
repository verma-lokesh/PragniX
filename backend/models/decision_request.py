from datetime import date
from sqlalchemy import String, Float, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from models.base import UUIDPKMixin, TimestampMixin


class DecisionRequest(Base, UUIDPKMixin, TimestampMixin):
    __tablename__ = "decision_requests"

    commodity: Mapped[str] = mapped_column(String(100))
    cargo_quantity: Mapped[float] = mapped_column(Float)
    origin: Mapped[str] = mapped_column(String(100))
    destination: Mapped[str] = mapped_column(String(100))
    earliest_loading_date: Mapped[date] = mapped_column(Date)
    latest_delivery_date: Mapped[date] = mapped_column(Date)
    contract_preference: Mapped[str] = mapped_column(String(30), default="AUTO")
    contract_duration_days: Mapped[int] = mapped_column(nullable=True)
    expected_voyages: Mapped[int] = mapped_column(nullable=True)
    preferred_vessel_type: Mapped[str] = mapped_column(String(50), nullable=True)
    target_freight_rate: Mapped[float] = mapped_column(Float, nullable=True)
    max_budget: Mapped[float] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="PENDING")

    forecasts: Mapped[list["FreightForecast"]] = relationship(back_populates="decision_request")
    landed_costs: Mapped[list["LandedCost"]] = relationship(back_populates="decision_request")
    recommendations: Mapped[list["Recommendation"]] = relationship(back_populates="decision_request")
    risks: Mapped[list["RiskAssessment"]] = relationship(back_populates="decision_request")
    market_entries: Mapped[list["MarketEntry"]] = relationship(back_populates="decision_request")
    split_cargos: Mapped[list["SplitCargo"]] = relationship(back_populates="decision_request")
    idle_vessels: Mapped[list["IdleVessel"]] = relationship(back_populates="decision_request")
    simulations: Mapped[list["Simulation"]] = relationship(back_populates="decision_request")
    audits: Mapped[list["DecisionAudit"]] = relationship(back_populates="decision_request")
