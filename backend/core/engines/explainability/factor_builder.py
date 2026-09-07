def build_factors(context) -> list[dict]:
    factors = []
    forecasts = context.forecast_result or []
    if forecasts:
        best = forecasts[0]
        factors.append({
            "factor": "Freight trend",
            "impact": "HIGH" if best["direction"] != "STABLE" else "MEDIUM",
            "direction": "POSITIVE" if best["direction"] == "DOWN" else ("NEGATIVE" if best["direction"] == "UP" else "NEUTRAL"),
            "explanation": f"{best['vessel_class']} freight rates are forecast to move {best['direction'].lower()} over the next {best['horizon_days']} days.",
        })

    recs = context.recommendation_result or []
    top_feasible = next((r for r in recs if r["is_feasible"]), None)
    if top_feasible:
        factors.append({
            "factor": "Cost efficiency",
            "impact": "HIGH",
            "direction": "POSITIVE",
            "explanation": f"{top_feasible['vessel_class']} offers the best landed-cost efficiency among feasible options (score {top_feasible['score']}).",
        })

    infeasible = [r for r in recs if not r["is_feasible"]]
    for r in infeasible[:2]:
        factors.append({
            "factor": f"{r['vessel_class']} feasibility",
            "impact": "MEDIUM",
            "direction": "NEGATIVE",
            "explanation": r.get("rejection_reason") or "Vessel class ruled infeasible for this route.",
        })

    risks = context.risk_results or []
    high_risks = [r for r in risks if r["risk_level"] in ("HIGH", "CRITICAL")]
    for r in high_risks[:2]:
        factors.append({
            "factor": r["risk_type"].replace("_", " ").title(),
            "impact": r["risk_level"],
            "direction": "NEGATIVE",
            "explanation": r["description"],
        })

    return factors
