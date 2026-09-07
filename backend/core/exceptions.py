class NavoraError(Exception):
    code = "NAVORA_ERROR"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationError(NavoraError):
    code = "VALIDATION_ERROR"


class NotFoundError(NavoraError):
    code = "NOT_FOUND"


class DatabaseError(NavoraError):
    code = "DATABASE_ERROR"


class ForecastError(NavoraError):
    code = "FORECAST_ERROR"


class RecommendationError(NavoraError):
    code = "RECOMMENDATION_ERROR"


class EngineExecutionError(NavoraError):
    code = "ENGINE_EXECUTION_ERROR"


class GuardrailViolation(NavoraError):
    code = "GUARDRAIL_VIOLATION"


class SimulationError(NavoraError):
    code = "SIMULATION_ERROR"


class AgentError(NavoraError):
    code = "AGENT_ERROR"
