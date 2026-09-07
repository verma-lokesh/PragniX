from utils.calculations import weighted_score, clamp


def score_option(cost_per_ton: float, min_cost: float, max_cost: float, confidence: float, feasible: bool) -> float:
    if not feasible:
        return 0.0
    cost_range = max(max_cost - min_cost, 1e-6)
    cost_score = clamp(1 - (cost_per_ton - min_cost) / cost_range, 0, 1)
    return weighted_score({
        "cost": (cost_score, 0.6),
        "confidence": (confidence, 0.4),
    })
