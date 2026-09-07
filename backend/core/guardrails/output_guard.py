from core.exceptions import GuardrailViolation


def run_output_guardrail(context) -> list[str]:
    warnings: list[str] = []

    for lc in (context.landed_cost_result or []):
        if lc["total_cost"] < 0 or lc["cost_per_ton"] < 0:
            raise GuardrailViolation(f"Negative cost computed for {lc['vessel_class']}.")

    for f in (context.forecast_result or []):
        if not (0 <= f["confidence"] <= 1):
            raise GuardrailViolation(f"Invalid confidence for {f['vessel_class']} forecast.")
        if f["lower_bound"] > f["upper_bound"]:
            raise GuardrailViolation(f"Invalid forecast range for {f['vessel_class']}.")

    for r in (context.risk_results or []):
        if r["risk_level"] not in ("LOW", "MEDIUM", "HIGH", "CRITICAL"):
            raise GuardrailViolation(f"Invalid risk level: {r['risk_level']}")

    for rec in (context.recommendation_result or []):
        if rec["is_feasible"] and rec["rank"] == 999:
            warnings.append(f"{rec['vessel_class']} marked feasible but unranked.")

    return warnings
