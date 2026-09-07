from core.interfaces.engine import Engine
from core.engines.risk.rules import freight_volatility_risk, delivery_window_risk
from core.engines.risk.scorer import level_from_score, combined_score


class RiskEngine(Engine):
    name = "RiskEngine"

    def execute(self, context) -> None:
        dr = context.decision_request
        forecasts = context.forecast_result or []
        route = context.master_data.get("route")
        congestion = context.master_data.get("congestion_index", 0.3)
        cyclone_risk = context.master_data.get("cyclone_risk", 0.1)
        piracy_risk = route.piracy_risk_index if route else 0.1

        risks = []

        if forecasts:
            best = forecasts[0]
            vol = freight_volatility_risk(best["lower_bound"], best["upper_bound"], best["predicted_rate"])
            prob = min(vol, 1.0)
            impact = 0.6
            score = combined_score(prob, impact)
            risks.append({
                "risk_type": "FREIGHT_VOLATILITY", "risk_level": level_from_score(score),
                "probability": prob, "impact": impact, "score": score,
                "description": f"Forecast range spans {round(vol*100,1)}% of predicted rate.",
                "mitigation": "Consider index-linked or staggered booking to hedge volatility.",
            })

        transit_days = route.typical_transit_days if route else 18.0
        dw_prob = delivery_window_risk(dr.earliest_loading_date, dr.latest_delivery_date, transit_days)
        dw_score = combined_score(dw_prob, 0.7)
        risks.append({
            "risk_type": "DELIVERY_WINDOW", "risk_level": level_from_score(dw_score),
            "probability": dw_prob, "impact": 0.7, "score": dw_score,
            "description": "Delivery window buffer relative to typical transit time.",
            "mitigation": "Add schedule buffer or select a faster vessel class.",
        })

        cong_score = combined_score(congestion, 0.5)
        risks.append({
            "risk_type": "PORT_CONGESTION", "risk_level": level_from_score(cong_score),
            "probability": congestion, "impact": 0.5, "score": cong_score,
            "description": f"Destination congestion index observed at {congestion}.",
            "mitigation": "Build in waiting-time buffer or consider alternate berth scheduling.",
        })

        cyclone_score = combined_score(cyclone_risk, 0.8)
        risks.append({
            "risk_type": "WEATHER_CYCLONE", "risk_level": level_from_score(cyclone_score),
            "probability": cyclone_risk, "impact": 0.8, "score": cyclone_score,
            "description": f"Seasonal cyclone risk index for the route is {cyclone_risk}.",
            "mitigation": "Monitor weather advisories close to the loading window.",
        })

        piracy_score = combined_score(piracy_risk, 0.6)
        risks.append({
            "risk_type": "GEOPOLITICAL", "risk_level": level_from_score(piracy_score),
            "probability": piracy_risk, "impact": 0.6, "score": piracy_score,
            "description": "Route-level piracy/geopolitical risk index.",
            "mitigation": "Review current advisories for the transit corridor.",
        })

        feasible = (context.feasibility_result or {}).get("feasible_vessels", [])
        if not feasible:
            risks.append({
                "risk_type": "VESSEL_FEASIBILITY", "risk_level": "CRITICAL",
                "probability": 1.0, "impact": 1.0, "score": 1.0,
                "description": "No vessel class is feasible for this route/port combination.",
                "mitigation": "Reconsider destination port or split cargo across smaller vessels.",
            })

        context.risk_results = risks
