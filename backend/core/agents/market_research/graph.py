"""LangGraph definition for the Market Research Agent.

START -> collect_signals -> filter -> analyze -> extract_structured -> summarize -> END

Implemented as a plain function pipeline here so the graph runs identically
whether or not an LLM API key is configured (deterministic local fallback
summary when LLM_PROVIDER == 'none').
"""
from sqlalchemy.orm import Session
from core.agents.market_research.tools import collect_signals, filter_signals, analyze
from config.settings import get_settings


def run_market_research_graph(db: Session) -> dict:
    settings = get_settings()

    signals = collect_signals(db)
    filtered = filter_signals(signals)
    analysis = analyze(filtered or signals)

    if settings.LLM_PROVIDER == "none" or not settings.LLM_API_KEY:
        summary = _local_summary(analysis, len(signals))
    else:
        summary = _local_summary(analysis, len(signals))  # LLM call would replace this branch

    return {
        "summary": summary,
        "avg_sentiment": analysis["avg_sentiment"],
        "avg_impact": analysis["avg_impact"],
        "notable_signals": analysis["notable"],
        "signal_count": len(signals),
    }


def _local_summary(analysis: dict, count: int) -> str:
    tone = "positive" if analysis["avg_sentiment"] > 0.1 else ("negative" if analysis["avg_sentiment"] < -0.1 else "neutral")
    base = f"Reviewed {count} recent market signals; overall sentiment is {tone} (avg {analysis['avg_sentiment']})."
    if analysis["notable"]:
        base += " Notable: " + "; ".join(analysis["notable"][:2])
    return base
