from core.orchestrator.execution_context import ExecutionContext
from core.engines.feasibility.engine import FeasibilityEngine
from core.engines.forecast.engine import ForecastEngine


def test_forecast_produces_bounds_and_confidence(sample_decision_request):
    context = ExecutionContext(decision_request=sample_decision_request, execution_id="t3")
    context.master_data = {"route": None, "congestion_index": 0.3, "bunker_price": 550}
    FeasibilityEngine().execute(context)
    ForecastEngine().execute(context)

    assert context.forecast_result
    for f in context.forecast_result:
        assert f["lower_bound"] <= f["predicted_rate"] <= f["upper_bound"]
        assert 0 <= f["confidence"] <= 1
        assert f["model_type"] == "fallback"
