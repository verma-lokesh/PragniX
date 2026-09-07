from datetime import timedelta


def determine_action(rate_direction: str, expected_change_pct: float, volatility_pct: float, avg_sentiment: float) -> tuple[str, float]:
    confidence = 0.6
    if rate_direction == "UP" and expected_change_pct > 5:
        confidence = min(0.9, 0.6 + expected_change_pct / 100)
        return "BOOK_NOW", confidence
    if rate_direction == "DOWN" and expected_change_pct < -5:
        confidence = min(0.85, 0.6 + abs(expected_change_pct) / 100)
        return "WAIT", confidence
    if volatility_pct > 15:
        return "MONITOR", 0.55
    if avg_sentiment < -0.3:
        return "MONITOR", 0.6
    return "MONITOR", confidence


def ideal_window(loading_date, action: str):
    if action == "BOOK_NOW":
        return loading_date, loading_date + timedelta(days=5)
    if action == "WAIT":
        return loading_date + timedelta(days=10), loading_date + timedelta(days=20)
    return loading_date, loading_date + timedelta(days=10)
