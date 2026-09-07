from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_db_session
from schemas.decision_request import DecisionRequestCreate
from schemas.decision import DecisionResponse
from core.orchestrator.decision_orchestrator import DecisionOrchestrator
from core.exceptions import NotFoundError
from repositories.decision_request_repository import DecisionRequestRepository
from models.decision_request import DecisionRequest as DecisionRequestModel
from api.routes._response_builder import build_decision_response

router = APIRouter(prefix="/api/decision", tags=["decision"])


@router.post("", response_model=DecisionResponse)
def create_decision(payload: DecisionRequestCreate, db: Session = Depends(get_db_session)):
    dr = DecisionRequestModel(**payload.model_dump())
    db.add(dr)
    db.flush()

    orchestrator = DecisionOrchestrator(db)
    context = orchestrator.run(dr)

    return build_decision_response(dr, context)


@router.get("/{decision_id}", response_model=DecisionResponse)
def get_decision(decision_id: str, db: Session = Depends(get_db_session)):
    repo = DecisionRequestRepository(db)
    dr = repo.get(decision_id)
    if dr is None:
        raise NotFoundError(f"Decision {decision_id} not found.")
    return build_decision_response(dr, context=None, db=db)
