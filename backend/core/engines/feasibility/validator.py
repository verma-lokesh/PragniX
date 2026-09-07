from config.constants import VESSEL_CLASSES
from core.engines.feasibility.rules import check_vessel_port_compatibility, check_delivery_window


def validate_all_vessels(decision_request, transit_days_by_class: dict[str, float]) -> dict:
    feasible = []
    infeasible = []

    for vessel_class in VESSEL_CLASSES:
        ok, reason = check_vessel_port_compatibility(vessel_class, decision_request.destination)
        if not ok:
            infeasible.append({"vessel_class": vessel_class, "reason": reason})
            continue

        ok2, reason2 = check_vessel_port_compatibility(vessel_class, decision_request.origin) \
            if decision_request.origin in transit_days_by_class.get("_known_ports", []) else (True, None)

        transit_days = transit_days_by_class.get(vessel_class, 20.0)
        ok3, reason3 = check_delivery_window(
            decision_request.earliest_loading_date, decision_request.latest_delivery_date, transit_days
        )
        if not ok3:
            infeasible.append({"vessel_class": vessel_class, "reason": reason3})
            continue

        feasible.append(vessel_class)

    return {
        "feasible_vessels": feasible,
        "infeasible_vessels": infeasible,
        "port_compatible": len(feasible) > 0,
        "route_compatible": decision_request.destination in transit_days_by_class.get("_known_ports", [decision_request.destination]),
    }
