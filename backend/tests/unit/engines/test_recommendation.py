from core.orchestrator.execution_context import ExecutionContext
from core.engines.feasibility.engine import FeasibilityEngine
from core.engines.forecast.engine import ForecastEngine
from core.engines.landed_cost.engine import LandedCostEngine
from core.engines.recommendation.engine import RecommendationEngine


def test_infeasible_vessel_never_top_ranked(sample_decision_request):
    sample_decision_request.destination = "Vizag"
    context = ExecutionContext(decision_request=sample_decision_request, execution_id="t4")
    context.master_data = {"route": None, "congestion_index": 0.3, "bunker_price": 550, "commodity_price": 220}
    FeasibilityEngine().execute(context)
    ForecastEngine().execute(context)
    LandedCostEngine().execute(context)
    RecommendationEngine().execute(context)

    ranked = sorted(context.recommendation_result, key=lambda r: r["rank"])
    top = ranked[0]
    assert top["is_feasible"] is True

    capesize = next(r for r in context.recommendation_result if r["vessel_class"] == "Capesize")
    assert capesize["is_feasible"] is False
    assert capesize["rank"] == 999
