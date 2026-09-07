import pytest
from core.orchestrator.decision_orchestrator import DecisionOrchestrator
from models.decision_request import DecisionRequest
from datetime import date


def test_full_orchestrator_run_completes(db_session):
    dr = DecisionRequest(
        commodity="Coking Coal", cargo_quantity=80000, origin="Australia", destination="Vizag",
        earliest_loading_date=date(2026, 10, 1), latest_delivery_date=date(2026, 10, 30),
        contract_preference="AUTO", currency="USD",
    )
    db_session.add(dr)
    db_session.flush()

    orchestrator = DecisionOrchestrator(db_session)
    context = orchestrator.run(dr)

    assert dr.status in ("COMPLETED", "PARTIALLY_COMPLETED")
    assert context.feasibility_result is not None
    assert context.forecast_result
    assert context.landed_cost_result
    assert context.recommendation_result
    assert context.risk_results
    assert context.explanation_results

    states = {s.engine: s.state for s in context.execution_state.records.values()}
    for critical in ("FeasibilityEngine", "ForecastEngine", "LandedCostEngine", "RecommendationEngine"):
        assert states[critical] == "COMPLETED"


def test_guardrail_rejects_bad_input(db_session):
    from core.exceptions import GuardrailViolation
    dr = DecisionRequest(
        commodity="Unobtainium", cargo_quantity=-5, origin="Australia", destination="Australia",
        earliest_loading_date=date(2026, 10, 30), latest_delivery_date=date(2026, 10, 1),
        contract_preference="AUTO", currency="USD",
    )
    db_session.add(dr)
    db_session.flush()

    orchestrator = DecisionOrchestrator(db_session)
    with pytest.raises(GuardrailViolation):
        orchestrator.run(dr)
