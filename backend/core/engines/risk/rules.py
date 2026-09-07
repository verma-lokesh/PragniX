def freight_volatility_risk(lower, upper, predicted) -> float:
    if predicted == 0:
        return 0.0
    return round(abs(upper - lower) / predicted, 3)


def delivery_window_risk(loading_date, delivery_date, transit_days) -> float:
    available = (delivery_date - loading_date).days
    if available <= 0:
        return 1.0
    buffer_ratio = (available - transit_days) / available
    return round(max(0.0, min(1.0, 1 - buffer_ratio)), 3)
