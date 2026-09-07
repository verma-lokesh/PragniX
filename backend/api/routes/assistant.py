from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from api.dependencies import get_db_session
from core.agents.ops_assistant.agent import OpsAssistantAgent

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


class ChatRequest(BaseModel):
    decision_id: str
    message: str


class ChatResponse(BaseModel):
    answer: str
    tool: str


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db_session)):
    agent = OpsAssistantAgent()
    result = agent.chat(db, payload.decision_id, payload.message)
    return ChatResponse(**result)
