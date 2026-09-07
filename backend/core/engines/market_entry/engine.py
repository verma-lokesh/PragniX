from core.interfaces.engine import Engine
from core.engines.market_entry.timing import determine_action, ideal_window
from core.engines.market_entry.signal_analyzer import analyze_signals
from utils.calculations import pct_change


class MarketEntryEngine(Engine):
    name = "MarketEntryEngine"

    def execute(self, context) -> None:
        forecasts = context.forecast_result or []
        if not forecasts:
            context.market_entry_result = None
            return

        best = min(forecasts, key=lambda f: f["predicted_rate"])
        expected_change_pct = pct_change(
            (best["lower_bound"] + best["upper_bound"]) / 2, best["predicted_rate"]
        )
        volatility_pct = pct_change(best["lower_bound"], best["upper_bound"])
        signals = context.master_data.get("market_signals", [])
        signal_summary = analyze_signals(signals)

        action, confidence = determine_action(
            best["direction"], expected_change_pct, volatility_pct, signal_summary["avg_sentiment"]
        )
        window_start, window_end = ideal_window(context.decision_request.earliest_loading_date, action)

        reasons = [
            f"{best['vessel_class']} freight rate direction is {best['direction']}.",
            f"Forecast confidence is {best['confidence']}.",
        ]
        if signal_summary["notable"]:
            reasons.append("Notable market signals detected in recent data.")

        context.market_entry_result = {
            "recommended_action": action,
            "ideal_entry_window_start": window_start.isoformat(),
            "ideal_entry_window_end": window_end.isoformat(),
            "expected_rate_change_pct": expected_change_pct,
            "confidence": confidence,
            "reasons": reasons,
            "risk_factors": signal_summary["notable"],
        }
