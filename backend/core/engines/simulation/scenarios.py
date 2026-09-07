from dataclasses import dataclass


@dataclass
class ScenarioParams:
    freight_rate_pct_change: float = 0.0
    port_congestion_pct_change: float = 0.0
    bunker_price_pct_change: float = 0.0
    demand_pct_change: float = 0.0
    delivery_delay_days: float = 0.0
