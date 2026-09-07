from core.orchestrator.execution_context import ExecutionContext
from core.engines.feasibility.engine import FeasibilityEngine
from core.engines.forecast.engine import ForecastEngine
from core.engines.risk.engine import RiskEngine


def test_risk_levels_are_valid(sample_decision_request):
    context = ExecutionContext(decision_request=sample_decision_request, execution_id="t5")
    context.master_data = {
        "route": None, "congestion_index": 0.3, "cyclone_risk": 0.15, "bunker_price": 550,
    }
    FeasibilityEngine().execute(context)
    ForecastEngine().execute(context)
    RiskEngine().execute(context)

    valid_levels = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
    for r in context.risk_results:
        assert r["risk_level"] in valid_levels
        assert 0 <= r["probability"] <= 1
