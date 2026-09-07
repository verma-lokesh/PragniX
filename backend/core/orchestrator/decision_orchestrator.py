import time
import uuid
from sqlalchemy.orm import Session

from core.orchestrator.execution_context import ExecutionContext
from core.orchestrator.workflow import EXECUTION_ORDER, CRITICAL_ENGINES
from core.services.decision_service import load_master_data
from core.guardrails.input_guard import run_input_guardrail
from core.guardrails.output_guard import run_output_guardrail
from core.exceptions import EngineExecutionError, GuardrailViolation

from core.engines.feasibility.engine import FeasibilityEngine
from core.engines.forecast.engine import ForecastEngine
from core.engines.landed_cost.engine import LandedCostEngine
from core.engines.recommendation.engine import RecommendationEngine
from core.engines.market_entry.engine import MarketEntryEngine
from core.engines.risk.engine import RiskEngine
from core.engines.split_cargo.engine import SplitCargoEngine
from core.engines.idle_vessel.engine import IdleVesselEngine
from core.engines.simulation.engine import SimulationEngine
from core.engines.explainability.engine import ExplainabilityEngine

from repositories.decision_request_repository import DecisionRequestRepository
from repositories.forecast_repository import FreightForecastRepository
from repositories.landed_cost_repository import LandedCostRepository
from repositories.recommendation_repository import RecommendationRepository
from repositories.risk_repository import RiskAssessmentRepository
from repositories.market_entry_repository import MarketEntryRepository
from repositories.split_cargo_repository import SplitCargoRepository
from repositories.idle_vessel_repository import IdleVesselRepository
from repositories.decision_audit_repository import DecisionAuditRepository

from config.logging import get_logger
from utils.serialization import to_json
from datetime import date as _date


def _parse_date(value):
    if value is None or isinstance(value, _date):
        return value
    return _date.fromisoformat(value)

logger = get_logger("navora.orchestrator")

ENGINE_REGISTRY = {
    "FeasibilityEngine": FeasibilityEngine,
    "ForecastEngine": ForecastEngine,
    "LandedCostEngine": LandedCostEngine,
    "RecommendationEngine": RecommendationEngine,
    "MarketEntryEngine": MarketEntryEngine,
    "RiskEngine": RiskEngine,
    "SplitCargoEngine": SplitCargoEngine,
    "IdleVesselEngine": IdleVesselEngine,
    "SimulationEngine": SimulationEngine,
    "ExplainabilityEngine": ExplainabilityEngine,
}


class DecisionOrchestrator:
    def __init__(self, db: Session):
        self.db = db

    def run(self, decision_request) -> ExecutionContext:
        execution_id = str(uuid.uuid4())

        run_input_guardrail(decision_request)

        context = ExecutionContext(decision_request=decision_request, execution_id=execution_id)
        context.master_data = load_master_data(self.db, decision_request)

        for engine_name in EXECUTION_ORDER:
            engine_cls = ENGINE_REGISTRY[engine_name]
            engine = engine_cls()
            start = time.perf_counter()
            context.execution_state.start(engine_name)
            try:
                engine.execute(context)
                duration_ms = round((time.perf_counter() - start) * 1000, 2)
                context.execution_state.complete(engine_name, duration_ms)
                logger.info(f"{engine_name} completed", extra={
                    "engine": engine_name, "execution_id": execution_id, "duration_ms": duration_ms, "status": "COMPLETED",
                })
            except Exception as exc:  # noqa: BLE001
                duration_ms = round((time.perf_counter() - start) * 1000, 2)
                context.execution_state.fail(engine_name, str(exc), duration_ms)
                context.errors[engine_name] = str(exc)
                logger.error(f"{engine_name} failed: {exc}", extra={
                    "engine": engine_name, "execution_id": execution_id, "duration_ms": duration_ms, "status": "FAILED",
                })
                if engine_name in CRITICAL_ENGINES:
                    raise EngineExecutionError(f"{engine_name} failed critically: {exc}") from exc

        warnings = run_output_guardrail(context)
        for w in warnings:
            logger.warning(w, extra={"execution_id": execution_id})

        self._persist(context)
        return context

    def _persist(self, context: ExecutionContext) -> None:
        dr = context.decision_request
        db = self.db

        if context.forecast_result:
            from models.freight_forecast import FreightForecast
            for f in context.forecast_result:
                data = dict(f)
                data["forecast_date"] = _parse_date(data["forecast_date"])
                db.add(FreightForecast(decision_request_id=dr.id, **data))

        landed_cost_ids = {}
        if context.landed_cost_result:
            from models.landed_cost import LandedCost
            for lc in context.landed_cost_result:
                row = LandedCost(decision_request_id=dr.id, **lc)
                db.add(row)
                db.flush()
                landed_cost_ids[lc["vessel_class"]] = row.id

        if context.recommendation_result:
            from models.recommendation import Recommendation
            for rec in context.recommendation_result:
                db.add(Recommendation(
                    decision_request_id=dr.id,
                    landed_cost_id=landed_cost_ids.get(rec["vessel_class"]),
                    vessel_class=rec["vessel_class"],
                    origin_port=rec["origin_port"],
                    destination_port=rec["destination_port"],
                    route_id=None,
                    charter_strategy=rec["charter_strategy"],
                    rank=rec["rank"],
                    score=rec["score"],
                    is_feasible=rec["is_feasible"],
                    rejection_reason=rec["rejection_reason"],
                ))

        if context.risk_results:
            from models.risk_assessment import RiskAssessment
            db.add_all([RiskAssessment(decision_request_id=dr.id, **r) for r in context.risk_results])

        if context.market_entry_result:
            from models.market_entry import MarketEntry
            me = dict(context.market_entry_result)
            reasons = me.pop("reasons", [])
            me.pop("risk_factors", None)
            db.add(MarketEntry(
                decision_request_id=dr.id,
                recommended_action=me["recommended_action"],
                ideal_entry_window_start=_parse_date(me.get("ideal_entry_window_start")),
                ideal_entry_window_end=_parse_date(me.get("ideal_entry_window_end")),
                expected_rate_change_pct=me["expected_rate_change_pct"],
                confidence=me["confidence"],
                reasons="; ".join(reasons),
            ))

        if context.split_cargo_result and context.split_cargo_result.get("options"):
            from models.split_cargo import SplitCargo
            for opt in context.split_cargo_result["options"]:
                db.add(SplitCargo(
                    decision_request_id=dr.id,
                    option_label=opt["option_label"],
                    vessel_composition=to_json(opt["vessel_composition"]),
                    total_cost=opt["total_cost"],
                    is_recommended=opt["is_recommended"],
                ))

        if context.idle_vessel_result:
            from models.idle_vessel import IdleVessel
            db.add_all([IdleVessel(decision_request_id=dr.id, **iv) for iv in context.idle_vessel_result])

        from models.decision_audit import DecisionAudit
        for engine_name, record in context.execution_state.records.items():
            db.add(DecisionAudit(
                decision_request_id=dr.id,
                execution_id=context.execution_id,
                engine=engine_name,
                input_summary=f"decision_request={dr.id}",
                output_summary=record.state,
                model_version=None,
                confidence=None,
                decision=record.state,
                explanation=context.errors.get(engine_name),
            ))

        has_critical_failure = any(
            e in context.errors for e in CRITICAL_ENGINES
        )
        dr.status = "PARTIALLY_COMPLETED" if context.errors and not has_critical_failure else "COMPLETED"

        db.commit()
