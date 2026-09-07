from core.interfaces.engine import Engine
from core.engines.idle_vessel.positioning import estimate_deadhead_distance
from core.engines.idle_vessel.optimizer import recommend_action


class IdleVesselEngine(Engine):
    name = "IdleVesselEngine"

    def execute(self, context) -> None:
        dr = context.decision_request
        route = context.master_data.get("route")
        distance_nm = route.distance_nm if route else 5500.0
        feasible = (context.feasibility_result or {}).get("feasible_vessels", [])

        results = []
        for vessel_class in feasible or ["Panamax"]:
            demand_signal = context.master_data.get("demand_outlook", 0.5)
            idle_probability = round(max(0.05, min(0.9, 1 - demand_signal)), 2)
            expected_idle_days = round(idle_probability * 10, 1)
            deadhead = estimate_deadhead_distance(None, dr.origin, distance_nm)
            action = recommend_action(idle_probability, expected_idle_days)
            estimated_savings = round(deadhead * 0.0 if action == "CONTINUE_CURRENT_ROUTE" else expected_idle_days * 8000, 2)

            results.append({
                "vessel_class": vessel_class,
                "idle_probability": idle_probability,
                "expected_idle_days": expected_idle_days,
                "deadhead_distance_nm": deadhead,
                "recommended_action": action,
                "estimated_savings": estimated_savings,
            })

        context.idle_vessel_result = results
