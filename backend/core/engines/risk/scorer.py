from utils.enums import RiskLevel


def level_from_score(score: float) -> str:
    if score >= 0.75:
        return RiskLevel.CRITICAL.value
    if score >= 0.5:
        return RiskLevel.HIGH.value
    if score >= 0.25:
        return RiskLevel.MEDIUM.value
    return RiskLevel.LOW.value


def combined_score(probability: float, impact: float) -> float:
    return round(probability * impact, 3)
