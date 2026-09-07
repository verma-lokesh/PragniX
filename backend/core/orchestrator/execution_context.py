from dataclasses import dataclass, field
from typing import Any, Optional
from core.orchestrator.execution_state import ExecutionState


@dataclass
class ExecutionContext:
    decision_request: Any
    execution_id: str
    master_data: dict[str, Any] = field(default_factory=dict)

    feasibility_result: Optional[dict] = None
    forecast_result: Optional[list[dict]] = None
    landed_cost_result: Optional[list[dict]] = None
    recommendation_result: Optional[list[dict]] = None
    market_entry_result: Optional[dict] = None
    risk_results: Optional[list[dict]] = None
    split_cargo_result: Optional[dict] = None
    idle_vessel_result: Optional[list[dict]] = None
    simulation_results: Optional[dict] = None
    explanation_results: Optional[dict] = None
    audit_result: Optional[list[dict]] = None

    execution_state: ExecutionState = field(default_factory=ExecutionState)
    errors: dict[str, str] = field(default_factory=dict)
