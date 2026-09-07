from datetime import date
from config.constants import COMMODITIES, ORIGINS, DESTINATIONS, CONTRACT_PREFERENCES


def validate_commodity(commodity: str) -> list[str]:
    return [] if commodity in COMMODITIES else [f"Unknown commodity '{commodity}'. Expected one of {COMMODITIES}."]


def validate_origin_destination(origin: str, destination: str) -> list[str]:
    errors = []
    if origin not in ORIGINS:
        errors.append(f"Unknown origin '{origin}'. Expected one of {ORIGINS}.")
    if destination not in DESTINATIONS:
        errors.append(f"Unknown destination '{destination}'. Expected one of {DESTINATIONS}.")
    if origin == destination:
        errors.append("origin and destination must differ.")
    return errors


def validate_dates(loading: date, delivery: date) -> list[str]:
    if delivery < loading:
        return ["latest_delivery_date must be on or after earliest_loading_date."]
    return []


def validate_quantity(quantity: float) -> list[str]:
    return [] if quantity > 0 else ["cargo_quantity must be positive."]


def validate_contract_preference(pref: str) -> list[str]:
    return [] if pref in CONTRACT_PREFERENCES else [f"Unknown contract_preference '{pref}'."]
