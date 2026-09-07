from fastapi import APIRouter
from db.health import check_db_health

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/health/db")
def health_db():
    ok = check_db_health()
    return {"status": "ok" if ok else "unavailable"}
