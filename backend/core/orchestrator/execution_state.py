from dataclasses import dataclass, field
from utils.enums import EngineState


@dataclass
class EngineExecutionRecord:
    engine: str
    state: str = EngineState.PENDING.value
    duration_ms: float | None = None
    error: str | None = None


@dataclass
class ExecutionState:
    records: dict[str, EngineExecutionRecord] = field(default_factory=dict)

    def start(self, engine: str):
        self.records[engine] = EngineExecutionRecord(engine=engine, state=EngineState.RUNNING.value)

    def complete(self, engine: str, duration_ms: float):
        rec = self.records.setdefault(engine, EngineExecutionRecord(engine=engine))
        rec.state = EngineState.COMPLETED.value
        rec.duration_ms = duration_ms

    def fail(self, engine: str, error: str, duration_ms: float | None = None):
        rec = self.records.setdefault(engine, EngineExecutionRecord(engine=engine))
        rec.state = EngineState.FAILED.value
        rec.error = error
        rec.duration_ms = duration_ms

    def skip(self, engine: str, reason: str = ""):
        rec = self.records.setdefault(engine, EngineExecutionRecord(engine=engine))
        rec.state = EngineState.SKIPPED.value
        rec.error = reason or None

    def as_list(self) -> list[dict]:
        return [
            {"engine": r.engine, "state": r.state, "duration_ms": r.duration_ms, "error": r.error}
            for r in self.records.values()
        ]
