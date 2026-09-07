from config.constants import VESSEL_SPECS, PORT_SPECS


def check_vessel_port_compatibility(vessel_class: str, port_name: str) -> tuple[bool, str | None]:
    vessel = VESSEL_SPECS.get(vessel_class)
    port = PORT_SPECS.get(port_name)
    if not vessel or not port:
        return False, f"Unknown vessel class or port: {vessel_class}/{port_name}"

    if vessel["draft"] > port["max_draft"]:
        return False, (
            f"{vessel_class} rejected: destination draft limit "
            f"({port['max_draft']}m) is lower than vessel operating draft ({vessel['draft']}m)."
        )
    if vessel["loa"] > port["max_loa"]:
        return False, f"{vessel_class} rejected: LOA ({vessel['loa']}m) exceeds port max LOA ({port['max_loa']}m)."
    if vessel["beam"] > port["max_beam"]:
        return False, f"{vessel_class} rejected: beam ({vessel['beam']}m) exceeds port max beam ({port['max_beam']}m)."
    return True, None


def check_delivery_window(loading_date, delivery_date, transit_days: float) -> tuple[bool, str | None]:
    available_days = (delivery_date - loading_date).days
    if available_days < transit_days:
        return False, (
            f"Delivery window ({available_days} days) is shorter than the typical "
            f"transit time ({transit_days:.1f} days)."
        )
    return True, None


def check_storage_and_handling(cargo_quantity: float, port_name: str) -> tuple[bool, str | None]:
    port = PORT_SPECS.get(port_name)
    if not port:
        return False, f"Unknown port: {port_name}"
    if cargo_quantity > port.get("storage_capacity_tons", 500000):
        return False, "Cargo quantity exceeds destination storage capacity."
    return True, None
