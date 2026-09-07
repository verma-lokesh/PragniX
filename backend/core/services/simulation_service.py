from sqlalchemy.orm import Session
from core.orchestrator.execution_context import ExecutionContext
from core.services.decision_service import load_master_data
from core.engines.feasibility.engine import FeasibilityEngine
from core.engines.forecast.engine import ForecastEngine
from core.engines.landed_cost.engine import LandedCostEngine
from core.engines.simulation.engine import SimulationEngine
from core.engines.simulation.scenarios import ScenarioParams
from core.exceptions import SimulationError
from repositories.decision_request_repository import DecisionRequestRepository
from models.simulation import Simulation
from utils.serialization import to_json


def run_simulation(db: Session, request) -> dict:
    repo = DecisionRequestRepository(db)
    dr = repo.get(request.decision_id)
    if dr is None:
        raise SimulationError(f"Decision {request.decision_id} not found.")

    context = ExecutionContext(decision_request=dr, execution_id="sim")
    context.master_data = load_master_data(db, dr)

    FeasibilityEngine().execute(context)
    ForecastEngine().execute(context)
    LandedCostEngine().execute(context)

    params = ScenarioParams(
        freight_rate_pct_change=request.freight_rate_pct_change or 0.0,
        port_congestion_pct_change=request.port_congestion_pct_change or 0.0,
        bunker_price_pct_change=request.bunker_price_pct_change or 0.0,
        demand_pct_change=request.demand_pct_change or 0.0,
        delivery_delay_days=request.delivery_delay_days or 0.0,
    )
    result = SimulationEngine().execute(context, params=params, scenario_name=request.scenario_name)
    if result is None:
        raise SimulationError("Unable to run simulation: no baseline forecast/landed cost available.")

    db.add(Simulation(
        decision_request_id=dr.id,
        scenario_name=result["scenario_name"],
        scenario_params=to_json(params.__dict__),
        baseline_cost=result["baseline_cost"],
        scenario_cost=result["scenario_cost"],
        cost_delta=result["cost_delta"],
        delay_impact_days=result["delay_impact_days"],
        risk_impact=result["risk_impact"],
        recommendation_impact=result["recommendation_impact"],
    ))
    db.commit()

    return result
