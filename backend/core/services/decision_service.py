import statistics
from datetime import date
from sqlalchemy.orm import Session

from repositories.port_repository import PortRepository
from repositories.vessel_repository import VesselRepository
from repositories.route_repository import RouteRepository
from repositories.commodity_price_repository import CommodityPriceRepository
from repositories.freight_rate_repository import FreightRateRepository
from repositories.bunker_price_repository import BunkerPriceRepository
from repositories.port_congestion_repository import PortCongestionRepository
from repositories.weather_repository import WeatherRepository
from repositories.market_signal_repository import MarketSignalRepository
from config.constants import VESSEL_CLASSES, VESSEL_SPECS, PORT_SPECS


def load_master_data(db: Session, decision_request) -> dict:
    """Loads real DB data where present, otherwise falls back to config
    baselines so the pipeline is runnable without a fully seeded database.
    """
    route_repo = RouteRepository(db)
    route = (
        db.query(route_repo.model)
        .filter_by(origin=decision_request.origin, destination=decision_request.destination)
        .first()
    )
    if route is None:
        route = route_repo.model(
            origin=decision_request.origin,
            destination=decision_request.destination,
            distance_nm=5500.0,
            typical_transit_days=18.0,
            piracy_risk_index=0.12,
        )

    freight_repo = FreightRateRepository(db)
    recent_rates: dict[str, list[float]] = {}
    for vessel_class in VESSEL_CLASSES:
        rows = (
            db.query(freight_repo.model)
            .filter_by(vessel_class=vessel_class, origin=decision_request.origin, destination=decision_request.destination)
            .order_by(freight_repo.model.rate_date.desc())
            .limit(10)
            .all()
        )
        if rows:
            recent_rates[vessel_class] = [r.rate_usd_per_ton for r in rows]

    bunker_repo = BunkerPriceRepository(db)
    bunker_row = (
        db.query(bunker_repo.model)
        .filter_by(port_name=decision_request.destination)
        .order_by(bunker_repo.model.price_date.desc())
        .first()
    )
    bunker_price = bunker_row.price_usd_per_ton if bunker_row else 550.0

    commodity_price_repo = CommodityPriceRepository(db)
    commodity_price = 120.0  # fallback baseline; real lookup requires commodity_id join

    congestion_repo = PortCongestionRepository(db)
    congestion_row = (
        db.query(congestion_repo.model)
        .filter_by(port_name=decision_request.destination)
        .order_by(congestion_repo.model.observed_date.desc())
        .first()
    )
    congestion_index = congestion_row.congestion_index if congestion_row else PORT_SPECS.get(
        decision_request.destination, {}
    ).get("congestion_baseline", 0.3)

    weather_repo = WeatherRepository(db)
    weather_row = (
        db.query(weather_repo.model)
        .filter_by(region=decision_request.destination)
        .order_by(weather_repo.model.observed_date.desc())
        .first()
    )
    cyclone_risk = weather_row.cyclone_risk_index if weather_row else 0.15

    signal_repo = MarketSignalRepository(db)
    market_signals = db.query(signal_repo.model).order_by(signal_repo.model.signal_date.desc()).limit(10).all()

    return {
        "route": route,
        "recent_rates": recent_rates,
        "bunker_price": bunker_price,
        "commodity_price": commodity_price,
        "congestion_index": congestion_index,
        "cyclone_risk": cyclone_risk,
        "market_signals": market_signals,
        "demand_outlook": 0.55,
    }
