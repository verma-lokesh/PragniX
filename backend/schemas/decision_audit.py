from typing import Optional
from pydantic import BaseModel


class DecisionAuditOut(BaseModel):
    execution_id: str
    engine: str
    input_summary: str
    output_summary: str
    model_version: Optional[str] = None
    confidence: Optional[float] = None
    decision: Optional[str] = None
    explanation: Optional[str] = None
