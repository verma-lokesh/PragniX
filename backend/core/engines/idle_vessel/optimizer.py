def recommend_action(idle_probability: float, expected_idle_days: float) -> str:
    if idle_probability > 0.6:
        return "SEEK_ALTERNATE_CARGO"
    if idle_probability > 0.35:
        return "REPOSITION"
    if expected_idle_days > 3:
        return "WAIT"
    return "CONTINUE_CURRENT_ROUTE"
