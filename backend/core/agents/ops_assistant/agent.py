from sqlalchemy.orm import Session
from core.agents.ops_assistant.graph import route_and_answer


class OpsAssistantAgent:
    def chat(self, db: Session, decision_id: str, message: str) -> dict:
        return route_and_answer(db, decision_id, message)
