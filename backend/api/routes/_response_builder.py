import json
from schemas.decision import DecisionResponse, FeasibilityOut, ExplanationOut, EngineStatusOut


def build_decision_response(dr, context=None, db=None) -> DecisionResponse:
    if context is not None:
        return DecisionResponse(
            request_id=dr.id,
            status=dr.status,
            feasibility=FeasibilityOut(**context.feasibility_result) if context.feasibility_result else None,
            forecast=context.forecast_result,
            landed_cost=context.landed_cost_result,
            recommendation=context.recommendation_result,
            market_entry=context.market_entry_result,
            risks=context.risk_results,
            split_cargo=context.split_cargo_result,
            idle_vessel=context.idle_vessel_result,
            simulation=context.simulation_results,
            explanation=ExplanationOut(**context.explanation_results) if context.explanation_results else None,
            audit=None,
            engine_statuses=[EngineStatusOut(**s) for s in context.execution_state.as_list()],
        )

    # Reconstruct from persisted rows for GET /api/decision/{id}
    from repositories.forecast_repository import FreightForecastRepository
    from repositories.landed_cost_repository import LandedCostRepository
    from repositories.recommendation_repository import RecommendationRepository
    from repositories.risk_repository import RiskAssessmentRepository
    from repositories.market_entry_repository import MarketEntryRepository
    from repositories.split_cargo_repository import SplitCargoRepository
    from repositories.idle_vessel_repository import IdleVesselRepository
    from repositories.decision_audit_repository import DecisionAuditRepository

    def _rows(repo_cls):
        repo = repo_cls(db)
        return db.query(repo.model).filter_by(decision_request_id=dr.id).all()

    forecasts = _rows(FreightForecastRepository)
    landed_costs = _rows(LandedCostRepository)
    recs = _rows(RecommendationRepository)
    risks = _rows(RiskAssessmentRepository)
    market_entries = _rows(MarketEntryRepository)
    splits = _rows(SplitCargoRepository)
    idles = _rows(IdleVesselRepository)
    audits = _rows(DecisionAuditRepository)

    lc_by_id = {lc.id: lc for lc in landed_costs}

    def lc_dict(lc):
        return {
            "vessel_class": lc.vessel_class, "freight_cost": lc.freight_cost, "port_charges": lc.port_charges,
            "insurance": lc.insurance, "levies": lc.levies, "bunker_cost": lc.bunker_cost,
            "other_costs": lc.other_costs, "total_cost": lc.total_cost, "cost_per_ton": lc.cost_per_ton,
            "currency": lc.currency,
        }

    recommendation_out = [{
        "vessel_class": r.vessel_class, "origin_port": r.origin_port, "destination_port": r.destination_port,
        "charter_strategy": r.charter_strategy, "rank": r.rank, "score": r.score, "is_feasible": r.is_feasible,
        "rejection_reason": r.rejection_reason,
        "landed_cost": lc_dict(lc_by_id[r.landed_cost_id]) if r.landed_cost_id in lc_by_id else None,
    } for r in recs]

    me = market_entries[0] if market_entries else None
    split_options = [{
        "option_label": s.option_label,
        "vessel_composition": json.loads(s.vessel_composition),
        "total_cost": s.total_cost,
        "is_recommended": s.is_recommended,
    } for s in splits]

    return DecisionResponse(
        request_id=dr.id,
        status=dr.status,
        feasibility=None,
        forecast=[{
            "vessel_class": f.vessel_class, "horizon_days": f.horizon_days, "predicted_rate": f.predicted_rate,
            "lower_bound": f.lower_bound, "upper_bound": f.upper_bound, "direction": f.direction,
            "confidence": f.confidence, "forecast_date": f.forecast_date, "model_name": f.model_name,
            "model_version": f.model_version, "model_type": f.model_type,
        } for f in forecasts],
        landed_cost=[lc_dict(lc) for lc in landed_costs],
        recommendation=recommendation_out,
        market_entry={
            "recommended_action": me.recommended_action,
            "ideal_entry_window_start": me.ideal_entry_window_start,
            "ideal_entry_window_end": me.ideal_entry_window_end,
            "expected_rate_change_pct": me.expected_rate_change_pct,
            "confidence": me.confidence,
            "reasons": me.reasons.split("; ") if me.reasons else [],
            "risk_factors": [],
        } if me else None,
        risks=[{
            "risk_type": r.risk_type, "risk_level": r.risk_level, "probability": r.probability,
            "impact": r.impact, "score": r.score, "description": r.description, "mitigation": r.mitigation,
        } for r in risks],
        split_cargo={"options": split_options, "recommended_option": next((s["option_label"] for s in split_options if s["is_recommended"]), "NONE")} if split_options else None,
        idle_vessel=[{
            "vessel_class": i.vessel_class, "idle_probability": i.idle_probability,
            "expected_idle_days": i.expected_idle_days, "deadhead_distance_nm": i.deadhead_distance_nm,
            "recommended_action": i.recommended_action, "estimated_savings": i.estimated_savings,
        } for i in idles],
        simulation=None,
        explanation=None,
        audit=[{
            "execution_id": a.execution_id, "engine": a.engine, "input_summary": a.input_summary,
            "output_summary": a.output_summary, "model_version": a.model_version, "confidence": a.confidence,
            "decision": a.decision, "explanation": a.explanation,
        } for a in audits],
        engine_statuses=[],
    )
