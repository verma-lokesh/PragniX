def analyze_signals(market_signals: list) -> dict:
    if not market_signals:
        return {"avg_sentiment": 0.0, "avg_impact": 0.0, "notable": []}
    sentiments = [s.sentiment_score for s in market_signals]
    impacts = [s.impact_score for s in market_signals]
    notable = [s.description for s in market_signals if abs(s.impact_score) > 0.5][:3]
    return {
        "avg_sentiment": round(sum(sentiments) / len(sentiments), 3),
        "avg_impact": round(sum(impacts) / len(impacts), 3),
        "notable": notable,
    }
