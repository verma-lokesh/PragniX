from core.interfaces.engine import Engine
from core.engines.landed_cost.calculator import calculate_landed_cost


class LandedCostEngine(Engine):
    name = "LandedCostEngine"

    def execute(self, context) -> None:
        dr = context.decision_request
        forecasts = context.forecast_result or []
        route = context.master_data.get("route")
        distance_nm = route.distance_nm if route else 5500.0
        bunker_price = context.master_data.get("bunker_price", 550.0)
        commodity_price = context.master_data.get("commodity_price", 120.0)

        results = []
        for f in forecasts:
            result = calculate_landed_cost(
                vessel_class=f["vessel_class"],
                freight_rate_usd_per_ton=f["predicted_rate"],
                cargo_quantity=dr.cargo_quantity,
                port_name=dr.destination,
                distance_nm=distance_nm,
                bunker_price=bunker_price,
                commodity_price_usd_per_ton=commodity_price,
            )
            results.append(result)

        context.landed_cost_result = results
