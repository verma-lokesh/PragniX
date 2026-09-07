from fastapi import APIRouter

from api.routes import health, decision, forecast, recommendation, risk, market_entry, split_cargo, idle_vessel, simulation, assistant, market

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(decision.router)
api_router.include_router(forecast.router)
api_router.include_router(recommendation.router)
api_router.include_router(risk.router)
api_router.include_router(market_entry.router)
api_router.include_router(split_cargo.router)
api_router.include_router(idle_vessel.router)
api_router.include_router(simulation.router)
api_router.include_router(assistant.router)
api_router.include_router(market.router)
