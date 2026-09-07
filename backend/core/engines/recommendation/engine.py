from core.interfaces.engine import Engine
from core.engines.recommendation.scorer import score_option
from core.engines.recommendation.ranking import rank_options
from config.constants import VESSEL_CLASSES


class RecommendationEngine(Engine):
    name = "RecommendationEngine"

    def execute(self, context) -> None:
        dr = context.decision_request
        feasible_classes = set((context.feasibility_result or {}).get("feasible_vessels", []))
        infeasible_map = {
            i["vessel_class"]: i["reason"]
            for i in (context.feasibility_result or {}).get("infeasible_vessels", [])
        }
        landed_costs = {lc["vessel_class"]: lc for lc in (context.landed_cost_result or [])}
        forecasts = {f["vessel_class"]: f for f in (context.forecast_result or [])}

        costs_per_ton = [lc["cost_per_ton"] for lc in landed_costs.values()] or [0]
        min_cost, max_cost = min(costs_per_ton), max(costs_per_ton) if costs_per_ton else (0, 1)
        if min_cost == max_cost:
            max_cost = min_cost + 1

        strategy = self._select_charter_strategy(dr)

        options = []
        for vessel_class in VESSEL_CLASSES:
            is_feasible = vessel_class in feasible_classes
            lc = landed_costs.get(vessel_class)
            fc = forecasts.get(vessel_class)
            score = 0.0
            if is_feasible and lc and fc:
                score = score_option(lc["cost_per_ton"], min_cost, max_cost, fc["confidence"], True)

            options.append({
                "vessel_class": vessel_class,
                "origin_port": dr.origin,
                "destination_port": dr.destination,
                "charter_strategy": strategy,
                "score": round(score, 4),
                "is_feasible": is_feasible,
                "rejection_reason": None if is_feasible else infeasible_map.get(vessel_class, "Infeasible"),
                "landed_cost": lc,
            })

        context.recommendation_result = rank_options(options)

    @staticmethod
    def _select_charter_strategy(dr) -> str:
        if dr.contract_preference and dr.contract_preference != "AUTO":
            return dr.contract_preference
        if dr.expected_voyages and dr.expected_voyages > 3:
            return "MULTI_VOYAGE"
        if dr.contract_duration_days and dr.contract_duration_days > 180:
            return "MEDIUM_TERM"
        if dr.contract_duration_days and dr.contract_duration_days > 30:
            return "SHORT_TERM"
        return "SPOT"
