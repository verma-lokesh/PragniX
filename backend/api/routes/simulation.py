from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies import get_db_session
from schemas.simulation import SimulationRequest, SimulationOut
from core.services.simulation_service import run_simulation

router = APIRouter(prefix="/api/simulation", tags=["simulation"])


@router.post("", response_model=SimulationOut)
def post_simulation(payload: SimulationRequest, db: Session = Depends(get_db_session)):
    result = run_simulation(db, payload)
    return SimulationOut(**result)
