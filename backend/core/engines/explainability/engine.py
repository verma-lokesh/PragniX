from core.interfaces.engine import Engine
from core.engines.explainability.factor_builder import build_factors
from core.engines.explainability.formatter import format_explanation
from config.constants import MODEL_VERSIONS


class ExplainabilityEngine(Engine):
    name = "ExplainabilityEngine"

    def execute(self, context) -> None:
        factors = build_factors(context)
        forecasts = context.forecast_result or []
        confidence = forecasts[0]["confidence"] if forecasts else 0.5
        context.explanation_results = format_explanation(
            factors, MODEL_VERSIONS["freight_forecast"], confidence
        )
