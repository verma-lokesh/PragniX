from core.orchestrator.execution_context import ExecutionContext
from core.engines.feasibility.engine import FeasibilityEngine


def test_capesize_rejected_for_shallow_port(sample_decision_request):
    sample_decision_request.destination = "Vizag"
    context = ExecutionContext(decision_request=sample_decision_request, execution_id="t1")
    context.master_data = {"route": None}
    FeasibilityEngine().execute(context)

    result = context.feasibility_result
    assert "Capesize" not in result["feasible_vessels"]
    reasons = [i["reason"] for i in result["infeasible_vessels"] if i["vessel_class"] == "Capesize"]
    assert reasons and "draft" in reasons[0]


def test_all_smaller_classes_feasible_for_deep_port(sample_decision_request):
    sample_decision_request.destination = "Paradip"
    context = ExecutionContext(decision_request=sample_decision_request, execution_id="t2")
    context.master_data = {"route": None}
    FeasibilityEngine().execute(context)

    result = context.feasibility_result
    assert "Capesize" in result["feasible_vessels"]
    assert result["port_compatible"] is True
