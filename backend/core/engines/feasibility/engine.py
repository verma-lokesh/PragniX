from core.interfaces.engine import Engine
from core.engines.feasibility.validator import validate_all_vessels
from config.constants import PORT_SPECS


class FeasibilityEngine(Engine):
    name = "FeasibilityEngine"

    def execute(self, context) -> None:
        dr = context.decision_request
        route = context.master_data.get("route")
        base_transit = route.typical_transit_days if route else 18.0

        transit_days_by_class = {
            "Handysize": base_transit * 1.05,
            "Supramax": base_transit * 1.02,
            "Panamax": base_transit,
            "Capesize": base_transit * 0.97,
            "_known_ports": list(PORT_SPECS.keys()),
        }

        context.feasibility_result = validate_all_vessels(dr, transit_days_by_class)
