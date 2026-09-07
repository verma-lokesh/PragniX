import statistics
from config.constants import MODEL_VERSIONS


def predict_rate(features: dict, horizon_days: int) -> dict:
    """Deterministic MVP fallback forecaster.
    Uses recent rate history (mean + seasonal/horizon drift) when available,
    otherwise a commodity/route baseline. Always marked model_type=fallback
    unless a trained artifact is later plugged in via ml/inference.
    """
    recent = features.get("recent_rates") or []
    if recent:
        base_rate = statistics.mean(recent)
        volatility = statistics.pstdev(recent) if len(recent) > 1 else base_rate * 0.08
    else:
        base_rate = _baseline_rate(features["vessel_class"])
        volatility = base_rate * 0.12

    congestion_adj = 1 + (features.get("congestion", 0.3) - 0.3) * 0.3
    bunker_adj = 1 + max(0.0, (features.get("bunker_price", 550) - 550) / 550) * 0.15
    horizon_drift = 1 + (horizon_days / 90) * 0.03

    predicted = base_rate * congestion_adj * bunker_adj * horizon_drift
    direction = "UP" if predicted > base_rate * 1.01 else ("DOWN" if predicted < base_rate * 0.99 else "STABLE")

    return {
        "predicted_rate": round(predicted, 2),
        "lower_bound": round(max(predicted - volatility, 0), 2),
        "upper_bound": round(predicted + volatility, 2),
        "direction": direction,
        "model_name": "freight_forecast_fallback",
        "model_version": MODEL_VERSIONS["freight_forecast"],
        "model_type": "fallback",
        "sample_size": len(recent),
    }


def _baseline_rate(vessel_class: str) -> float:
    baselines = {"Handysize": 18.0, "Supramax": 15.5, "Panamax": 13.0, "Capesize": 10.5}
    return baselines.get(vessel_class, 14.0)
