def estimate_deadhead_distance(current_position: str | None, origin: str, route_distance_nm: float) -> float:
    if not current_position or current_position == origin:
        return 0.0
    return round(route_distance_nm * 0.15, 1)
