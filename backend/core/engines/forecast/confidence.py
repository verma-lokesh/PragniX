def compute_confidence(sample_size: int, model_type: str) -> float:
    base = 0.55 if model_type == "fallback" else 0.8
    bonus = min(sample_size, 20) * 0.01
    return round(min(base + bonus, 0.95), 2)
