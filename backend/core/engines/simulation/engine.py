from core.interfaces.engine import Engine
from core.engines.simulation.scenarios import ScenarioParams
from core.engines.simulation.calculator import run_scenario


class SimulationEngine(Engine):
    name = "SimulationEngine"

    def execute(self, context, params: ScenarioParams | None = None, scenario_name: str = "default") -> dict | None:
        forecasts = context.forecast_result or []
        landed_costs = {lc["vessel_class"]: lc for lc in (context.landed_cost_result or [])}
        if not forecasts:
            context.simulation_results = None
            return None

        baseline_forecast = forecasts[0]
        baseline_lc = landed_costs.get(baseline_forecast["vessel_class"])
        if not baseline_lc:
            context.simulation_results = None
            return None

        params = params or ScenarioParams()
        result = run_scenario(context.decision_request, baseline_forecast, baseline_lc, context.master_data, params)
        result["scenario_name"] = scenario_name
        context.simulation_results = result
        return result
