def build_features(decision_request, vessel_class: str, master_data: dict) -> dict:
    return {
        "vessel_class": vessel_class,
        "commodity": decision_request.commodity,
        "origin": decision_request.origin,
        "destination": decision_request.destination,
        "cargo_quantity": decision_request.cargo_quantity,
        "recent_rates": master_data.get("recent_rates", {}).get(vessel_class, []),
        "congestion": master_data.get("congestion_index", 0.3),
        "bunker_price": master_data.get("bunker_price", 550.0),
    }
