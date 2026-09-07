"""Declares the conceptual engine execution order used by the DecisionOrchestrator.
Critical engines (feasibility, forecast, landed_cost, recommendation) must succeed
for a COMPLETED status; non-critical engines can fail without failing the whole decision.
"""

CRITICAL_ENGINES = {"FeasibilityEngine", "ForecastEngine", "LandedCostEngine", "RecommendationEngine"}

EXECUTION_ORDER = [
    "FeasibilityEngine",
    "ForecastEngine",
    "LandedCostEngine",
    "RecommendationEngine",
    "MarketEntryEngine",
    "RiskEngine",
    "SplitCargoEngine",
    "IdleVesselEngine",
    "SimulationEngine",
    "ExplainabilityEngine",
]
