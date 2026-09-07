import datetime
from core.interfaces.engine import Engine
from core.engines.forecast.feature_builder import build_features
from core.engines.forecast.predictor import predict_rate
from core.engines.forecast.confidence import compute_confidence
from config.constants import FORECAST_HORIZONS_DAYS


class ForecastEngine(Engine):
    name = "ForecastEngine"

    def execute(self, context) -> None:
        dr = context.decision_request
        feasible = (context.feasibility_result or {}).get("feasible_vessels", [])
        vessel_classes = feasible or ["Panamax"]

        results = []
        horizon = self._select_horizon(dr)
        for vessel_class in vessel_classes:
            features = build_features(dr, vessel_class, context.master_data)
            prediction = predict_rate(features, horizon)
            confidence = compute_confidence(prediction.pop("sample_size", 0), prediction["model_type"])
            results.append({
                "vessel_class": vessel_class,
                "horizon_days": horizon,
                "confidence": confidence,
                "forecast_date": datetime.date.today().isoformat(),
                **prediction,
            })
        context.forecast_result = results

    @staticmethod
    def _select_horizon(dr) -> int:
        days_out = (dr.latest_delivery_date - dr.earliest_loading_date).days
        for h in FORECAST_HORIZONS_DAYS:
            if days_out <= h:
                return h
        return FORECAST_HORIZONS_DAYS[-1]
