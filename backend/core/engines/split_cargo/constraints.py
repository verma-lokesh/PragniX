from config.constants import VESSEL_SPECS, PORT_SPECS


def max_feasible_dwt(port_name: str) -> float:
    port = PORT_SPECS.get(port_name, {})
    feasible_classes = [
        vc for vc, spec in VESSEL_SPECS.items()
        if spec["draft"] <= port.get("max_draft", 0) and spec["loa"] <= port.get("max_loa", 0)
    ]
    if not feasible_classes:
        return 0.0
    return max(VESSEL_SPECS[vc]["dwt"] for vc in feasible_classes)
