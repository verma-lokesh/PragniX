from sqlalchemy.orm import Session
from core.agents.market_research.graph import run_market_research_graph


class MarketResearchAgent:
    def run(self, db: Session) -> dict:
        return run_market_research_graph(db)
