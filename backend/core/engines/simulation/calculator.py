from core.engines.landed_cost.calculator import calculate_landed_cost
from core.engines.risk.scorer import level_from_score


def run_scenario(dr, baseline_forecast: dict, baseline_landed_cost: dict, master_data: dict, params) -> dict:
    adjusted_rate = baseline_forecast["predicted_rate"] * (1 + params.freight_rate_pct_change / 100)
    adjusted_bunker = master_data.get("bunker_price", 550.0) * (1 + params.bunker_price_pct_change / 100)
    route = master_data.get("route")
    distance_nm = route.distance_nm if route else 5500.0

    scenario_lc = calculate_landed_cost(
        vessel_class=baseline_forecast["vessel_class"],
        freight_rate_usd_per_ton=adjusted_rate,
        cargo_quantity=dr.cargo_quantity,
        port_name=dr.destination,
        distance_nm=distance_nm,
        bunker_price=adjusted_bunker,
        commodity_price_usd_per_ton=master_data.get("commodity_price", 120.0),
    )

    cost_delta = round(scenario_lc["total_cost"] - baseline_landed_cost["total_cost"], 2)
    congestion_effect = abs(params.port_congestion_pct_change) / 100
    risk_score = min(1.0, 0.2 + congestion_effect + abs(params.demand_pct_change) / 200)

    return {
        "baseline_cost": baseline_landed_cost["total_cost"],
        "scenario_cost": scenario_lc["total_cost"],
        "cost_delta": cost_delta,
        "delay_impact_days": params.delivery_delay_days,
        "risk_impact": level_from_score(risk_score),
        "recommendation_impact": (
            "Recommendation would likely shift toward a smaller vessel class or WAIT strategy."
            if cost_delta > 0 else "Current recommendation remains favorable under this scenario."
        ),
    }
