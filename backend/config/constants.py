COMMODITIES = ["Coal", "Coking Coal", "Iron Ore"]
ORIGINS = ["Australia", "United States", "Mozambique", "Russia", "Indonesia"]
DESTINATIONS = ["Paradip", "Vizag", "Gangavaram", "Gopalpur", "Dhamra", "Sagar", "Haldia"]
VESSEL_CLASSES = ["Handysize", "Supramax", "Panamax", "Capesize"]
CHARTER_STRATEGIES = ["SPOT", "SHORT_TERM", "MEDIUM_TERM", "MULTI_VOYAGE"]
CONTRACT_PREFERENCES = ["AUTO", "SPOT", "SHORT_TERM", "MEDIUM_TERM", "MULTI_VOYAGE"]
RISK_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
MARKET_ENTRY_ACTIONS = ["BOOK_NOW", "WAIT", "MONITOR"]
ENGINE_STATES = ["PENDING", "RUNNING", "COMPLETED", "FAILED", "SKIPPED"]
FORECAST_HORIZONS_DAYS = [7, 14, 30, 60, 90]

VESSEL_SPECS = {
    "Handysize": {"dwt": 35000, "loa": 190, "beam": 32, "draft": 10.5},
    "Supramax": {"dwt": 58000, "loa": 200, "beam": 32.3, "draft": 12.5},
    "Panamax": {"dwt": 82000, "loa": 225, "beam": 32.3, "draft": 14.2},
    "Capesize": {"dwt": 180000, "loa": 292, "beam": 45, "draft": 18.2},
}

PORT_SPECS = {
    "Paradip": {"max_draft": 18.5, "max_loa": 300, "max_beam": 48, "congestion_baseline": 0.3},
    "Vizag": {"max_draft": 17.0, "max_loa": 290, "max_beam": 45, "congestion_baseline": 0.35},
    "Gangavaram": {"max_draft": 18.0, "max_loa": 300, "max_beam": 48, "congestion_baseline": 0.2},
    "Gopalpur": {"max_draft": 14.0, "max_loa": 230, "max_beam": 33, "congestion_baseline": 0.15},
    "Dhamra": {"max_draft": 18.0, "max_loa": 300, "max_beam": 48, "congestion_baseline": 0.2},
    "Sagar": {"max_draft": 13.5, "max_loa": 225, "max_beam": 32.3, "congestion_baseline": 0.25},
    "Haldia": {"max_draft": 8.5, "max_loa": 186, "max_beam": 28, "congestion_baseline": 0.4},
}

MODEL_VERSIONS = {
    "freight_forecast": "freight_forecast_v1",
    "risk_model": "risk_model_v1",
    "idle_vessel_model": "idle_vessel_model_v1",
}
