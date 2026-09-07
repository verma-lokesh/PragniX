def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def pct_change(old: float, new: float) -> float:
    if old == 0:
        return 0.0
    return round(((new - old) / old) * 100, 2)


def weighted_score(components: dict[str, tuple[float, float]]) -> float:
    """components: name -> (value_0_to_1, weight). Returns 0-1 score."""
    total_weight = sum(w for _, w in components.values()) or 1.0
    return round(sum(v * w for v, w in components.values()) / total_weight, 4)
