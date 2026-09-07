import datetime


def format_explanation(factors: list[dict], model_version: str, confidence: float) -> dict:
    return {
        "model_version": model_version,
        "data_timestamp": datetime.datetime.utcnow().isoformat(),
        "factors": factors,
        "confidence": confidence,
    }
