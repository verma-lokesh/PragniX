"""Seed the database from CSV files in data/raw/.

Run with:
    python -m backend.db.seed
or, when already inside the backend/ directory:
    python -m db.seed
"""
import csv
import os
from datetime import date, timedelta

from db.session import SessionLocal
from models.port import Port
from models.vessel import Vessel
from models.route import Route
from models.commodity import Commodity
from models.commodity_price import CommodityPrice
from models.bunker_price import BunkerPrice
from models.port_congestion import PortCongestion
from models.weather import Weather
from models.market_signal import MarketSignal

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def _read_csv(filename):
    path = os.path.join(RAW_DIR, filename)
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def seed_ports(db):
    if db.query(Port).count() > 0:
        return
    for row in _read_csv("port_infrastructure.csv"):
        db.add(Port(
            name=row["name"], country=row["country"], max_draft=float(row["max_draft"]),
            max_loa=float(row["max_loa"]), max_beam=float(row["max_beam"]),
            berth_count=int(row["berth_count"]),
            cargo_handling_rate_tons_per_day=float(row["cargo_handling_rate_tons_per_day"]),
            storage_capacity_tons=float(row["storage_capacity_tons"]),
            congestion_baseline=float(row["congestion_baseline"]),
        ))


def seed_vessels(db):
    if db.query(Vessel).count() > 0:
        return
    for row in _read_csv("vessel_data.csv"):
        db.add(Vessel(
            name=row["name"], vessel_class=row["vessel_class"], dwt=float(row["dwt"]),
            loa=float(row["loa"]), beam=float(row["beam"]), draft=float(row["draft"]),
            current_position=row["current_position"], status=row["status"],
        ))


def seed_routes(db):
    if db.query(Route).count() > 0:
        return
    for row in _read_csv("route_data.csv"):
        db.add(Route(
            origin=row["origin"], destination=row["destination"],
            distance_nm=float(row["distance_nm"]), typical_transit_days=float(row["typical_transit_days"]),
            piracy_risk_index=float(row["piracy_risk_index"]),
        ))


def seed_commodities(db):
    if db.query(Commodity).count() > 0:
        return {c.name: c for c in db.query(Commodity).all()}
    result = {}
    for row in _read_csv("commodity_data.csv"):
        c = Commodity(name=row["name"], category=row["category"])
        db.add(c)
        db.flush()
        result[c.name] = c
        db.add(CommodityPrice(commodity_id=c.id, price_date=date.today(), price_usd_per_ton=float(row["price_usd_per_ton"])))
    return result


def seed_bunker(db):
    if db.query(BunkerPrice).count() > 0:
        return
    for row in _read_csv("bunker_prices.csv"):
        db.add(BunkerPrice(port_name=row["port_name"], price_date=date.today(), price_usd_per_ton=float(row["price_usd_per_ton"])))


def seed_congestion(db):
    if db.query(PortCongestion).count() > 0:
        return
    for row in _read_csv("port_congestion.csv"):
        db.add(PortCongestion(
            port_name=row["port_name"], observed_date=date.today(),
            congestion_index=float(row["congestion_index"]), avg_wait_days=float(row["avg_wait_days"]),
        ))


def seed_weather(db):
    if db.query(Weather).count() > 0:
        return
    for row in _read_csv("weather.csv"):
        db.add(Weather(
            region=row["region"], observed_date=date.today(),
            cyclone_risk_index=float(row["cyclone_risk_index"]), rough_sea_index=float(row["rough_sea_index"]),
        ))


def seed_market_signals(db):
    if db.query(MarketSignal).count() > 0:
        return
    for i, row in enumerate(_read_csv("market_signals.csv")):
        db.add(MarketSignal(
            signal_date=date.today() - timedelta(days=i), category=row["category"],
            description=row["description"], sentiment_score=float(row["sentiment_score"]),
            impact_score=float(row["impact_score"]),
        ))


def run_seed():
    db = SessionLocal()
    try:
        seed_ports(db)
        seed_vessels(db)
        seed_routes(db)
        seed_commodities(db)
        seed_bunker(db)
        seed_congestion(db)
        seed_weather(db)
        seed_market_signals(db)
        db.commit()
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
