from enum import Enum


class VesselClass(str, Enum):
    HANDYSIZE = "Handysize"
    SUPRAMAX = "Supramax"
    PANAMAX = "Panamax"
    CAPESIZE = "Capesize"


class CharterStrategy(str, Enum):
    SPOT = "SPOT"
    SHORT_TERM = "SHORT_TERM"
    MEDIUM_TERM = "MEDIUM_TERM"
    MULTI_VOYAGE = "MULTI_VOYAGE"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class MarketEntryAction(str, Enum):
    BOOK_NOW = "BOOK_NOW"
    WAIT = "WAIT"
    MONITOR = "MONITOR"


class EngineState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class DecisionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"
    FAILED = "FAILED"
