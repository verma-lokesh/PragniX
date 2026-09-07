"""Simple deterministic router standing in for a LangGraph tool-calling graph.
Maps a natural-language-ish intent to the correct backend tool call, since
running this without an LLM key still needs to answer the example questions
in the spec. When LLM_API_KEY is configured, this is the seam where an LLM
would perform tool selection instead of the keyword router below.
"""
from sqlalchemy.orm import Session
from core.agents.ops_assistant.tools import TOOLS


def route_and_answer(db: Session, decision_id: str, message: str) -> dict:
    msg = message.lower()

    if "why" in msg and "capesize" in msg:
        rec = TOOLS["get_recommendation"](db, decision_id)
        cape = next((r for r in rec if r["vessel_class"] == "Capesize"), None)
        return {"answer": cape["rejection_reason"] if cape and not cape["is_feasible"] else "Capesize is feasible for this decision.", "tool": "get_recommendation"}

    if "book now" in msg or "why should i book" in msg:
        me = TOOLS["get_market_entry"](db, decision_id)
        if not me:
            return {"answer": "No market-entry recommendation is available for this decision yet.", "tool": "get_market_entry"}
        return {"answer": f"Recommended action: {me['recommended_action']} (confidence {me['confidence']}). " + " ".join(me["reasons"]), "tool": "get_market_entry"}

    if "landed cost" in msg:
        lc = TOOLS["get_landed_cost"](db, decision_id)
        if not lc:
            return {"answer": "No landed cost has been calculated yet for this decision.", "tool": "get_landed_cost"}
        best = min(lc, key=lambda x: x["cost_per_ton"])
        return {"answer": f"Estimated landed cost is lowest for {best['vessel_class']} at ${best['cost_per_ton']}/ton (total ${best['total_cost']}).", "tool": "get_landed_cost"}

    if "best vessel" in msg or "which vessel" in msg:
        rec = TOOLS["get_recommendation"](db, decision_id)
        top = next((r for r in sorted(rec, key=lambda r: r["rank"]) if r["is_feasible"]), None)
        if not top:
            return {"answer": "No feasible vessel was found for this decision.", "tool": "get_recommendation"}
        return {"answer": f"The recommended vessel is {top['vessel_class']} using a {top['charter_strategy']} strategy (score {top['score']}).", "tool": "get_recommendation"}

    if "risk" in msg:
        risks = TOOLS["get_risk"](db, decision_id)
        if not risks:
            return {"answer": "No risk assessment is available yet.", "tool": "get_risk"}
        lowest = min(risks, key=lambda r: {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}[r["risk_level"]])
        return {"answer": f"Lowest current risk factor is {lowest['risk_type']} ({lowest['risk_level']}): {lowest['description']}", "tool": "get_risk"}

    if "what happens if" in msg or "simulate" in msg or "%" in msg:
        pct = 15.0
        for token in msg.replace("%", " % ").split():
            try:
                pct = float(token)
                break
            except ValueError:
                continue
        result = TOOLS["run_simulation"](db, decision_id, pct)
        return {"answer": f"Under a {pct}% freight rate change, estimated cost delta is ${result['cost_delta']}. {result['recommendation_impact']}", "tool": "run_simulation"}

    status = TOOLS["get_decision_status"](db, decision_id)
    return {"answer": f"Decision {decision_id} status: {status.get('status', 'unknown')}.", "tool": "get_decision_status"}
